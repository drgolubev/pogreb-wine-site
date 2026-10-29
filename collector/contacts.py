"""Телефоны, WhatsApp и Telegram с сайтов бюро."""
import json, re, html
from urllib.parse import urljoin, urlparse, unquote
from concurrent.futures import ThreadPoolExecutor
import requests, urllib3
urllib3.disable_warnings()
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36', 'Accept-Language': 'ru-RU,ru;q=0.9'}
CONTACT = re.compile(r'contact|kontakt|контакт|about|o-nas|onas|o-studii|o-byuro', re.I)
def get(u):
    for v in (True, False):
        try:
            r = requests.get(u, headers=UA, timeout=15, verify=v)
            r.encoding = r.apparent_encoding if (r.encoding or '').lower() in ('', 'iso-8859-1') else r.encoding
            return r.url, r.text[:1500000] if r.status_code < 400 else ''
        except requests.exceptions.SSLError:
            continue
        except Exception:
            return u, ''
    return u, ''
def norm(p):
    d = re.sub(r'\D', '', p)
    if len(d) == 11 and d[0] in '78': d = '7' + d[1:]
    elif len(d) == 10 and d[0] == '9': d = '7' + d
    return d if len(d) == 11 and d[0] == '7' else ''
def scan(h):
    t = html.unescape(unquote(h))
    phones = [norm(x) for x in re.findall(r'tel:\s*([+\d()\-\s]{10,20})', t)]
    phones += [norm(x) for x in re.findall(r'(?<![\d])(?:\+7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?![\d])', t)]
    wa = [norm(x) for x in re.findall(r'(?:wa\.me/|api\.whatsapp\.com/send\?phone=|whatsapp://send\?phone=)\+?(\d{10,13})', t)]
    tg = [x for x in re.findall(r'(?:t\.me|telegram\.me)/([A-Za-z][A-Za-z0-9_]{3,31})', t) if x.lower() not in ('share', 'joinchat', 'iv', 's', 'addstickers', 'proxy', 'c')]
    return phones, wa, tg
def one(e):
    site = e['site'] if e['site'].startswith('http') else 'https://' + e['site']
    final, h = get(site)
    p = urlparse(final); origin = f'{p.scheme}://{p.netloc}'
    P, W, T = scan(h)
    links = []
    for href in re.findall(r'href=["\']([^"\'#]+)["\']', h, re.I):
        u = urljoin(origin + '/', href)
        if urlparse(u).netloc == p.netloc and CONTACT.search(href) and u not in links: links.append(u)
    for path in ('/contacts', '/kontakty', '/contact'):
        if origin + path not in links: links.append(origin + path)
    for u in links[:4]:
        _, hh = get(u); a, b, c = scan(hh); P += a; W += b; T += c
    uniq = lambda xs: [x for i, x in enumerate(xs) if x and x not in xs[:i]]
    P, W, T = uniq(P)[:4], uniq(W)[:2], uniq(T)[:3]
    return {**e, 'phones': P, 'whatsapp': W, 'telegram': T}
cfg = json.load(open('collector/input.json', encoding='utf-8'))
with ThreadPoolExecutor(12) as ex: res = list(ex.map(one, cfg['rows']))
json.dump({'items': res}, open('out.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done', len(res), 'phones', sum(1 for r in res if r['phones']), 'wa', sum(1 for r in res if r['whatsapp']), 'tg', sum(1 for r in res if r['telegram']))
