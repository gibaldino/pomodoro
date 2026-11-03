import os,json,datetime as dt,urllib.request
from zoneinfo import ZoneInfo
import icalendar, recurring_ical_events
tz=ZoneInfo("America/Sao_Paulo")
cal=icalendar.Calendar.from_ical(urllib.request.urlopen(os.environ["ICAL_URL"]).read())
now=dt.datetime.now(tz); end=now+dt.timedelta(days=7)
out=[]
for ev in recurring_ical_events.of(cal).between(now-dt.timedelta(hours=12),end):
    s=ev.get("DTSTART").dt; e=ev.get("DTEND").dt if ev.get("DTEND") else s
    if not isinstance(s,dt.datetime): continue
    t=str(ev.get("SUMMARY","")).strip()
    if t.startswith("⏱") or "decompress" in t.lower() or str(ev.get("TRANSP",""))=="TRANSPARENT": continue
    s=s.astimezone(tz); e=e.astimezone(tz)
    if e<now: continue
    out.append({"t":t,"s":s.isoformat(),"e":e.isoformat()})
out.sort(key=lambda x:x["s"])
json.dump({"updated":now.isoformat(timespec="seconds"),"events":out},open("events.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(len(out))
