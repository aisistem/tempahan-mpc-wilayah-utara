import json,random,calendar,collections
from datetime import date,timedelta
from pathlib import Path
random.seed(20260106)
root=Path(__file__).resolve().parent.parent
catalog={x['id']:x for x in json.loads((root/'content/catalog.json').read_text())}
counts={'produktiviti':92,'kualiti':66,'team':18,'six':14,'multimedia':10,'dayasaing':8,'makanac':5,'makanterbuka':4,'lelaki':6,'perempuan':5,'vip':3}
main=[k for k,n in counts.items() for _ in range(n)];random.shuffle(main)
apps=[];records=[]
def item(fid,app,day,status,paid):
 f=catalog[fid];night='night' in f;qty=random.randint(2,8) if fid in ['lelaki','perempuan'] else 1
 duration=random.choice([1,1,1,2,2,3])
 if day.month==6:duration=min(duration,31-day.day)
 if night:package='night';unit=f['night'];extra=prep=0
 else:
  package='half' if f.get('half') and random.random()<.45 else 'day'
  unit=f['half'] if package=='half' else f['day'];extra=random.choice([0,0,1,2]) if package=='half' and f.get('extra') else 0;prep=random.choice([0,0,1]) if f.get('prep') else 0
 end=day+timedelta(days=duration if night else duration-1)
 amount=duration*qty*(unit+extra*f.get('extra',0))+prep*f.get('prep',0)
 return {'id':app+'-'+str(len(records)+1),'application':app,'facility':fid,'start':str(day),'end':str(end),'month':day.month,'duration':duration,'quantity':qty,'package':package,'rate':unit,'extraHours':extra,'prepHours':prep,'amount':amount,'received':amount if paid else 0,'status':status,'payment':'Dibayar' if paid else 'Tidak berkenaan' if status=='Dibatalkan' else 'Belum dibayar'}
for i,fid in enumerate(main):
 app=f'NRO-2026-{i+1:04d}';month=random.choices(range(1,7),weights=[11,12,14,16,18,20])[0];day=date(2026,month,random.randint(1,25))
 status=random.choices(['Selesai','Disahkan','Dalam proses','Dibatalkan'],weights=[72,12,10,6])[0];paid=status=='Selesai' or (status=='Disahkan' and random.random()<.65)
 apps.append({'id':app,'organisation':f'Organisasi Demo {i+1:03d}'})
 records.append(item(fid,app,day,status,paid))
 if fid in ['produktiviti','kualiti','team','six'] and i%3==0:
  records.append(item('lelaki' if i%2==0 else 'perempuan',app,day,status,paid))
 if fid in ['produktiviti','kualiti'] and i%11==0:
  records.append(item('vip',app,day,status,paid))
data={'isSimulation':True,'period':'Januari–Jun 2026','applications':apps,'items':sorted(records,key=lambda x:(x['start'],x['application']))}
(root/'content/showcase-data.json').write_text(json.dumps(data,ensure_ascii=False))
c=collections.Counter(x['facility'] for x in records)
assert c.most_common(2)==[('produktiviti',92),('kualiti',66)]
assert len({x['application'] for x in records})==len(apps)
assert all(x['start']>='2026-01-01' and x['end']<='2026-06-30' for x in records)
print(json.dumps({'applications':len(apps),'items':len(records),'received':sum(x['received'] for x in records),'top':c.most_common(4)}))
