#!/usr/bin/env python3
"""Scan a directory of Hasselblad .3FR files and emit a reproducible sequence manifest."""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path
VALID = {4, 6, 16}
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()
def exif_times(paths: list[Path]) -> dict[str, float]:
    tool = shutil.which('exiftool')
    if not tool: return {}
    try:
        p = subprocess.run([tool, '-j', '-DateTimeOriginal', *map(str, paths)], capture_output=True, text=True, check=True)
        result = {}
        for row in json.loads(p.stdout):
            name, raw = row.get('SourceFile'), row.get('DateTimeOriginal')
            if name and raw:
                try: result[str(Path(name).resolve())] = datetime.strptime(raw, '%Y:%m:%d %H:%M:%S').replace(tzinfo=timezone.utc).timestamp()
                except ValueError: pass
        return result
    except Exception: return {}
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('directory', type=Path); ap.add_argument('-o', '--output', type=Path)
    ap.add_argument('--gap-seconds', type=float, default=20.0); ap.add_argument('--expected-count', type=int, choices=sorted(VALID))
    args = ap.parse_args(); root = args.directory.expanduser().resolve()
    if not root.is_dir(): ap.error(f'Not a directory: {root}')
    paths = sorted((p for p in root.rglob('*') if p.is_file() and p.suffix.lower() == '.3fr'), key=lambda p: (p.stat().st_mtime_ns, str(p)))
    if not paths: ap.error('No .3FR files found recursively')
    times = exif_times(paths); rows=[]
    for p in paths:
        stamp = times.get(str(p.resolve()), p.stat().st_mtime)
        rows.append({'path':str(p), 'relativePath':str(p.relative_to(root)), 'bytes':p.stat().st_size, 'sha256':sha256(p), 'timeSource':'exif' if str(p.resolve()) in times else 'mtime', 'sortTime':stamp})
    rows.sort(key=lambda r:(r['sortTime'],r['relativePath'])); groups=[]; current=[]
    for row in rows:
        if current and row['sortTime']-current[-1]['sortTime'] > args.gap_seconds: groups.append(current); current=[]
        current.append(row)
    if current: groups.append(current)
    result=[]
    for i, group in enumerate(groups,1):
        count=len(group); valid=count in VALID
        result.append({'id':f'group-{i:03d}','frames':count,'validFrameCount':valid,'selected':(args.expected_count is None and valid) or count==args.expected_count,'files':group})
    manifest={'schema':'phocus-pixel-shift/1','sourceDirectory':str(root),'createdAt':datetime.now(timezone.utc).isoformat(),'gapSeconds':args.gap_seconds,'groups':result,'warnings':[]}
    if not times: manifest['warnings'].append('EXIF capture times unavailable; groups were inferred from filesystem modification times.')
    for g in result:
        if not g['validFrameCount']: manifest['warnings'].append(f"{g['id']} has {g['frames']} frames; expected exactly 4, 6, or 16.")
    out=(args.output or root/'phocus-pixel-shift-manifest.json').expanduser().resolve(); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'manifest':str(out),'files':len(rows),'groups':[(g['id'],g['frames'],g['selected']) for g in result]},ensure_ascii=False))
    return 0 if any(g['selected'] for g in result) else 3
if __name__ == '__main__': raise SystemExit(main())
