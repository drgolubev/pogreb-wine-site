import json, re, os, sys
BASE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,BASE); from etz_svg import etz_svg
from cases import CASES, case_card, case_url, gallery_figure, case_catalog
SEC_DIR=os.path.join(BASE,'sections')
S={f[:-5]:open(os.path.join(SEC_DIR,f),encoding='utf-8').read() for f in os.listdir(SEC_DIR) if f.endswith('.html')}
D=open(os.path.join(BASE,'diagram.svg'),encoding='utf-8').read()
OUT=os.environ.get('OUT',os.path.join(BASE,'..','dist'))
ARTIFACT=os.environ.get('ARTIFACT')=='1'
os.makedirs(OUT,exist_ok=True)
FONTS='''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Golos+Text:wght@400;500;600&display=swap">
<link rel="stylesheet" href="style.css">'''
NAV=[('about.html','О погребе'),('pogreb.html','Устройство'),('etazherki.html','Этажерки'),('objects.html','Объекты'),('price.html','Стоимость'),('konstruktor.html','Конструктор'),('architects.html','Архитекторам'),('contacts.html','Контакты')]
def header(active):
    links=''.join(f'<a href="{h}"{" class=\"is-active\" aria-current=\"page\"" if h==active else ""}>{n}</a>' for h,n in NAV)
    return f'''<div class="grain" aria-hidden="true"></div>
<header class="site-head" id="top">
  <div class="wrap head-row">
    <a class="brand" href="index.html">ПО<b>G</b>REB WINE</a>
    <nav class="nav" aria-label="Разделы сайта">{links}</nav>
    <div class="head-cta">
      <a class="head-phone" href="tel:+79172057000">+7 917 205-70-00</a>
      <a class="btn btn-wine" href="contacts.html">Рассчитать погреб</a>
      <button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mnav"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-nav" id="mnav">
  <a href="index.html"{' class="is-active"' if active=='index.html' else ''}>Главная</a>{links}
  <div class="m-contacts"><span>Роман Голубев, директор</span><a href="tel:+79172057000">+7 917 205-70-00</a><span>Офис</span><a href="tel:+79271575888">+7 927 157-58-88</a></div>
</div>
'''
CTA='''<section class="cta-strip"><div class="wrap cta-row"><div><span class="kicker">Расчёт стоимости</span><h2>Мы вам перезвоним и расскажем стоимость</h2><p>Оставьте телефон: ответим на вопросы, подскажем, какой погреб подойдёт вашему дому, и назовём цену.</p></div><div class="cta-actions"><a class="btn btn-wine" href="contacts.html">Оставить заявку</a><a class="btn btn-line" href="tel:+79172057000">+7 917 205-70-00</a></div></div></section>
'''
FOOT='''<footer class="foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a class="brand" href="index.html">ПО<b>G</b>REB WINE</a>
      <p>Спиральные винные погреба и автоматические этажерки. По всей России и не только.</p>
    </div>
    <nav class="foot-col" aria-label="Разделы">
      <span class="foot-k">Разделы</span>
      <a href="about.html">О погребе</a><a href="pogreb.html">Устройство</a><a href="etazherki.html">Этажерки</a><a href="objects.html">Объекты</a>
    </nav>
    <nav class="foot-col" aria-label="Ещё">
      <span class="foot-k">Ещё</span>
      <a href="price.html">Стоимость</a><a href="konstruktor.html">Конструктор</a><a href="journal.html">Журнал</a><a href="architects.html">Архитекторам</a>
    </nav>
    <div class="foot-col">
      <span class="foot-k">Контакты</span>
      <a href="tel:+79172057000">+7 917 205-70-00</a><a href="tel:+79271575888">+7 927 157-58-88</a>
      <span>Саратов, ул. Кособокова, 40</span>
      <a href="https://t.me/pogrebwine" target="_blank" rel="noopener">Telegram</a>
    </div>
  </div>
  <div class="wrap foot-bottom"><span>© ПОGREB WINE · ИП Голубев Роман Николаевич · ИНН 645402896405 · ОГРНИП 323645700011801</span><span class="foot-links"><a href="politika.html">Политика конфиденциальности</a><a href="contacts.html">Рассчитать погреб</a></span></div>
</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="app.js"></script>'''
def page_hero(crumb, title, lead, img=None, alt=''):
    bg=f'<div class="hero-bg"><img id="heroImg" src="{img}" alt="{alt}"></div>' if img else ''
    return f'''<section class="page-hero{' has-img' if img else ''}">{bg}<div class="wrap"><div class="crumb"><a href="index.html">Главная</a> / {crumb}</div><h1>{title}</h1><p class="page-lead">{lead}</p></div></section>
'''
def fix(s):
    s=s.replace('href="#contact" data-scroll','href="contacts.html"').replace('href="#cases" data-scroll','href="objects.html"')
    return s
def strip_head(sec):
    # remove the sec-head block (first <div class="sec-head">...</div>\n      </div>) — used when page hero already states it
    return sec
SITE='https://pogreb-wine.ru/'
ORG={"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","@id":SITE+"#org","name":"ПОGREB WINE","alternateName":["Погреб Вайн","Pogreb Wine","ПОГРЕБ WINE","Погреб Wine"],"url":SITE,"logo":SITE+"media/top-hatch.jpg","image":SITE+"media/hatch-open.jpg","description":"Спиральные винные погреба под полом дома со стеклянным автоматическим люком, автоматические винные этажерки. Производство и монтаж по всей России.","telephone":["+7 917 205-70-00","+7 927 157-58-88"],"address":{"@type":"PostalAddress","streetAddress":"ул. Кособокова, 40","addressLocality":"Саратов","addressRegion":"Саратовская область","addressCountry":"RU"},"areaServed":["Москва","Московская область","Санкт-Петербург","Сочи","Калининград","Екатеринбург","Саратов","Россия"],"legalName":"ИП Голубев Роман Николаевич","taxID":"645402896405","founder":{"@type":"Person","name":"Роман Голубев","jobTitle":"Директор"},"sameAs":["https://t.me/pogrebwine"],"priceRange":"от 3 500 000 ₽"}
PAGES=[]
def crumbs_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+(h if h!='index.html' else '')} for i,(h,n) in enumerate(items)]}
def ld_tags(objs):
    return ''.join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>\n' for o in objs)
def doc(fname, title, desc, body, active, first=False, ld=None, img='media/hatch-open.jpg', ogtype='website'):
    url=SITE+('' if fname=='index.html' else fname)
    PAGES.append(fname)
    meta=f'<link rel="canonical" href="{url}">\n<meta property="og:type" content="{ogtype}">\n<meta property="og:site_name" content="ПОGREB WINE">\n<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n<meta property="og:image" content="{SITE}{img}">\n<meta property="og:locale" content="ru_RU">\n'
    head=f'<title>{title}</title>\n'+('<meta name="claude:viewport-fit-sides" content="cover">\n' if ARTIFACT else '')+f'<meta name="description" content="{desc}">\n{meta}{FONTS}\n'+ld_tags([ORG]+(ld or []))
    inner=head+header(active)+'<main>\n'+body+'</main>\n'+FOOT
    if not (first and ARTIFACT):
        inner='<!doctype html>\n<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'+head+'</head><body>\n'+header(active)+'<main>\n'+body+'</main>\n'+FOOT+'\n</body></html>'
    open(os.path.join(OUT,fname),'w',encoding='utf-8').write(inner)

PROD_LD=[{"@context":"https://schema.org","@type":"Product","name":"Спиральный винный погреб с автоматическим стеклянным люком","brand":{"@type":"Brand","name":"ПОGREB WINE"},"description":"Модульный спиральный погреб глубиной 2–3 м на 800–3 500 бутылок: блоки из бетона М500, мембрана ЭПДМ, дубовые накладки на ступенях, LED-подсветка 24 В, автоматический люк из триплекса до 32 мм.","image":SITE+"media/hatch-open.jpg","offers":{"@type":"AggregateOffer","lowPrice":"3500000","priceCurrency":"RUB","availability":"https://schema.org/InStock","seller":{"@id":SITE+"#org"}}},
 {"@context":"https://schema.org","@type":"Product","name":"Автоматическая винная этажерка, поднимающаяся из пола","brand":{"@type":"Brand","name":"ПОGREB WINE"},"description":"Этажерка из нержавеющей стали с тремя ярусами, Ø250 мм на 12–15 бутылок или Ø400 мм на 15–25 бутылок.","offers":{"@type":"AggregateOffer","lowPrice":"250000","priceCurrency":"RUB","availability":"https://schema.org/InStock","seller":{"@id":SITE+"#org"}}}]
def faq_ld(sec):
    qs=re.findall(r'<summary>(.*?)<i[^>]*></i></summary><div class="ans">(.*?)</div>',sec,flags=re.S)
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q.strip(),"acceptedAnswer":{"@type":"Answer","text":re.sub(r'<[^>]+>',' ',a).strip()}} for q,a in qs]}
# ---------- index ----------
tease='''<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Объекты</span><h2>Погреба, которые уже стоят</h2></div><p>Москва и Подмосковье, Сочи, Санкт-Петербург, Калининград, Екатеринбург, Саратов.</p></div>
  <div class="ogrid ogrid-4">'''+''.join(case_card(x) for x in CASES[:4])+'''</div>
  <div class="case-more"><a class="btn btn-line" href="objects.html">Все объекты</a></div>
</div></section>
'''
arch_short=S['ARCHITECTS'].replace('<section class="band" id="architects">','<section class="band band-short">').replace('href="#contact" data-scroll data-role="architect">Обсудить партнёрство','href="architects.html">Условия для архитекторов')
INSIDE='''<section class="inside" aria-label="Внутри погреба"><div class="inside-media"><video src="media/inside-descent.mp4" poster="media/inside-descent-poster.jpg" muted loop playsinline preload="metadata" aria-label="Спуск по лестнице мимо ниш с вином и шампанским"></video></div><div class="wrap inside-copy"><h2>Ниши для бутылок, ящиков и шампанского по всей спирали</h2><p>Каждая полка под рукой, пока спускаетесь по лестнице.</p></div></section>\n'''
ETZ_TEASE='''<section class="sec" style="padding-top:0"><div class="wrap etz-tease"><div class="etz-pair"><div class="etz-scheme">'''+etz_svg()+'''<span class="etz-cap">Схема</span></div><div class="etz-video"><video src="media/etz-lift.mp4" poster="media/etz-lift-poster.jpg" muted loop playsinline preload="metadata" aria-label="Этажерка из нержавеющей стали поднимается из пола с напитками на трёх ярусах и опускается обратно"></video><span class="etz-cap">Видео</span></div></div><div><span class="kicker">Ещё мы делаем</span><h2>Этажерка, которая поднимается из пола</h2><p class="lid-lead">Три яруса из нержавеющей стали выезжают из пола одним касанием и показывают коллекцию. Ставится в гостиной, винной комнате, ресторане или у зоны барбекю. А в бочке на колёсиках её можно выкатить даже на улицу.</p><div class="hero-actions"><a class="btn btn-line" href="etazherki.html">Подробнее об этажерках</a></div></div></div></section>\n'''
ANAT_IDX=S['ANATOMY'].replace('{{DIAGRAM}}',D).replace(' style="padding-top:0"','')+'<div class="wrap anat-more"><a class="btn btn-line" href="pogreb.html">Подробнее об устройстве</a></div>\n'
KZ_TEASE='''<section class="sec" style="padding-top:0"><div class="wrap kz-tease"><a class="kz-tease-media" href="konstruktor.html" aria-label="Открыть конструктор погреба"><img src="media/kz-preview.jpg" alt="Конструктор погреба: круглый люк открыт, видна винтовая лестница и ниши с вином" loading="lazy"><span class="kz-tease-tag">Онлайн</span></a><div><span class="kicker">Конструктор</span><h2>Соберите свой погреб за пару минут</h2><p class="lid-lead">Выберите форму люка, механизм, цвет стекла, глубину и дерево ступеней. Рисунок меняется вместе с выбором, а люк открывается прямо на экране. Готовую сборку отправьте нам, и мы назовём цену.</p><div class="hero-actions"><a class="btn btn-wine" href="konstruktor.html">Открыть конструктор</a></div></div></div></section>
'''
idx=fix(S['HERO'])+S['IRIS']+S['COMPARE']+ANAT_IDX+INSIDE+tease+KZ_TEASE+ETZ_TEASE+CTA
doc('index.html','ПОGREB WINE','Спиральные винные погреба под полом дома со стеклянным автоматическим люком. От 3,5 млн ₽, 800–3 500 бутылок, монтаж до 10 дней.',idx,'index.html',first=True,ld=PROD_LD)

# ---------- pogreb ----------
LIFT='''<section class="sec" style="padding-top:0"><div class="wrap lift">
  <div><span class="kicker">Прямоугольный люк</span><h2>Створка поднимается, внизу загорается свет</h2><p class="lid-lead">Так открывается прямоугольный люк в частном доме. Стекло лежит заподлицо с плиткой, а на приводе поднимается целиком. Форму и размер люка подбираем под пол и интерьер.</p></div>
  <div class="lift-media"><video src="media/hatch-lift.mp4" poster="media/hatch-lift-poster.jpg" muted loop playsinline preload="metadata" aria-label="Прямоугольный стеклянный люк поднимается на приводе, под ним включается тёплая подсветка"></video></div>
</div></section>
'''

anat=S['ANATOMY'].replace('{{DIAGRAM}}',D).replace(' style="padding-top:0"','')
p=page_hero('Устройство','Как устроен спиральный погреб','Бетонные блоки, мембрана, винтовая лестница, свет и стеклянный люк. Разбираем по частям, из чего состоит погреб и почему ему не нужно электричество.','media/top-hatch.jpg','Вид сверху сквозь стеклянный люк на лестницу погреба')
p+=anat+S['LID']+LIFT+INSIDE.replace('Ниши для бутылок, ящиков и шампанского по всей спирали','Так выглядит спуск в погреб')+S['FAQ']+CTA
doc('pogreb.html','Устройство, ПОGREB WINE','Устройство спирального винного погреба: люк, лестница, блоки М500, мембрана ЭПДМ, кессон, вентиляция, подсветка.',p,'pogreb.html',ld=[faq_ld(S['FAQ']),crumbs_ld([('index.html','Главная'),('pogreb.html','Устройство')])],img='media/top-hatch.jpg')

# ---------- about ----------
ab=page_hero('О погребе','Место, где вино ждёт своего часа','Спиральный погреб под полом дома: идея из Франции 1977 года, модульные блоки из камня и наш автоматический люк. Рассказываем, что это и почему так вино хранится лучше всего.','media/spiral-close.jpg','Винтовая лестница погреба сверху, ниши с бутылками по всей высоте')
ab+='''<section class="sec" style="padding-top:0"><div class="wrap about-intro">
  <div><span class="kicker">Что это такое</span><h2>Погреб из камня, лестница и ваша коллекция вокруг неё</h2></div>
  <div class="about-text">
    <p>Спиральный погреб уходит под пол на 2–3 метра. Его стены собраны из модульных блоков, внутри идёт винтовая лестница, а по стенам вдоль всей спирали расположены ниши для бутылок, ящиков и шампанского. Сверху погреб закрыт стеклянным люком, который выглядит как часть пола гостиной, кухни или террасы.</p>
    <p>Касание кнопки, и люк плавно открывается. Вы спускаетесь по винтовой лестнице, а бутылки всё время под рукой. Погреб можно поставить при строительстве или в уже готовый дом, и он не отнимает ни метра площади комнаты.</p>
    <p>Мы не просто строим погреба. Каждый проект подбираем под дом, интерьер и коллекцию владельца: форму, глубину, отделку ступеней, бары, свет и способ открывания люка.</p>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">История</span><h2>От римского акведука до вашей гостиной</h2></div><p>Идея спирального погреба появилась почти полвека назад и с тех пор почти не изменилась. Изменились материалы и техника.</p></div>
  <ol class="timeline">
    <li><span class="tl-y">Древний Рим</span><div><h3>Лестница в подвал акведука</h3><p>Винтовая лестница, уходящая в прохладный подвал древнеримского акведука, стала прообразом погреба.</p></div></li>
    <li><span class="tl-y">1977</span><div><h3>Первый погреб во Франции</h3><p>Француз Жорж Арнуа увидел эту лестницу и решил повторить её у себя дома. Он вырыл яму диаметром 2 метра, обложил её кирпичом, поставил деревянную винтовую лестницу и полки для бутылок.</p></div></li>
    <li><span class="tl-y">Позже</span><div><h3>Камень вместо дерева</h3><p>Недолговечные деревянные конструкции заменили модульными блоками из искусственного камня. Так появились спиральные погреба, которые разошлись по Европе.</p></div></li>
    <li><span class="tl-y">Сегодня</span><div><h3>ПОGREB WINE</h3><p>Мы ставим спиральные погреба по всей России, сами делаем автоматические стеклянные люки и выдвижные этажерки. В 2024 году показывали люк на выставке «Виноиндустрия» в Санкт-Петербурге.</p></div></li>
  </ol>
</div></section>
<section class="inside" aria-label="Внутри погреба"><div class="inside-media"><video src="media/inside-pan.mp4" poster="media/inside-pan-poster.jpg" muted loop playsinline preload="metadata" aria-label="Ниши с бутылками и ящиками внутри погреба"></video></div><div class="wrap inside-copy"><h2>Почему земля хранит вино лучше любого шкафа</h2><p>На глубине грунт держит ровную температуру круглый год, без скачков и без электричества. Внизу прохладнее, наверху теплее, поэтому белые и игристые вина лежат ниже, а красные выше. В погребе темно, тихо и нет вибраций, которые мешают вину созревать.</p></div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Материалы</span><h2>Из чего мы делаем погреб</h2></div><p>Всё, что видно глазу, и всё, что спрятано в земле.</p></div>
  <div class="mat">
    <div><h3>Модульные блоки</h3><p>Бетон класса М500 с пластификаторами и фиброволокном. Держит нагрузку грунта, не боится влаги и служит практически без срока.</p></div>
    <div><h3>Мембрана ЭПДМ</h3><p>Прорезиненный герметичный карман толщиной 1,5 мм снаружи погреба. При высоких грунтовых водах добавляем бетонный кессон.</p></div>
    <div><h3>Натуральный дуб и кожа</h3><p>Ступени, пол и бары отделываем натуральным дубом. По желанию на ступени ставим кожаные накладки.</p></div>
    <div><h3>Сталь и триплекс</h3><p>Рама люка из нержавеющей стали и закалённое стекло триплекс толщиной до 32 мм, по которому можно ходить.</p></div>
    <div><h3>Свет</h3><p>Светодиодная подсветка 24 В, 4000 К по окружности пола и люка, а также в барах. Показывает этикетки и не греет вино.</p></div>
    <div><h3>Автоматика</h3><p>Привод люка 24 В, сенсорная кнопка или отпечаток пальца, подключение к умному дому и Алисе.</p></div>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Выставки</span><h2>Виноиндустрия 2024, Санкт-Петербург</h2></div><p>Главным на стенде был наш автоматический стеклянный люк: гости открывали его касанием и смотрели, как работает механизм. Под стеклом мы положили фото погреба, чтобы было видно, как люк выглядит над настоящей лестницей. Рядом стояла этажерка.</p></div>
  <div class="expo">
    <figure class="expo-v"><video src="media/expo.mp4" poster="media/expo-poster.jpg" muted loop playsinline preload="metadata" aria-label="Стенд ПОGREB WINE на выставке, автоматический стеклянный люк"></video></figure>
    <figure class="expo-w"><img src="media/expo-stand.jpg" alt="Стенд ПОGREB WINE на выставке Виноиндустрия 2024"><figcaption>Стенд с автоматическим люком</figcaption></figure>
    <figure class="expo-v"><img src="media/expo-bar.jpg" alt="Этажерка и витрина на стенде ПОGREB WINE"><figcaption>Этажерка и витрина</figcaption></figure>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap about-co">
  <div class="about-co-media"><img src="media/descent.jpg" alt="Гостья спускается по винтовой лестнице погреба"></div>
  <div>
    <span class="kicker">О компании</span>
    <h2>Вековые традиции и современная инженерия</h2>
    <p class="lid-lead">ПОGREB WINE работает из Саратова и ставит погреба по всей стране: Москва и Подмосковье, Санкт-Петербург, Сочи, Калининград, Екатеринбург. Люки делаем на собственном производстве и сами везём их на объект на специальном прицепе. Монтаж ведёт наша команда.</p>
    <p class="lid-lead" style="margin-top:16px">Каждый погреб для нас отдельный проект, сделанный с заботой о коллекции и вниманием к образу жизни владельца. Мы уверены, что хорошее вино заслуживает лучшего места.</p>
    <div class="hero-actions"><a class="btn btn-wine" href="contacts.html">Обсудить ваш погреб</a><a class="btn btn-line" href="objects.html">Смотреть объекты</a></div>
  </div>
</div></section>
'''+CTA
doc('about.html','О погребе, ПОGREB WINE','Что такое спиральный винный погреб, история идеи с 1977 года, материалы и компания ПОGREB WINE.',ab,'about.html',ld=[crumbs_ld([('index.html','Главная'),('about.html','О погребе')])])

# ---------- etazherki ----------
e=page_hero('Этажерки','Этажерка, которая поднимается из пола','Автоматическая винная этажерка из нержавеющей стали. Закрытая, она почти не видна в полу, а по касанию поднимается и плавно вращается, показывая бутылки.',None)
e+='''<section class="sec" style="padding-top:0"><div class="wrap lid lid-etz">
  <div class="etz-pair"><div class="etz-scheme">'''+etz_svg()+'''<span class="etz-cap">Схема</span></div><div class="etz-video"><video src="media/etz-lift.mp4" poster="media/etz-lift-poster.jpg" muted loop playsinline preload="metadata" aria-label="Этажерка из нержавеющей стали поднимается из пола с напитками на трёх ярусах и опускается обратно"></video><span class="etz-cap">Видео</span></div></div>
  <div>
    <span class="kicker">Как это работает</span>
    <h2>Три яруса, бесшумный ход и плавное вращение</h2>
    <p class="lid-lead">Механизм спрятан в полу. По касанию этажерка выезжает вверх, ярусы вращаются, и любая бутылка оказывается под рукой. Корпус из нержавеющей стали не боится влаги винной комнаты и служит долго.</p>
    <dl class="specs">
      <div><dt>Ø 250 мм, 3 полки</dt><dd>от 12 до 15 бутылок</dd></div>
      <div><dt>Ø 400 мм, 3 полки</dt><dd>от 15 до 25 бутылок</dd></div>
      <div><dt>Материал</dt><dd>нержавеющая сталь</dd></div>
      <div><dt>Ход</dt><dd>автоматический, бесшумный</dd></div>
      <div><dt>Посадочные места</dt><dd>под классические и бургундские бутылки, магнумы</dd></div>
      <div><dt>Стоимость</dt><dd>от 250 000 ₽</dd></div>
    </dl>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Где ставят</span><h2>В доме, в ресторане и на участке</h2></div><p>Вместимость зависит от формы и объёма бутылок. Посадочные места подгоняем под вашу коллекцию.</p></div>
  <div class="why-arch">
    <div><h3>Гостиная и винная комната</h3><p>Этажерка выезжает из пола рядом с диваном или баром и становится центральным предметом комнаты.</p></div>
    <div><h3>Ресторан и бар</h3><p>Динамичная витрина для дорогих позиций: гости видят, как бутылки поднимаются к столу.</p></div>
    <div><h3>Терраса и зона барбекю</h3><p>Корпус герметичный, поэтому этажерку ставят и на участке. Напитки остаются прохладными за счёт грунта.</p></div>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="barrel">
    <div class="barrel-text">
      <span class="kicker">Этажерка в бочке</span>
      <h2>Выкатили на террасу, нажали, и бар готов</h2>
      <p class="lid-lead">Та же автоматическая этажерка, только встроена в стальную бочку. Пол вскрывать не нужно: бочка стоит на колёсиках, её можно выкатить на террасу, к бассейну, в беседку или в бар и поставить там, где сейчас нужнее.</p>
      <ul class="barrel-list">
        <li><b>Поднимается из бочки</b> вместе с деревянной столешницей, внутри горит подсветка</li>
        <li><b>На колёсиках</b>: катается по дому и участку, ставится на улице</li>
        <li><b>Те же параметры</b>, что у встроенной этажерки: Ø 250 или 400 мм, от 12 до 25 бутылок</li>
        <li><b>Для вина, пива и напитков</b>: на вечеринке, в баре, в зоне барбекю</li>
      </ul>
      <div class="hero-actions"><a class="btn btn-wine" href="contacts.html">Узнать цену бочки</a></div>
    </div>
    <div class="barrel-media">
      <figure><video src="media/etz-barrel-night.mp4" poster="media/etz-barrel-night-poster.jpg" muted loop playsinline preload="metadata" aria-label="Этажерка поднимается из чёрной бочки на летней веранде ресторана вечером"></video><figcaption>Летняя веранда ресторана, вечер</figcaption></figure>
      <figure><video src="media/etz-barrel.mp4" poster="media/etz-barrel-poster.jpg" muted loop playsinline preload="metadata" aria-label="Бочка с деревянной столешницей, из неё поднимается этажерка с напитками"></video><figcaption>В комнате отдыха</figcaption></figure>
    </div>
  </div>
</div></section>
'''+CTA
doc('etazherki.html','Этажерки, ПОGREB WINE','Автоматическая винная этажерка из нержавеющей стали, которая поднимается из пола: Ø250 мм на 12–15 бутылок, Ø400 мм на 15–25 бутылок, от 250 000 ₽.',e,'etazherki.html',ld=[PROD_LD[1],crumbs_ld([('index.html','Главная'),('etazherki.html','Этажерки')])])

# ---------- objects ----------
o=page_hero('Объекты','Погреба, которые уже стоят','Рестораны, частные дома и виллы от Калининграда до Сочи. У каждого объекта своя страница с фото и видео: как ставили и что получилось.','media/hall-hatch.jpg','Люк погреба в зале ресторана Панинотека')
o+='<section class="sec" style="padding-top:0"><div class="wrap">'+case_catalog(CASES)+'</div></section>\n'
o+='''<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="geo">
    <h4>Где стоят наши погреба</h4>
    <div>
      <ul class="cities"><li>Москва</li><li>Подмосковье</li><li>Санкт-Петербург</li><li>Сочи</li><li>Калининград</li><li>Екатеринбург</li><li>Саратов</li></ul>
    </div>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">На стройке</span><h2>Как это выглядит до отделки</h2></div><p>Котлован, модульные блоки, лестница, рама люка и стекло. Так погреб выглядит, пока его не закрыли полом.</p></div>
  <div class="strip" id="strip2" tabindex="0" aria-label="Фото со стройки, листайте в сторону">
'''+''.join('    '+gallery_figure(f,cap)+'\n' for f,cap in [
  ('media/ostr-2.jpg','Бетонный котлован, Подмосковье'),
  ('media/kld-1.jpg','Блоки в котловане, Калининград'),
  ('media/kh-st1.jpg','Блоки в мембране, Хоста'),
  ('media/ostr-3.jpg','Блоки и лестница, Подмосковье'),
  ('media/kh-st2.jpg','Лестница до отделки, Хоста'),
  ('media/ekb-1.jpg','Рама люка, Екатеринбург'),
  ('media/kaliningrad-mount.jpg','Рама люка, Калининград'),
  ('media/kh-st3.jpg','Выставляем ряд по уровню, Хоста'),
  ('media/mount-glass.jpg','Ставим стекло люка, Подмосковье'),
  ('media/ostr-4.jpg','Стекло в черновом полу, Подмосковье'),
])+'''  </div>
</div></section>
'''+CTA
doc('objects.html','Объекты, ПОGREB WINE','Реализованные винные погреба: Панинотека в Можайске, вилла в Хосте, Калининград, Екатеринбург, Подмосковье. Фото и видео монтажа.',o,'objects.html',ld=[crumbs_ld([('index.html','Главная'),('objects.html','Объекты')])])

# ---------- price ----------
pk=re.sub(r'\s*<div class="sec-head">.*?</p>\s*</div>\s*\n','\n',S['PACKAGE'],count=1,flags=re.S).replace(' class="sec" id="pack"',' class="sec" id="pack" style="padding-top:0"')
pr=page_hero('Стоимость','Погреб от 3,5 млн ₽','Итоговая цена зависит от места установки, глубины, отделки и инженерии. Ниже что входит в базовую цену и что добавляется по проекту. Точную сумму считаем после замера.')
pr+=pk+S['PROCESS']+CTA
doc('price.html','Стоимость, ПОGREB WINE','Стоимость винного погреба: базовая комплектация от 3,5 млн ₽, опции, этажерка Beerlift от 250 000 ₽, сроки изготовления и монтажа.',pr,'price.html',ld=PROD_LD+[crumbs_ld([('index.html','Главная'),('price.html','Стоимость')])])

# ---------- architects ----------
band=S['ARCHITECTS'].replace('href="#contact" data-scroll data-role="architect"','href="#arch-form" data-scroll')
why='''<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Почему клиенты соглашаются</span><h2>Погреб, который продаёт ваш проект</h2></div><p>Стеклянный люк в полу запоминается сильнее любой отделки. Это деталь, ради которой клиент показывает дом гостям.</p></div>
  <div class="why-arch">
    <div><h3>Не отнимает площадь</h3><p>Погреб уходит под пол. Комната остаётся такой, как вы её задумали, люк становится частью рисунка пола.</p></div>
    <div><h3>Ставится и в готовый дом</h3><p>Если клиент уже живёт в доме, погреб всё равно можно поставить: вскрываем перекрытие, монтаж до 10 дней.</p></div>
    <div><h3>Без сложной инженерии</h3><p>Естественная вентиляция с выводом на фасад, механизмы на 24 В, подключение к умному дому по KNX, Z-Wave, Zigbee, Wi-Fi.</p></div>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Как мы работаем с бюро</span><h2>Четыре шага до вознаграждения</h2></div><p>Вы ведёте клиента и интерьер, мы отвечаем за погреб от расчёта до сдачи.</p></div>
  <ol class="partner-steps">
    <li><span class="p-n">1</span><h3>Присылаете проект</h3><p>План, разрез или просто идею: где хотите люк и какая коллекция у клиента.</p></li>
    <li><span class="p-n">2</span><h3>Готовим решение</h3><p>Подбираем форму, глубину и отделку, даём технические данные и предварительный расчёт.</p></li>
    <li><span class="p-n">3</span><h3>Заключаем договор</h3><p>Фиксируем агентское вознаграждение 5–10% от стоимости погреба.</p></li>
    <li><span class="p-n">4</span><h3>Делаем и сдаём</h3><p>Производство, монтаж и запуск под нашим контролем. Вы получаете вознаграждение по договору.</p></li>
  </ol>
</div></section>
'''
form=S['CONTACT'].replace('<section class="sec" id="contact" style="padding-top:0">','<section class="sec" id="arch-form" style="padding-top:0">').replace('<form class="form" id="leadForm" novalidate>','<form class="form" id="leadForm" novalidate data-role="architect">').replace('<h2>Расскажите о доме, и мы рассчитаем погреб</h2>','<h2>Расскажите о проекте, и мы подготовим решение</h2>').replace('<h3>Заявка на расчёт</h3>','<h3>Заявка от архитектора</h3>')
a=band.replace('<div class="wrap sec">','<div class="wrap sec" style="padding-top:calc(170px + env(safe-area-inset-top,0px))">')
a=a.replace('<span class="kicker" style="color:var(--bone);opacity:.8">Для архитекторов и дизайнеров интерьеров</span>','<div class="crumb" style="color:rgba(242,235,227,.75)"><a href="index.html">Главная</a> / Архитекторам</div><span class="kicker" style="color:var(--bone);opacity:.8;margin-top:28px">Для архитекторов и дизайнеров интерьеров</span>')
a+=why+form
doc('architects.html','Архитекторам, ПОGREB WINE','Агентское вознаграждение 5–10% для архитекторов и дизайнеров интерьеров за винные погреба в проектах клиентов.',a,'architects.html',ld=[crumbs_ld([('index.html','Главная'),('architects.html','Архитекторам')])])

# ---------- contacts ----------
ct=S['CONTACT'].replace('<section class="sec" id="contact" style="padding-top:0">','<section class="sec" id="contact" style="padding-top:calc(170px + env(safe-area-inset-top,0px))">')
ct=ct.replace('<span class="kicker">Контакты</span>','<div class="crumb"><a href="index.html">Главная</a> / Контакты</div><span class="kicker" style="margin-top:28px">Контакты</span>')
doc('contacts.html','Контакты, ПОGREB WINE','Контакты ПОGREB WINE: директор Роман Голубев, офис в Саратове, заявка на расчёт винного погреба.',ct,'contacts.html',ld=[crumbs_ld([('index.html','Главная'),('contacts.html','Контакты')])])
exec(open(os.path.join(BASE,'build_more.py'),encoding='utf-8').read())
print('built')
