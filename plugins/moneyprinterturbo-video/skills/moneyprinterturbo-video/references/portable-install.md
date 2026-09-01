# Portable installation and dependency contract

Read this reference on a fresh machine, after installing from a ZIP or GitHub,
or when the workflow behaves differently from the author's machine.

## Required local tools

- Git
- Python 3.11 or newer
- `uv`
- FFmpeg and FFprobe
- network access for the pinned upstream checkout, Python dependencies, and
  Edge TTS during the first run

Run the bundled preflight from the Skill directory:

```text
python scripts/check_environment.py --json
```

For a US-equity Short, use:

```text
python scripts/check_environment.py --mode us-equity --json
```

The preflight checks executable availability, the bundled font and scripts,
and whether companion Skills can be discovered in common Codex user locations.
It does not download dependencies or modify the machine.

## Companion capabilities

Ordinary prepared-local video work does not require another Skill. The
following capabilities become relevant only for their matching mode:

- `us-stock-research`: required by the US-equity research gate. If absent,
  independently lock the primary SEC and issuer-IR evidence or place production
  on HOLD; do not invent or reuse stale numbers.
- `infographic-creator`: required when the frozen storyboard calls for a
  generated editorial infographic. A custom deterministic chart is an allowed
  fallback only when its source values and layout are still validated.
- Unusual Whales: optional secondary market-context check. Record `unavailable`
  when the connector is not installed. Never use it as final evidence for
  company fundamentals, dividends, buybacks, valuation denominators, or 13F
  ownership.

## Installation forms

The release supports two forms:

1. Plugin installation from the repository marketplace. This is preferred when
   sharing the ZIP or installing the whole release.
2. Standalone Skill installation from the nested `skills/moneyprinterturbo-video`
   folder. This is useful for local Codex experimentation.

Start a new Codex task after installation so the new Skill is discovered.

## Portability boundaries

- The Plugin does not include Git, uv, FFmpeg, operating-system codecs, API
  credentials, or optional companion Skills.
- The pinned MoneyPrinterTurbo checkout is created in an isolated runtime on
  first use rather than bundled in the release.
- Example photos and fonts retain their own attribution and license terms. Read
  `THIRD_PARTY_NOTICES.md`, `assets/fonts/OFL.txt`, and each example asset
  manifest before redistributing a modified package.
- Generated videos, QA frames, caches, virtual environments, secrets, and local
  absolute paths must stay outside a release archive.
