import http from 'node:http';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import worker from '../worker/index.js';
await mkdir(new URL('../.sites-runtime/',import.meta.url),{recursive:true});
const localFile=new URL('../.sites-runtime/availability-preview.json',import.meta.url);
const bucket={async get(){try{const s=await readFile(localFile,'utf8');return {etag:JSON.parse(s).revision.toString(),json:async()=>JSON.parse(s)}}catch{return null}},async put(k,s,opt){const old=await this.get();if(opt.onlyIf.etagMatches&&old?.etag!==opt.onlyIf.etagMatches)return null;if(opt.onlyIf.etagDoesNotMatch&&old)return null;await writeFile(localFile,s);return {etag:JSON.parse(s).revision.toString()}}};
const server=http.createServer(async(req,res)=>{const base='http://'+req.headers.host;let body='';for await(const chunk of req)body+=chunk;const headers={...req.headers,'oai-authenticated-user-email':'aisistem@mpc.gov.my'};const r=await worker.fetch(new Request(base+req.url,{method:req.method,headers,body:['GET','HEAD'].includes(req.method)?undefined:body}),{BUCKET:bucket});res.writeHead(r.status,Object.fromEntries(r.headers));res.end(Buffer.from(await r.arrayBuffer()));});server.listen(4173,'127.0.0.1');
