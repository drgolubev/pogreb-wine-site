import json, re, requests
from urllib.parse import quote_plus
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'ru-RU,ru;q=0.9'}
q='архитектурное бюро проектирование загородных домов Казань'
urls={
 'bing':'https://www.bing.com/search?q='+quote_plus(q)+'&setlang=ru&cc=ru',
 'mojeek':'https://www.mojeek.com/search?q='+quote_plus(q),
 'yahoo':'https://search.yahoo.com/search?p='+quote_plus(q),
 'brave':'https://search.brave.com/search?q='+quote_plus(q),
 'ddg_lite':'https://lite.duckduckgo.com/lite/?q='+quote_plus(q),
 'startpage':'https://www.startpage.com/do/search?q='+quote_plus(q),
 'zoon_kzn':'https://zoon.ru/kazan/building/type/arhitekturnye_byuro/',
 'houzz':'https://www.houzz.ru/professionaly/arkhitektory/c/Kazan',
 'yandex_maps':'https://yandex.ru/maps/43/kazan/search/архитектурное%20бюро/',
 '2gis':'https://2gis.ru/kazan/search/архитектурное%20бюро',
}
out={}
for k,u in urls.items():
    try:
        r=requests.get(u,headers=UA,timeout=20)
        hrefs=re.findall(r'href="(https?://[^"]+)"',r.text)
        doms=sorted({re.sub(r'^www\.','',h.split('/')[2]) for h in hrefs})
        out[k]={'status':r.status_code,'len':len(r.text),'ndoms':len(doms),'sample':doms[:40]}
    except Exception as e:
        out[k]={'err':str(e)[:200]}
json.dump(out,open('out.json','w'),ensure_ascii=False,indent=1)
print({k:(v.get('status'),v.get('ndoms')) for k,v in out.items()})
