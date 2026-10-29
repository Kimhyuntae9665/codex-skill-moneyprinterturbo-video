"""Synthetic contract regressions; these do not certify a real video's reviews."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_delivery as delivery
import validate_video as video
import probe_scene_frames as probe


class DurationTests(unittest.TestCase):
    def test_focused_thirty_seconds_passes(self):
        args = video.parse_args(["--video", "synthetic.mp4", "--duration-profile", "focused"])
        video.validate_metadata(dict(duration=30.0, width=1080, height=1920,
                                     video_codec="h264", audio_codec="aac"), args)

    def test_full_thirty_seconds_still_fails(self):
        args = video.parse_args(["--video", "synthetic.mp4", "--duration-profile", "full"])
        with self.assertRaises(video.ValidationError):
            video.validate_metadata(dict(duration=30.0, width=1080, height=1920,
                                         video_codec="h264", audio_codec="aac"), args)

    def test_custom_bounds(self):
        args = video.parse_args(["--video", "synthetic.mp4", "--duration-profile", "custom",
                                 "--min-duration", "65", "--max-duration", "70"])
        self.assertEqual((args.min_duration, args.max_duration), (65, 70))


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.reports = {}
        self.paths = {}
        for name in delivery.ARTIFACT_FIELDS + ("news_context_report",):
            path = self.root / (name + ".json")
            path.write_text("synthetic fixture", encoding="utf-8")
            self.paths[name] = str(path)
        digest = hashlib.sha256(Path(self.paths["video"]).read_bytes()).hexdigest()
        self.reports["production"] = {"editorial_route": "news-explainer", "content_kind": "company",
                                       "strategy": {"duration_profile": "full"}}
        self.reports["layout_report"] = {"pass": True}
        self.reports["video_report"] = {"pass": True, "duration": 50.0, "duration_profile": "full", "video_sha256": digest}
        self.reports["scene_probe_report"] = {"pass": True, "video_sha256": digest}
        official_row = dict(scene_id="S1", asset_id="A1", official_publisher="synthetic publisher",
            source_page_url="https://example.org/demo", source_media_url="https://example.org/demo.mp4",
            source_in_s=0, source_out_s=30, output_start_s=0, output_end_s=30,
            narration_match="synthetic eligibility fixture", review_evidence="not an actual review")
        self.reports["official_video_report"] = {"pass": True, "video_sha256": digest,
            "duration_s": 50.0, "official_video_s": 30.0, "official_video_share": 0.60, "intervals": [official_row]}
        self.reports["news_context_report"] = {"pass": True, "video_sha256": digest, "duration_s": 50.0,
            "narrated_intervals": [{"start_s": 0, "end_s": 48}], "narrated_s": 48.0,
            "intervals": [{"start_s": 0, "end_s": 15, "spoken_point": "synthetic business context",
                "source_url": "https://example.org/news", "source_date": "2026-10-27", "review_evidence": "synthetic"}],
            "news_context_s": 15.0, "news_context_share": 15 / 48}
        self.status = {"schema_version": "mpt-delivery-status-v2", **dict.fromkeys(delivery.PASS_FIELDS, "PASS"),
            "editorial_route": "news-explainer", "content_kind": "company", "news_context_qa": "PASS",
            "official_video_share": 0.60, "emphasis_plan_count": 0, "emphasis_cue_count": 0,
            "artifacts": self.paths, "reviews": {
                "audio": {"reviewer": "synthetic", "observations": ["fixture, not listening"]},
                "visual": {"reviewer": "synthetic", "observations": ["fixture, not playback"], "timestamps_s": [0, 49]}}}

    def errors(self):
        for name, value in self.reports.items():
            Path(self.paths[name]).write_text(json.dumps(value), encoding="utf-8")
        path = self.root / "status.json"
        path.write_text(json.dumps(self.status), encoding="utf-8")
        return delivery.validate(path)

    def test_valid_news_contract_does_not_require_investment_verdict(self):
        self.assertEqual(self.errors(), [])

    def test_empty_official_intervals_cannot_pass_by_claiming_sixty_percent(self):
        self.reports["official_video_report"]["intervals"] = []
        self.assertTrue(self.errors())

    def test_overlapping_footage_is_not_double_counted(self):
        report = self.reports["official_video_report"]
        report["intervals"] = [copy.deepcopy(report["intervals"][0]) for _ in range(2)]
        for row in report["intervals"]:
            row["output_end_s"] = 20
        self.assertTrue(any("recomputed" in error for error in self.errors()))

    def test_news_report_is_required_for_company(self):
        del self.status["artifacts"]["news_context_report"]
        del self.reports["news_context_report"]
        self.assertTrue(any("news_context_report" in error for error in self.errors()))

    def test_below_thirty_percent_news_fails(self):
        report = self.reports["news_context_report"]
        report["intervals"][0]["end_s"] = 10
        report["news_context_s"], report["news_context_share"] = 10, 10 / 48
        self.assertTrue(any("below 0.30" in error for error in self.errors()))

    def test_news_outside_narration_fails(self):
        self.reports["news_context_report"]["intervals"][0].update(start_s=35, end_s=50)
        self.assertTrue(any("outside measured narrated" in error for error in self.errors()))

    def test_stale_hash_fails(self):
        self.reports["video_report"]["video_sha256"] = "0" * 64
        self.assertTrue(any("video_sha256" in error for error in self.errors()))

    def test_unperformed_listening_cannot_pass(self):
        self.status["audio_listening"] = "NOT_PERFORMED"
        self.assertTrue(self.errors())

    def test_boolean_cue_counts_and_negative_review_timestamp_fail(self):
        self.status.update(emphasis_plan_count=False, emphasis_cue_count=True)
        self.status["reviews"]["visual"]["timestamps_s"] = [-1]
        errors = self.errors()
        self.assertTrue(any("integer" in e for e in errors))
        self.assertTrue(any("timestamps" in e for e in errors))

    def test_production_cannot_be_bypassed_by_changing_status_route(self):
        self.status["content_kind"] = "general"
        self.assertTrue(any("differs" in error for error in self.errors()))

    def test_canonical_profile_mismatch_fails(self):
        self.reports["production"]["strategy"]["duration_profile"] = "focused"
        self.assertTrue(any("profile" in error for error in self.errors()))

    def test_no_scene_probe_cannot_pass(self):
        del self.status["artifacts"]["scene_probe_report"]
        del self.reports["scene_probe_report"]
        self.assertTrue(any("scene_probe_report" in error for error in self.errors()))

    def test_investment_route_requires_verdict_review(self):
        self.status["editorial_route"] = self.reports["production"]["editorial_route"] = "investment-analysis"
        self.assertTrue(any("verdict_qa" in error for error in self.errors()))


class FreezeTests(unittest.TestCase):
    def setUp(self):
        self.raw = {"pass": False, "threshold_s": 1, "events": [{"start_s": 1, "end_s": 3, "duration_s": 2}]}
        self.errors = ["freeze_0_at_least_1.00s"]

    def review(self, digest="abc", start=1, end=3, extra_errors=None):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "review.json"
            path.write_text(json.dumps({"video_sha256": digest, "intervals": [{"start_s": start, "end_s": end,
                "kind": "source_native_wait", "asset_id": "A1", "reviewer": "synthetic",
                "reason": "fixture", "evidence": "synthetic only"}]}), encoding="utf-8")
            return probe.review_freezes(self.raw, self.errors + (extra_errors or []), path, "abc", 5)

    def test_unreviewed_freeze_stays_hold(self):
        self.assertTrue(probe.review_freezes(self.raw, self.errors, None, "abc", 5)[1])

    def test_individually_reviewed_native_wait_keeps_raw_failure(self):
        report, errors = self.review()
        self.assertEqual(errors, [])
        self.assertFalse(report["raw"]["pass"])
        self.assertTrue(report["pass"])

    def test_whole_video_waiver_rejected(self):
        self.assertTrue(self.review(start=0, end=5)[1])

    def test_stale_freeze_review_rejected(self):
        self.assertTrue(self.review(digest="stale")[1])

    def test_decoder_failure_cannot_be_waived(self):
        self.assertTrue(self.review(extra_errors=["freezedetect_failed:decoder"])[1])

    def test_actual_detector_error_is_retained_even_with_events(self):
        fixture = subprocess.CompletedProcess([], 1, "", "freeze_start: 1\nfreeze_end: 3 freeze_duration: 2")
        with patch.object(probe, "run", return_value=fixture):
            self.assertTrue(any("freezedetect_failed" in e for e in probe.detect_freezes("ffmpeg", Path("fake"), 1)[1]))


if __name__ == "__main__":
    unittest.main()
