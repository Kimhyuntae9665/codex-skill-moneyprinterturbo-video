"""Install this reviewed skill bundle without changing Codex configuration."""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CORE = {'moneyprinterturbo-video', 'us-stock-research', 'logo-flow-infographics'}


def verify_bundle(root: Path = ROOT) -> int:
    manifest = json.loads((root / 'distribution/file-manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        relative = Path(item['path'])
        path = root / relative
        if relative.is_absolute() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Unsafe manifest path: {relative}')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError(f'Missing or modified package file: {relative}')
    return len(manifest['files'])


def default_target() -> Path:
    return Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'


def install(profile: str, target: Path, overwrite: bool = False,
            with_external: bool = False, dry_run: bool = False) -> dict:
    verified = verify_bundle()
    records = json.loads((ROOT / 'distribution/source-inventory.json').read_text(encoding='utf-8'))['skills']
    selected = [r for r in records if profile == 'all' or r['name'] in CORE]
    if with_external and profile != 'all':
        raise ValueError('--with-external requires --profile all')
    bundled = [r for r in selected if r['distribution'] == 'bundled']
    external = [r for r in selected if r['distribution'] == 'external']
    plan = [{'name': r['name'], 'destination': str(target / r['name'])} for r in bundled]
    if with_external:
        plan += [{'name': r['name'], 'destination': str(target / r['name'])} for r in external]
    conflicts = [p['destination'] for p in plan if Path(p['destination']).exists()]
    report = {'profile': profile, 'verified_files': verified, 'skills': plan,
              'external_not_installed': [] if with_external else [r['name'] for r in external],
              'conflicts': conflicts, 'dry_run': dry_run, 'backups': []}
    if dry_run:
        return report
    if conflicts and not overwrite:
        raise FileExistsError('Existing skills would be replaced. Review --dry-run; use --overwrite to back them up and replace explicitly: ' + ', '.join(conflicts))
    if target.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Install outside this repository, not over the distribution sources')
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='mpt-install-') as work:
        staging = Path(work)
        for r in bundled:
            shutil.copytree(ROOT / r['path'], staging / r['name'])
        # The plugin retains its legacy mpt folder; standalone uses the public
        # skill name. Keep cross-skill documentation links correct in that form.
        for document in staging.rglob('*.md'):
            text = document.read_text(encoding='utf-8')
            revised = text.replace('../../mpt/references/', '../../moneyprinterturbo-video/references/')
            if revised != text:
                document.write_text(revised, encoding='utf-8')
        if with_external:
            # These contents are obtained on the user's machine, never redistributed here.
            repo = staging / 'upstream-remotion'
            first = external[0]
            subprocess.run(['git', 'clone', '--no-checkout', first['repository'], str(repo)], check=True)
            subprocess.run(['git', '-C', str(repo), 'checkout', '--detach', first['commit']], check=True)
            actual = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
            if actual != first['commit']:
                raise ValueError('Upstream commit verification failed')
            for r in external:
                source = repo / r['path']
                if not (source / 'SKILL.md').is_file():
                    raise FileNotFoundError('Upstream skill not present: ' + r['name'])
                shutil.copytree(source, staging / r['name'])
        backup_root = target.parent / 'mpt-skill-backups' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        for p in plan:
            destination = Path(p['destination'])
            incoming = target / ('.mpt-incoming-' + p['name'])
            if incoming.exists():
                raise FileExistsError('An earlier temporary install remains: ' + str(incoming))
            shutil.copytree(staging / p['name'], incoming)
            backup = None
            try:
                if destination.exists():
                    backup_root.mkdir(parents=True, exist_ok=True)
                    backup = backup_root / p['name']
                    destination.rename(backup)
                    report['backups'].append(str(backup))
                incoming.rename(destination)
            except Exception:
                if backup and not destination.exists():
                    backup.rename(destination)
                raise
            finally:
                if incoming.exists():
                    shutil.rmtree(incoming)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['core', 'all'], default='core')
    parser.add_argument('--target', type=Path, default=default_target())
    parser.add_argument('--with-external', action='store_true', help='Fetch 12 official Remotion skills at the pinned commit; requires Git and network')
    parser.add_argument('--overwrite', action='store_true', help='Back up existing skill folders, then replace them')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        report = install(args.profile, args.target.expanduser().resolve(), args.overwrite, args.with_external, args.dry_run)
    except (ValueError, FileExistsError, FileNotFoundError, subprocess.CalledProcessError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
