"""Проверка базы: сайт жив, свежий год на сайте, ИНН/ОГРН, MX у почты."""
import json, re, html
from concurrent.futures import ThreadPoolExecutor
import requests, urllib3, dns.resolver
urllib3.disable_warnings()
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36', 'Accept-Language': 'ru-RU,ru;q=0.9'}
PARKED = re.compile(r'domain is for sale|домен продается|домен продаётся|this domain|parked|reg\.ru/domain|сайт заблокирован|account suspended|срок регистрации', re.I)

def get(url):
    for v in (True, False):
        try:
            r = requests.get(url, headers=UA, timeout=15, verify=v)
            r.encoding = r.apparent_encoding if (r.encoding or '').lower() in ('', 'iso-8859-1') else r.encoding
            return r.status_code, r.url, r.text[:1500000]
        except requests.exceptions.SSLError:
            continue
        except Exception as e:
            return 0, url, ''
    return 0, url, ''

def mx(domain):
    try:
        return len(dns.resolver.resolve(domain, 'MX', lifetime=10)) > 0
    except Exception:
        try:
            dns.resolver.resolve(domain, 'A', lifetime=10); return None
        except Exception:
            return False

def one(e):
    site = e['site'] if e['site'].startswith('http') else 'https://' + e['site']
    code, final, h = get(site)
    t = html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S | re.I))
    years = [int(y) for y in re.findall(r'(?<!\d)(20[12]\d)(?!\d)', t)]
    yrs = [y for y in years if y <= 2026]
    inn = bool(re.search(r'ИНН\s*:?\s*\d{10,12}|ОГРН(ИП)?\s*:?\s*\d{13,15}', t))
    dom = e['email'].split('@')[1]
    return {**e, 'http': code, 'final': final, 'parked': bool(PARKED.search(t[:20000])), 'max_year': max(yrs) if yrs else None, 'inn': inn, 'mx': mx(dom), 'size': len(h)}

cfg = json.load(open('collector/input.json', encoding='utf-8'))
with ThreadPoolExecutor(12) as ex:
    res = list(ex.map(one, cfg['rows']))
json.dump({'items': res}, open('out.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('checked', len(res))
