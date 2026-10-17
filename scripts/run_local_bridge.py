#!/usr/bin/env python3
"""Invoke a user-local Phocus bridge for manifest-selected 4/6/16-frame groups."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, shutil, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
    return h.hexdigest()
def resolve_bridge(value: str|None) -> Path:
    candidates=[]
    if value: candidates.append(Path(value).expanduser())
    if os.environ.get('PHOCUS_NATIVE_BRIDGE'): candidates.append(Path(os.environ['PHOCUS_NATIVE_BRIDGE']).expanduser())
    candidates.append(Path.cwd()/'native-fff-bridge')
    for base in (Path.home()/'Desktop/Codex', Path.home()/'Documents/Codex'):
        if base.is_dir():
            candidates.extend(base.rglob('native-fff-bridge'))
    if os.environ.get('PHOCUS_RESEARCH_ROOT'):
        candidates.append(Path(os.environ['PHOCUS_RESEARCH_ROOT']).expanduser()/'native-fff-bridge')
        candidates.append(Path(os.environ['PHOCUS_RESEARCH_ROOT']).expanduser()/'outputs/phocus-4-6-16-20261016/native-fff-bridge')
    for p in candidates:
        if p.is_file() and os.access(p,os.X_OK): return p.resolve()
    raise SystemExit('No local native bridge found. Configure PHOCUS_NATIVE_BRIDGE or pass --bridge; do not download Phocus components.')
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('manifest',type=Path); ap.add_argument('-o','--output',type=Path,required=True); ap.add_argument('--bridge'); ap.add_argument('--native-tiff',action='store_true')
    args=ap.parse_args(); manifest=args.manifest.expanduser().resolve(); data=json.loads(manifest.read_text()); bridge=resolve_bridge(args.bridge)
    phocus=Path('/Applications/Phocus.app')
    if platform.system()=='Darwin' and not phocus.exists(): raise SystemExit('Phocus.app was not found at /Applications/Phocus.app; use the user-installed application path only.')
    out=args.output.expanduser().resolve(); out.mkdir(parents=True,exist_ok=False)
    run={'schema':'phocus-pixel-shift/run/1','startedAt':datetime.now(timezone.utc).isoformat(),'manifest':str(manifest),'bridge':str(bridge),'bridgeSha256':sha256(bridge),'phocusPath':str(phocus),'groups':[]}
    selected=[g for g in data.get('groups',[]) if g.get('selected')]
    if not selected: raise SystemExit('Manifest has no selected 4/6/16-frame groups.')
    for group in selected:
        frames=int(group['frames']); gd=out/group['id']; gd.mkdir()
        inputs=[Path(f['path']).resolve() for f in group['files']]
        for p in inputs:
            if not p.is_file(): raise SystemExit(f'Missing input: {p}')
        ext='.fff' if frames in (4,6) else '.rgb16'
        merged=gd/f'native-{frames}{ext}'
        if merged.exists(): raise SystemExit(f'Refusing to overwrite {merged}')
        env=dict(os.environ,PHOCUS_PROBE_LABEL=group['id'])
        if args.native_tiff:
            env.update(PHOCUS_CALIBRATED_PROBE='1',PHOCUS_RETAIN_NATIVE_TIFF='1',PHOCUS_USE_NATIVE_FILE_WRITER='1',PHOCUS_ALLOW_NATIVE_64BIT_REOPEN='1')
            env['PHOCUS_ROUNDTRIP_FILE']=str(gd/f'native-{frames}-roundtrip.fff')
            env['PHOCUS_NATIVE_TIFF_FILE']=str(gd/f'native-{frames}.tif')
        cmd=[str(bridge),str(frames),str(merged),*(str(p) for p in inputs)]
        started=time.monotonic(); proc=subprocess.run(cmd,capture_output=True,text=True,env=env); elapsed=time.monotonic()-started
        (gd/'stdout.log').write_text(proc.stdout); (gd/'stderr.log').write_text(proc.stderr)
        record={'id':group['id'],'frames':frames,'command':cmd,'elapsedSeconds':elapsed,'exitCode':proc.returncode,'inputs':[{'path':str(p),'sha256':sha256(p),'bytes':p.stat().st_size} for p in inputs], 'output':str(merged) if merged.exists() else None}
        if merged.exists(): record['outputInfo']={'bytes':merged.stat().st_size,'sha256':sha256(merged)}
        tiff=gd/f'native-{frames}.tif'
        if tiff.exists(): record['nativeTiff']={'path':str(tiff),'bytes':tiff.stat().st_size,'sha256':sha256(tiff)}
        (gd/'run.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n'); run['groups'].append(record)
        if proc.returncode!=0: raise SystemExit(f'Native bridge failed for {group["id"]}; see {gd}/stderr.log')
    run['finishedAt']=datetime.now(timezone.utc).isoformat(); (out/'run.json').write_text(json.dumps(run,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'output':str(out),'groups':[(g['id'],g['frames'],g['exitCode']) for g in run['groups']]},ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
