import subprocess,os,json,re
from pathlib import Path
plan=json.loads(Path('.release-public-cache/plan.json').read_text())
ref=os.environ['GITHUB_REF'];assert ref=='refs/heads/chore/v4-website-media-cache'
def git(*args,input=None):return subprocess.check_output(['git',*args],input=input).decode().strip()
for e in plan['shared']:
 assert re.fullmatch('[0-9a-f]{40}',e['sha'])
 assert git('rev-parse',plan['sourceApp']+':'+e['sourcePath'])==e['sha']
 assert git('cat-file','-t',e['sha'])=='blob' and int(git('cat-file','-s',e['sha']))==e['size']
 git('update-index','--add','--cacheinfo','100644',e['sha'],'.release-public-cache/objects/'+e['sha'])
receipt=json.dumps({'count':len(plan['shared']),'sourceApp':plan['sourceApp'],'blobs':[e['sha'] for e in plan['shared']]},indent=2).encode()
sha=git('hash-object','-w','--stdin',input=receipt);git('update-index','--add','--cacheinfo','100644',sha,'.release-public-cache/complete.json')
git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
tree=git('write-tree');commit=git('commit-tree',tree,'-p','HEAD',input='chore(发布): 暂存4.0已公开的官网素材 [skip ci]\n'.encode())
subprocess.run(['git','push','origin',commit+':'+ref],check=True)
print('VERIFIED PUBLIC ASSET CACHE',len(plan['shared']),commit)
