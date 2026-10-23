from pathlib import Path
import json,base64
root=Path(__file__).resolve().parent.parent
files={}
for p in (root/'content').iterdir():
 if p.is_file() and p.suffix in ['.html','.js','.css','.json']:files['/'+p.name]=[p.read_text(),{'html':'text/html; charset=utf-8','js':'text/javascript; charset=utf-8','css':'text/css; charset=utf-8','json':'application/json'}[p.suffix[1:]],False]
for p in (root/'assets').iterdir():
 files['/assets/'+p.name]=[base64.b64encode(p.read_bytes()).decode(),'image/jpeg',True]
text='const FILES='+json.dumps(files)+';\nconst CATALOG='+ (root/'content/catalog.json').read_text()+';\n'+(root/'content/server.js.txt').read_text()
(root/'worker').mkdir(exist_ok=True)
(root/'worker/index.js').write_text(text)
