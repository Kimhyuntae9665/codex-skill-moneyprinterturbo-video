from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install_bundle
import audit_bundle


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DistributionTests(unittest.TestCase):
    def test_full_distribution_has_no_missing_references_or_files(self):
        report = audit_bundle.audit()
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['bundled_skills'], 53)
        self.assertEqual(report['external_skills'], 12)

    def test_corrupted_file_fails_before_install(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            (root / 'distribution').mkdir()
            (root / 'sample.txt').write_text('tampered', encoding='utf-8')
            (root / 'distribution/file-manifest.json').write_text(json.dumps({'files': [{'path': 'sample.txt', 'sha256': '0' * 64}]}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'modified'):
                install_bundle.verify_bundle(root)

    def test_fresh_core_install_conflict_refusal_and_backup(self):
        with tempfile.TemporaryDirectory() as work:
            target = Path(work) / 'skills'
            plan = install_bundle.install('core', target, dry_run=True)
            self.assertFalse(target.exists())
            self.assertEqual(len(plan['skills']), 3)
            install_bundle.install('core', target)
            marker = target / 'moneyprinterturbo-video/user-change.txt'
            marker.write_text('preserve me', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                install_bundle.install('core', target)
            self.assertEqual(marker.read_text(), 'preserve me')
            report = install_bundle.install('core', target, overwrite=True)
            self.assertEqual(len(report['backups']), 3)
            backed_up = [Path(p) for p in report['backups'] if p.endswith('moneyprinterturbo-video')][0]
            self.assertEqual((backed_up / 'user-change.txt').read_text(), 'preserve me')
            module = load('installed_preflight', target / 'moneyprinterturbo-video/scripts/check_environment.py')
            with patch.dict(os.environ, {'CODEX_HOME': str(Path(work) / 'unrelated')}):
                companions = module.inspect('us-equity')['companions']
            self.assertEqual(Path(companions['us-stock-research']), target / 'us-stock-research')
            self.assertEqual(Path(companions['logo-flow-infographics']), target / 'logo-flow-infographics')

    def test_external_is_pinned_and_requires_explicit_option(self):
        with tempfile.TemporaryDirectory() as work:
            report = install_bundle.install('all', Path(work) / 'skills', dry_run=True)
            self.assertEqual(len(report['skills']), 53)
            self.assertEqual(len(report['external_not_installed']), 12)
            report = install_bundle.install('all', Path(work) / 'skills', with_external=True, dry_run=True)
            self.assertEqual(len(report['skills']), 65)
            self.assertEqual(report['external_not_installed'], [])

    def test_plugin_companions_discovered_without_author_install(self):
        module = load('plugin_preflight', 'plugins/mpt/skills/mpt/scripts/check_environment.py')
        roots = module.candidate_skill_roots()
        self.assertEqual(roots[0], ROOT / 'plugins/mpt/skills')
        for skill in ['us-stock-research', 'logo-flow-infographics']:
            self.assertEqual(Path(module.find_skill(skill, roots)), ROOT / 'plugins/mpt/skills' / skill)


class AudioPortabilityTests(unittest.TestCase):
    def test_pcm_rms_silence_and_known_samples(self):
        module = load('audio_silence', 'plugins/mpt/skills/mpt/scripts/audit_audio_silence.py')
        self.assertEqual(module.pcm_rms(bytes([128, 128]), 1), 0)
        self.assertEqual(module.pcm_rms(struct.pack('<hhh', -1000, 1000, 1000), 2), 1000)
        for width in [2, 3, 4]:
            samples = b''.join(v.to_bytes(width, 'little', signed=True) for v in [-1000, 1000])
            self.assertEqual(module.pcm_rms(samples, width), 1000)
        with self.assertRaises(ValueError):
            module.pcm_rms(b'\0', 2)


if __name__ == '__main__':
    unittest.main()
