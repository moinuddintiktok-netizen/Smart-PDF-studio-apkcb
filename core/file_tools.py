from pathlib import Path
import hashlib, os, shutil, tempfile


def _human(n):
    for u in ['B','KB','MB','GB','TB']:
        if n < 1024: return f'{n:.1f} {u}'
        n /= 1024
    return f'{n:.1f} PB'


def disk_overview(path=None):
    path = path or str(Path.home())
    total, used, free = shutil.disk_usage(path)
    return {'total':total,'used':used,'free':free,'total_human':_human(total),'used_human':_human(used),'free_human':_human(free)}


def scan_temp_files():
    roots=[tempfile.gettempdir()]
    result=[]
    for root in roots:
        for base, dirs, files in os.walk(root):
            for name in files:
                try: result.append(os.path.join(base,name))
                except Exception: pass
    return result


def _hash(path, chunk=1024*1024):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()


def duplicate_files(folder):
    by_size={}
    for p in Path(folder).rglob('*'):
        if p.is_file():
            try: by_size.setdefault(p.stat().st_size,[]).append(p)
            except OSError: pass
    groups=[]
    for size, paths in by_size.items():
        if len(paths)<2: continue
        hashes={}
        for p in paths:
            try: hashes.setdefault(_hash(p),[]).append(str(p))
            except OSError: pass
        groups.extend([v for v in hashes.values() if len(v)>1])
    return groups


def organize_files(folder):
    root=Path(folder); moved=0
    for p in list(root.iterdir()):
        if not p.is_file(): continue
        ext=p.suffix.lower().lstrip('.') or 'no_extension'
        target=root/ext
        target.mkdir(exist_ok=True)
        dest=target/p.name
        if dest.exists():
            stem, suffix=p.stem,p.suffix; i=1
            while (target/f'{stem}_{i}{suffix}').exists(): i+=1
            dest=target/f'{stem}_{i}{suffix}'
        try: shutil.move(str(p),str(dest)); moved+=1
        except OSError: pass
    return moved
