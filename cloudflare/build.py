from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
source=(root/'worker/index.js').read_text()
prefix=source.split('const ownerEmail=')[0]
backend=(root/'cloudflare/server.js.txt').read_text()
(root/'cloudflare/worker.js').write_text(prefix+backend)
(root/'cloudflare/wrangler.jsonc').write_text(json.dumps({'name':'tempahan-mpc-nro','main':'worker.js','compatibility_date':'2026-10-20','compatibility_flags':['nodejs_compat'],'workers_dev':True,'observability':{'enabled':True}},indent=2))
