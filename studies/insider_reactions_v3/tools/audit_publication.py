"""Audit explicitly staged publication files without displaying credential-like values."""
import gzip,io,re,subprocess,zipfile
patterns=[rb'gsk_[A-Za-z0-9]{30,}',rb'ghp_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{35,}',rb'AIza[A-Za-z0-9_-]{30,}',rb'sk-proj-[A-Za-z0-9_-]{30,}',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
paths=subprocess.check_output(['git','diff','--cached','--name-only','-z']).split(b'\0');fail=[]
for p in paths:
 if not p:continue
 name=p.decode();data=subprocess.check_output(['git','show',':'+name])
 if len(data)>=95_000_000:fail.append((name,'large blob'))
 if name.endswith('.gz'):
  try:data=gzip.decompress(data)
  except OSError:fail.append((name,'invalid gzip'));continue
 elif name.endswith('.docx'):
  with zipfile.ZipFile(io.BytesIO(data))as z:data=b'\n'.join(z.read(n)for n in z.namelist()if n.endswith('.xml'))
 if any(re.search(pat,data)for pat in patterns):fail.append((name,'credential-like value; inspect privately'))
 if name.endswith('.env')or '/.env' in name:fail.append((name,'environment file'))
if fail:
 for name,reason in fail:print(name,reason)
 raise SystemExit('Publication audit failed; no secret values were printed')
print('Staged publication audit passed for',sum(bool(p)for p in paths),'files')
