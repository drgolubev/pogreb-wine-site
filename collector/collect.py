"""Сборщик контактов архитектурных бюро: сайты из списка + сайты из поиска.
Читает collector/input.json, пишет out.json."""
import json, re, sys, time, html
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import requests
import urllib3

urllib3.disable_warnings()
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
      'Accept-Language': 'ru-RU,ru;q=0.9'}
EMAIL = re.compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,10}', re.I)
BAD = re.compile(r'\.(png|jpe?g|gif|webp|svg|css|js|woff2?)$|example\.|sentry|wixpress|@2x|domain\.|yourmail|youremail|mail@mail|test@|noreply|no-reply|@sentry|user@|name@|email@email|ivanov@|privacy@|abuse@|webmaster@', re.I)
CONTACT = re.compile(r'contact|kontakt|контакт|about|o-nas|onas|o-studii|o-byuro|studio|team|komanda|o_nas', re.I)
SKIP_DOMAINS = re.compile(r'(zoon|2gis|yandex|google|avito|profi|houzz|vk\.com|ok\.ru|hh\.ru|youtube|wikipedia|vc\.ru|dzen|pinterest|instagram|facebook|t\.me|telegram|tenchat|rbc|kp\.ru|sostav|workspace|ruward|behance|livemaster|ozon|wildberries|duckduckgo|bing|mail\.ru|rambler|otzovik|irecommend|flamp|spr\.ru|rusprofile|list-org|checko|habr|pikabu|archi\.ru|archdaily|ivd\.ru|inmyroom|forumhouse|cian|domclick|tinkoff|tbank|sberbank|gosuslugi|skillbox|netology|geekbrains|youdo|remontnik|houzzy|dtf)\.', re.I)


def get(url, timeout=15):
    for verify in (True, False):
        try:
            r = requests.get(url, headers=UA, timeout=timeout, verify=verify, allow_redirects=True)
            if r.status_code < 400:
                r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == 'iso-8859-1' else r.encoding
                return r.url, r.text[:1500000]
            return r.url, ''
        except requests.exceptions.SSLError:
            continue
        except Exception:
            return url, ''
    return url, ''


def cf_decode(h):
    out = []
    for m in re.finditer(r'data-cfemail="([0-9a-f]+)"', h):
        s = m.group(1)
        k = int(s[:2], 16)
        out.append(''.join(chr(int(s[i:i + 2], 16) ^ k) for i in range(2, len(s), 2)))
    return out


def emails_of(h):
    t = html.unescape(h).replace('[at]', '@').replace('(at)', '@').replace(' собака ', '@')
    found = []
    for e in EMAIL.findall(t) + cf_decode(h):
        e = e.lower().strip('.')
        if not BAD.search(e) and e not in found:
            found.append(e)
    return found


def site(entry):
    raw = entry['site'].strip()
    if not raw.startswith('http'):
        raw = 'https://' + raw
    final, home = get(raw)
    if not home and raw.startswith('https://'):
        final, home = get('http://' + raw[8:])
    p = urlparse(final)
    origin = f'{p.scheme}://{p.netloc}'
    title = ''
    m = re.search(r'<title[^>]*>(.*?)</title>', home, re.I | re.S)
    if m:
        title = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()[:150]
    desc = ''
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', home, re.I)
    if m:
        desc = html.unescape(m.group(1)).strip()[:250]
    ems = emails_of(home)
    links = []
    for href in re.findall(r'href=["\']([^"\'#]+)["\']', home, re.I):
        u = urljoin(origin + '/', href)
        if urlparse(u).netloc == p.netloc and CONTACT.search(href) and u not in links:
            links.append(u)
    for path in ('/contacts', '/kontakty', '/contact', '/contacts/'):
        u = origin + path
        if u not in links:
            links.append(u)
    for u in links[:6]:
        if len(ems) >= 4:
            break
        _, h = get(u, timeout=12)
        for e in emails_of(h):
            if e not in ems:
                ems.append(e)
    tg = sorted(set(re.findall(r'https?://t\.me/([A-Za-z0-9_]{4,})', home)))[:3]
    return {**entry, 'site': origin, 'ok': bool(home), 'title': title, 'desc': desc,
            'emails': ems[:6], 'telegram': tg}



def main():
    cfg = json.load(open('collector/input.json', encoding='utf-8'))
    entries = list(cfg.get('sites', []))
    seen = {e['site'].lower().replace('https://', '').replace('http://', '').replace('www.', '').strip('/') for e in entries}
    log = []
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(site, entries))
    json.dump({'log': log, 'items': res}, open('out.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('sites', len(res), 'with email', sum(1 for r in res if r['emails']), 'queries', log)


if __name__ == '__main__':
    main()
