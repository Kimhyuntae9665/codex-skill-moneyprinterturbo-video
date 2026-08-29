from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "moneyprinterturbo-video"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MPT = load_module("mpt_agent", SKILL_ROOT / "scripts" / "mpt_agent.py")
VALIDATOR = load_module(
    "validate_video", SKILL_ROOT / "scripts" / "validate_video.py"
)
BURN_SUBTITLES = load_module(
    "burn_subtitles", SKILL_ROOT / "scripts" / "burn_subtitles.py"
)
V3_RESEARCH = load_module(
    "mcd_v3_research",
    SKILL_ROOT
    / "examples"
    / "mcd-valuation-2026"
    / "research"
    / "recompute_v3.py",
)


class RunnerSafetyTests(unittest.TestCase):
    def test_upstream_is_pinned(self) -> None:
        self.assertEqual(
            MPT.UPSTREAM_COMMIT,
            "eb8c23757e098a07bbcd93b3b50e252fc8d1869a",
        )

    def test_effective_source_uses_final_option(self) -> None:
        args = ["--video-source", "pexels", "--video-source=local"]
        self.assertEqual(MPT.selected_video_source(args), "local")

    def test_prepared_local_needs_no_llm_or_stock_key(self) -> None:
        config = "\n".join(
            [
                'llm_provider = "moonshot"',
                'moonshot_api_key = ""',
                "pexels_api_keys = []",
                "pixabay_api_keys = []",
                "coverr_api_keys = []",
            ]
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.toml"
            path.write_text(config, encoding="utf-8")
            provider, missing = MPT.missing_config(
                path,
                [
                    "--video-source",
                    "local",
                    "--video-script",
                    "prepared narration",
                    "--video-materials",
                    "one.png",
                ],
            )
        self.assertEqual(provider, "moonshot")
        self.assertEqual(missing, [])

    def test_online_mode_reports_llm_and_stock_keys(self) -> None:
        config = "\n".join(
            [
                'llm_provider = "moonshot"',
                'moonshot_api_key = ""',
                "pexels_api_keys = []",
            ]
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.toml"
            path.write_text(config, encoding="utf-8")
            _, missing = MPT.missing_config(path, [])
        self.assertEqual(missing, ["moonshot_api_key", "pexels_api_keys"])

    def test_upload_switches_are_forced_off(self) -> None:
        config = "\n".join(
            [
                "upload_post_enabled = true",
                "upload_post_auto_upload = true",
                'upload_post_platforms = ["youtube"]',
            ]
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.toml"
            path.write_text(config, encoding="utf-8")
            MPT.enforce_no_upload(path)
            result = path.read_text(encoding="utf-8")
        self.assertIn("upload_post_enabled = false", result)
        self.assertIn("upload_post_auto_upload = false", result)
        self.assertIn("upload_post_platforms = []", result)

    def test_paid_provider_requires_confirmation(self) -> None:
        args = Namespace(
            cli_args=["--video-source", "volcengine_seedance"],
            script_file=None,
            material=[],
            materials_dir=None,
            font_file=None,
            confirm_paid_provider=False,
        )
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(MPT.SkillError, "explicit"):
                MPT.build_forwarded_cli_args(args, Path(temp))

    def test_materials_are_sorted_and_comma_paths_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "b.png").write_bytes(b"png")
            (root / "a.jpg").write_bytes(b"jpg")
            (root / "ignore.txt").write_text("ignored", encoding="utf-8")
            materials = MPT.collect_local_materials([], root)
            self.assertEqual([path.name for path in materials], ["a.jpg", "b.png"])
            bad = root / "bad,name.png"
            bad.write_bytes(b"png")
            with self.assertRaisesRegex(MPT.SkillError, "commas"):
                MPT.collect_local_materials([bad], None)


class AssetAndExampleTests(unittest.TestCase):
    def test_skill_markdown_is_ascii(self) -> None:
        (SKILL_ROOT / "SKILL.md").read_text(encoding="ascii")

    def test_font_covers_every_modern_hangul_syllable(self) -> None:
        font = TTFont(SKILL_ROOT / "assets" / "fonts" / "NotoSansKR-Bold.ttf")
        codepoints = set()
        for table in font["cmap"].tables:
            codepoints.update(table.cmap)
        missing = [codepoint for codepoint in range(0xAC00, 0xD7A4) if codepoint not in codepoints]
        self.assertEqual(missing, [])

    def test_example_materials_are_reproducible_portrait_frames(self) -> None:
        script = SKILL_ROOT / "examples" / "mcd-2025" / "make_materials.py"
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "frames"
            environment = os.environ.copy()
            environment["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(
                [sys.executable, str(script), "--output", str(output)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=environment,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((output / "materials-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["frame_count"], 8)
            frames = sorted(output.glob("*-mcd-frame.png"))
            self.assertEqual(len(frames), 8)
            for frame in frames:
                with Image.open(frame) as image:
                    self.assertEqual(image.size, (1080, 1920))

    def test_probe_summary_requires_video_and_audio(self) -> None:
        summary = VALIDATOR.summarize_probe(
            {
                "streams": [
                    {"codec_type": "video", "codec_name": "h264", "width": 1080, "height": 1920},
                    {"codec_type": "audio", "codec_name": "aac"},
                ],
                "format": {"duration": "54.2"},
            }
        )
        self.assertEqual(summary["duration"], 54.2)
        self.assertEqual(summary["video_codec"], "h264")
        self.assertEqual(summary["audio_codec"], "aac")

    def test_professional_mcd_example_preserves_claim_limits(self) -> None:
        example = SKILL_ROOT / "examples" / "mcd-valuation-2026"
        narration = (example / "narration.ko.txt").read_text(encoding="utf-8")
        sources = (example / "sources.md").read_text(encoding="utf-8")
        self.assertIn("비조정 종가", narration)
        self.assertIn("최근 5년", narration)
        self.assertIn("20년", narration)
        self.assertIn("임대료는 이익이 아니고", narration)
        self.assertNotIn("지금 매수", narration)
        self.assertNotIn("역사적 저평가", narration)
        self.assertIn("260.06 / 341.06 - 1 = -23.7495%", sources)
        self.assertIn("가맹 매출은 이익이나 현금흐름이 아니고", sources)

    def test_professional_motion_uses_a_pinned_open_source_renderer(self) -> None:
        motion = SKILL_ROOT / "examples" / "mcd-valuation-2026" / "motion"
        project = (motion / "pyproject.toml").read_text(encoding="utf-8")
        scene = (motion / "mcd_short.py").read_text(encoding="utf-8")
        self.assertIn('"manim==0.21.0"', project)
        self.assertIn("config.pixel_width = 1080", scene)
        self.assertIn("config.pixel_height = 1920", scene)
        self.assertIn("config.frame_rate = 30", scene)
        self.assertIn("price_history.csv", scene)
        self.assertIn("two rights-cleared building photos are required", scene)

    def test_professional_research_packet_recomputes_displayed_drawdown(self) -> None:
        research = SKILL_ROOT / "examples" / "mcd-valuation-2026" / "research"
        facts = json.loads((research / "facts.json").read_text(encoding="utf-8"))
        self.assertEqual(len(facts["sources"]), 14)
        self.assertEqual(len(facts["facts"]), 56)

        with (research / "price_history.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        window = [
            row for row in rows if "2026-02-27" <= row["date"] <= "2026-08-27"
        ]
        self.assertEqual(len(window), 126)
        self.assertEqual(
            (window[0]["date"], float(window[0]["raw_close"])),
            ("2026-02-27", 341.06),
        )
        self.assertEqual(
            (window[-1]["date"], float(window[-1]["raw_close"])),
            ("2026-08-27", 260.06),
        )
        drawdown = (
            float(window[-1]["raw_close"]) / float(window[0]["raw_close"]) - 1
        ) * 100
        self.assertAlmostEqual(drawdown, -23.7494868938, places=8)

        with (research / "calculations.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            calculations = {row["metric"]: row for row in csv.DictReader(handle)}
        self.assertEqual(len(calculations), 30)
        self.assertAlmostEqual(
            float(calculations["raw_close_drawdown"]["result"]), drawdown, places=8
        )

    def test_professional_photo_assets_match_rights_manifest(self) -> None:
        assets = SKILL_ROOT / "examples" / "mcd-valuation-2026" / "assets"
        manifest = json.loads(
            (assets / "asset-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(manifest["assets"]), 2)
        for item in manifest["assets"]:
            path = assets / item["filename"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
            self.assertEqual(digest, item["file"]["sha256"])
            with Image.open(path) as image:
                self.assertEqual(
                    image.size,
                    (item["file"]["width_px"], item["file"]["height_px"]),
                )
            self.assertIn(item["source"]["license"], {"CC0 1.0", "CC BY 4.0"})
            self.assertTrue(item["source"]["author"])
            self.assertTrue(
                item["source"]["commons_page_url"].startswith(
                    "https://commons.wikimedia.org/"
                )
            )

    def test_v3_shareholder_return_and_market_sensitivity_recompute(self) -> None:
        metrics = V3_RESEARCH.compute()
        method = metrics["weekly_risk_method"]
        risk = metrics["risk_metrics"]
        shareholder = metrics["shareholder_return"]

        self.assertEqual(method["price_rows"], 262)
        self.assertEqual(method["return_observations"], 261)
        self.assertAlmostEqual(risk["mcd_beta_vs_spy"], 0.4766795, places=6)
        self.assertAlmostEqual(risk["qqq_beta_vs_spy"], 1.2516079, places=6)
        self.assertAlmostEqual(risk["mcd_qqq_correlation"], 0.3273663, places=6)
        self.assertEqual(shareholder["ttm_dividends_usd_millions"], 5225.0)
        self.assertEqual(shareholder["ttm_net_cash_buybacks_usd_millions"], 2086.0)
        self.assertEqual(
            shareholder["ttm_cash_shareholder_return_usd_millions"], 7311.0
        )
        self.assertAlmostEqual(
            shareholder["total_cash_shareholder_yield"], 0.039727, places=6
        )
        self.assertEqual(shareholder["dividend_increase_streak_years"], 50.0)

    def test_v3_narration_preserves_market_risk_limits(self) -> None:
        example = SKILL_ROOT / "examples" / "mcd-valuation-2026"
        narration = (example / "narration.v3.ko.txt").read_text(encoding="utf-8")
        sources = (example / "sources-v3.md").read_text(encoding="utf-8")
        for claim in (
            "순현금 자사주매입 21억 달러",
            "배당은 50년 연속 인상",
            "맥도날드 0.48",
            "큐큐큐 1.25",
            "상관은 0.33",
            "반대로 움직인 게 아니라",
            "낮은 베타가 낮은 위험을 보장하진 않습니다",
        ):
            self.assertIn(claim, narration)
        self.assertNotIn("기술주보다 안전", narration)
        self.assertNotIn("지금 매수", narration)
        self.assertIn("회사가 공시한 공식 비율이 아니라", sources)
        self.assertIn("반대로 움직임", sources)

    def test_v3_motion_and_reviewed_subtitles_are_portrait_safe(self) -> None:
        example = SKILL_ROOT / "examples" / "mcd-valuation-2026"
        scene = (example / "motion" / "mcd_short_v3.py").read_text(encoding="utf-8")
        for marker in (
            "config.pixel_width = 1080",
            "config.pixel_height = 1920",
            "config.frame_rate = 30",
            "MCDShareholderReturnShort",
            "weekly_adjusted_prices_v3.csv",
            "LOW BETA",
        ):
            self.assertIn(marker, scene)

        subtitle_text = (example / "subtitle.v3.srt").read_text(encoding="utf-8")
        blocks = [block for block in re.split(r"\r?\n\r?\n", subtitle_text.strip()) if block]
        self.assertEqual(len(blocks), 21)
        previous_end = 0.0
        for block in blocks:
            lines = block.splitlines()
            self.assertGreaterEqual(len(lines), 3)
            self.assertLessEqual(len(lines[2:]), 2)
            timestamps = re.findall(r"(\d\d):(\d\d):(\d\d),(\d\d\d)", lines[1])
            self.assertEqual(len(timestamps), 2)
            start, end = [
                int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000
                for hours, minutes, seconds, millis in timestamps
            ]
            self.assertGreaterEqual(start, previous_end)
            self.assertGreater(end, start)
            previous_end = end
        self.assertAlmostEqual(previous_end, 57.42, places=2)

    def test_subtitle_repair_filter_is_explicit_and_mobile_readable(self) -> None:
        example = SKILL_ROOT / "examples" / "mcd-valuation-2026"
        filter_text = BURN_SUBTITLES.subtitle_filter(
            example / "subtitle.v3.srt",
            SKILL_ROOT / "assets" / "fonts",
            font_name="Noto Sans KR",
            font_size=11,
            margin_v=66,
        )
        self.assertIn("subtitles=filename=", filter_text)
        self.assertIn("FontName=Noto Sans KR", filter_text)
        self.assertIn("FontSize=11", filter_text)
        self.assertIn("Alignment=2", filter_text)
        self.assertIn("MarginV=66", filter_text)


class RepositoryHygieneTests(unittest.TestCase):
    def test_no_runtime_outputs_or_credentials_are_committed(self) -> None:
        forbidden_names = {"config.toml", ".env"}
        forbidden_suffixes = {".mp4", ".log", ".pyc"}
        violations = []
        for path in REPO_ROOT.rglob("*"):
            if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                continue
            if path.is_file() and (
                path.name in forbidden_names or path.suffix.lower() in forbidden_suffixes
            ):
                violations.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
