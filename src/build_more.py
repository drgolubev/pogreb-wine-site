# executed inside build_pages.py namespace
from articles import ARTICLES
AMAP={a['slug']:a for a in ARTICLES}
DATE_ISO='2026-10-21'; DATE_RU='21 октября 2026'
def art_url(slug): return f'zhurnal-{slug}.html'

def art_card(a):
    return f'''<a class="jcard" href="{art_url(a['slug'])}"><div class="jcard-media"><img src="{a['img']}" alt="{a['alt']}" loading="lazy"></div><div class="jcard-body"><span class="jcard-meta">{a['read']} мин чтения</span><h3>{a['title']}</h3><p>{a['lead']}</p><span class="tcard-go"><i></i>Читать</span></div></a>'''

def case_hero(crumb, title, lead, img, alt):
    return page_hero('<a href="objects.html">Объекты</a> / '+crumb, title, lead, img, alt)

# ---------- case: Mozhaysk ----------
mz=case_hero('Панинотека','Панинотека, Можайск','Погреб в обеденном зале итальянского ресторана, в уже готовом помещении и при высоких грунтовых водах. Рассказываем, какие были условия, как шли работы и что получилось.','media/hatch-open.jpg','Открытый стеклянный люк погреба в зале ресторана Панинотека')
mz+='''<section class="sec" style="padding-top:0"><div class="wrap passport">
  <div><span class="kicker">Об объекте</span><h2>Погреб, который гости видят сквозь пол</h2><p class="lid-lead">Ресторан хотел винное пространство прямо в зале, рядом с винной стеной. Места под шкафы не было, а рядом Можайское водохранилище, поэтому грунтовые воды стоят высоко. Погреб нужно было поставить в готовое помещение и сделать так, чтобы внутри было сухо.</p></div>
  <dl class="specs passport-specs">
    <div><dt>Объект</dt><dd>итальянский ресторан «Панинотека»</dd></div>
    <div><dt>Город</dt><dd>Можайск, Московская область</dd></div>
    <div><dt>Год</dt><dd>2024</dd></div>
    <div><dt>Помещение</dt><dd>готовый обеденный зал</dd></div>
    <div><dt>Условия</dt><dd>высокие грунтовые воды рядом с водохранилищем</dd></div>
    <div><dt>Защита от воды</dt><dd>монолитный бетонный кессон и мембрана ЭПДМ</dd></div>
    <div><dt>Люк</dt><dd>круглый, лифтовые механизмы и осевое вращение</dd></div>
    <div><dt>Стекло</dt><dd>триплекс с чёрной стемалитовой полосой</dd></div>
  </dl>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="why-arch tsr">
    <div><span class="tsr-k">Задача</span><h3>Погреб в готовом зале</h3><p>Поставить погреб в работающее помещение ресторана и не перестраивать зал.</p></div>
    <div><span class="tsr-k">Сложность</span><h3>Вода рядом</h3><p>Можайское водохранилище поднимает уровень грунтовых вод. Обычной гидроизоляции здесь мало.</p></div>
    <div><span class="tsr-k">Результат</span><h3>Сухо внутри</h3><p>Погреб стоит в бетонном кессоне и мембране. Внутри сухо, а люк стал главной деталью зала.</p></div>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Этапы</span><h2>Как шли работы</h2></div><p>Фото со стройки. Так погреб выглядит, пока его не закрыли полом.</p></div>
  <ol class="stages">
    <li><figure><img src="media/mz-stage-1.jpg" alt="Основание кессона под погреб в Можайске" loading="lazy"></figure><span class="st-n">01</span><h3>Основание</h3><p>Вскрыли плиту перекрытия, вручную выбрали грунт и подготовили основание кессона.</p></li>
    <li><figure><img src="media/mz-stage-2.jpg" alt="Монолитный бетонный кессон под погреб" loading="lazy"></figure><span class="st-n">02</span><h3>Кессон</h3><p>Залили монолитный бетонный кессон. Он принимает давление грунтовых вод на себя.</p></li>
    <li><figure><img src="media/mz-stage-3.jpg" alt="Модульные блоки и ступени погреба внутри мембраны" loading="lazy"></figure><span class="st-n">03</span><h3>Мембрана и блоки</h3><p>Уложили мембрану ЭПДМ, собрали модульный погреб, лестницу и вентиляцию.</p></li>
    <li><figure><img src="media/hatch-closed.jpg" alt="Закрытый стеклянный люк в полу ресторана" loading="lazy"></figure><span class="st-n">04</span><h3>Люк и пол</h3><p>Поставили люк с лифтовыми механизмами и осевым вращением, восстановили пол плиткой.</p></li>
    <li><figure><img src="media/top-hatch.jpg" alt="Вид сверху сквозь стекло люка на лестницу" loading="lazy"></figure><span class="st-n">05</span><h3>Готово</h3><p>Стекло триплекс, подсветка, дубовые ступени. После сдачи ресторан открыл новое винное пространство.</p></li>
  </ol>
</div></section>
<section class="inside" aria-label="Спуск в погреб Панинотеки"><div class="inside-media"><video src="media/inside-descent.mp4" poster="media/inside-descent-poster.jpg" muted loop playsinline preload="metadata" aria-label="Спуск по лестнице мимо ниш с вином и шампанским"></video></div><div class="wrap inside-copy"><h2>Внутри погреба Панинотеки</h2><p>Дубовые ступени, ниши для бутылок, ящиков и шампанского по всей спирали, бар внизу. Подсветка 4000 К показывает этикетки и не греет вино.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Фото</span><h2>Погреб в жизни ресторана</h2></div><p>Листайте в сторону.</p></div>
  <div class="strip" id="strip" tabindex="0" aria-label="Фото Панинотеки, листайте в сторону">
    <figure style="aspect-ratio:3/4"><img src="media/dinner.jpg" alt="Гости ужинают у стола рядом с люком погреба"><figcaption>Ужин в паре шагов от коллекции</figcaption></figure>
    <figure style="aspect-ratio:3/4"><img src="media/guest-bottle.jpg" alt="Гость поднимается из погреба с бутылкой"><figcaption>За бутылкой к ужину</figcaption></figure>
    <figure style="aspect-ratio:4/3"><img src="media/hall-hatch.jpg" alt="Закрытый люк погреба в зале перед винной стеной"><figcaption>Люк в зале, перед винной стеной</figcaption></figure>
    <figure style="aspect-ratio:3/4"><img src="media/glass-angle.jpg" alt="Стеклянный люк под углом"><figcaption>Триплекс с чёрной стемалитовой полосой</figcaption></figure>
    <figure style="aspect-ratio:3/4"><img src="media/spiral-close.jpg" alt="Дубовые ступени и ниши с бутылками"><figcaption>Дубовые ступени и ниши</figcaption></figure>
    <figure style="aspect-ratio:4/3"><img src="media/wine-wall.jpg" alt="Винная стена ресторана"><figcaption>Винная стена Панинотеки</figcaption></figure>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Читать по теме</span><h2>Если у вас похожая задача</h2></div><p>Высокие грунтовые воды или готовый дом не помеха погребу.</p></div>
  <div class="jgrid jgrid-2">'''+art_card(AMAP['pogreb-pri-vysokih-gruntovyh-vodah'])+art_card(AMAP['pogreb-v-gotovom-dome'])+'''</div>
  <div class="case-next"><span>Следующий объект</span><a href="case-khosta.html">Хоста, вилла над морем →</a></div>
</div></section>
'''+CTA
doc('case-mozhaysk.html','Погреб в ресторане Панинотека, Можайск — ПОGREB WINE','Спиральный винный погреб в готовом зале ресторана Панинотека в Можайске при высоких грунтовых водах: бетонный кессон, мембрана ЭПДМ, этапы работ и фото.',mz,'objects.html',
    ld=[crumbs_ld([('index.html','Главная'),('objects.html','Объекты'),('case-mozhaysk.html','Панинотека, Можайск')])],img='media/hatch-open.jpg')

# ---------- case: Khosta ----------
kh=case_hero('Хоста','Дом над морем, Хоста','Частная вилла на горном склоне в Сочи с видом на Чёрное море. Погреб стоит в гостиной у панорамных окон: днём люк отражает небо, вечером светится изнутри.','media/khosta-build.jpg','Люк погреба в гостиной виллы, за окном море')
kh+='''<section class="sec" style="padding-top:0"><div class="wrap lid">
  <div class="lid-media"><img src="media/kh-open.jpg" alt="Открытый круглый люк погреба в светлой гостиной, видна дубовая лестница и белые ниши"></div>
  <div>
    <span class="kicker">Об объекте</span>
    <h2>Белый погреб в светлом доме</h2>
    <p class="lid-lead">Интерьер виллы светлый, с панорамным остеклением и видом на море. Погреб сделали в тон: белые модульные блоки, дубовые ступени и круглый стеклянный люк в полу гостиной. Когда люк закрыт, он почти растворяется в полу.</p>
    <dl class="specs">
      <div><dt>Объект</dt><dd>частная вилла</dd></div>
      <div><dt>Место</dt><dd>Хоста, Сочи</dd></div>
      <div><dt>Участок</dt><dd>горный склон с видом на море</dd></div>
      <div><dt>Где погреб</dt><dd>гостиная у панорамных окон</dd></div>
      <div><dt>Люк</dt><dd>круглый, стекло в раме из нержавеющей стали</dd></div>
      <div><dt>Отделка</dt><dd>белые блоки, дубовые ступени</dd></div>
    </dl>
  </div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap lid lid-rev">
  <div>
    <span class="kicker">Готовый погреб</span>
    <h2>Белые блоки, дубовые ступени, тёплый свет</h2>
    <p class="lid-lead">Так погреб выглядит изнутри после сдачи. Ниши по всей высоте спирали, ступени из дуба, подсветка по окружности пола и люка.</p>
  </div>
  <div class="etz-video"><video src="media/kh-ready.mp4" poster="media/kh-ready-poster.jpg" muted loop playsinline preload="metadata" aria-label="Белые модульные блоки и дубовые ступени погреба на вилле в Хосте"></video></div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Как ставили</span><h2>Погреб на горном склоне</h2></div><p>Блоки в мембране, лестница и колонна, проверка каждого ряда электронным уровнем и монтаж люка. Всё это происходило, пока на вилле шла отделка.</p></div>
  <div class="strip" id="strip" tabindex="0" aria-label="Фото со стройки в Хосте, листайте в сторону">
    <figure style="aspect-ratio:3/4"><img src="media/kh-st1.jpg" alt="Модульные блоки погреба в мембране" loading="lazy"><figcaption>Блоки в мембране</figcaption></figure>
    <figure style="aspect-ratio:3/4"><img src="media/kh-st2.jpg" alt="Лестница и центральная колонна до отделки" loading="lazy"><figcaption>Лестница и колонна до отделки</figcaption></figure>
    <figure style="aspect-ratio:3/4"><img src="media/kh-st3.jpg" alt="Электронный уровень на ряду блоков: проверяем, что ряд идеально ровный" loading="lazy"><figcaption>Электронный уровень: ряд должен быть идеально ровным</figcaption></figure>
    <figure style="aspect-ratio:3/4"><img src="media/khosta-build.jpg" alt="Люк в гостиной на этапе отделки, за окном море" loading="lazy"><figcaption>Люк в гостиной на этапе отделки</figcaption></figure>
    <figure style="aspect-ratio:3/4"><img src="media/kh-open.jpg" alt="Открытый люк в готовой гостиной" loading="lazy"><figcaption>Готово: люк открыт</figcaption></figure>
  </div>
</div></section>
<div class="sea" id="khosta">
  <div class="sea-bg"><video src="media/khosta-sea.mp4" poster="media/khosta-sea-poster.jpg" muted loop playsinline preload="metadata" data-autoplay aria-hidden="true"></video></div>
  <div class="wrap">
    <div class="sea-grid">
      <div>
        <div class="case-meta">Хоста, Сочи</div>
        <h3>Люк в гостиной</h3>
        <p class="case-text" style="margin-top:24px">Погреб открывается касанием кнопки. Створка уходит, и сквозь пол видно спираль лестницы и ниши для бутылок.</p>
      </div>
      <div class="sea-pair">
        <figure><video src="media/khosta-villa.mp4" poster="media/khosta-villa-poster.jpg" muted loop playsinline preload="metadata" data-autoplay aria-label="Люк в гостиной виллы"></video><figcaption>Люк в гостиной</figcaption></figure>
        <figure><img src="media/khosta-build.jpg" alt="Люк на этапе отделки, за окном море"><figcaption>На этапе отделки</figcaption></figure>
      </div>
    </div>
  </div>
</div>
<section class="sec"><div class="wrap lift">
  <div><span class="kicker">Вокруг дома</span><h2>Терраса, бассейн и море</h2><p class="lid-lead">Снаружи южное солнце, а под полом гостиной грунт держит ровную прохладу. Вино лежит при правильной температуре без шума компрессора.</p></div>
  <div class="lift-media"><video src="media/kh-terrace.mp4" poster="media/kh-terrace-poster.jpg" muted loop playsinline preload="metadata" aria-label="Терраса виллы с бассейном и видом на море"></video></div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <figure class="wide-photo"><img src="media/kh-sunset.jpg" alt="Закат над Чёрным морем с террасы виллы" loading="lazy"><figcaption>Вид с виллы на закате</figcaption></figure>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="kicker">Читать по теме</span><h2>Погреб в новом доме</h2></div><p>Если дом ещё строится, погреб проще заложить в проект.</p></div>
  <div class="jgrid jgrid-2">'''+art_card(AMAP['pogreb-v-proekte-doma'])+art_card(AMAP['kak-hranit-vino-doma'])+'''</div>
  <div class="case-next"><span>Следующий объект</span><a href="case-kaliningrad.html">На берегу Балтийского моря, Калининград →</a></div>
</div></section>
'''+CTA
doc('case-khosta.html','Погреб на вилле в Хосте, Сочи — ПОGREB WINE','Спиральный винный погреб в гостиной частной виллы в Хосте (Сочи) на горном склоне с видом на море: круглый стеклянный люк, белые блоки, дубовые ступени.',kh,'objects.html',
    ld=[crumbs_ld([('index.html','Главная'),('objects.html','Объекты'),('case-khosta.html','Хоста, Сочи')])],img='media/khosta-build.jpg')


# ---------- generic case pages ----------
from cases import CASES, case_card, case_url, gallery_figure
for i, cs in enumerate(CASES):
    if cs.get('custom'):
        continue
    nxt = CASES[(i + 1) % len(CASES)]
    body = page_hero('<a href="objects.html">Объекты</a> / ' + cs['city'], cs['title'] + ', ' + cs['city'].split(',')[-1].strip(), cs['lead'], cs['hero'], cs['card_alt'])
    body += '<section class="sec" style="padding-top:0"><div class="wrap passport"><div><span class="kicker">Об объекте</span><h2>' + cs['kind'] + ', ' + cs['city'] + '</h2><p class="lid-lead">' + cs['short'] + '</p></div><dl class="specs passport-specs">' + ''.join('<div><dt>' + k + '</dt><dd>' + v + '</dd></div>' for k, v in cs['passport']) + '</dl></div></section>\n'
    body += '<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><div><span class="kicker">Фото и видео</span><h2>Как это было</h2></div><p>Листайте в сторону или нажимайте стрелки.</p></div><div class="strip" id="strip" tabindex="0" aria-label="Фото объекта, листайте в сторону">' + ''.join(gallery_figure(*g) for g in cs['gallery']) + '</div></div></section>\n'
    others = [x for x in CASES if x['slug'] != cs['slug']][:3]
    body += '<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><div><span class="kicker">Другие объекты</span><h2>Ещё наши погреба</h2></div><p><a href="objects.html">Все объекты</a></p></div><div class="ogrid">' + ''.join(case_card(x) for x in others) + '</div><div class="case-next"><span>Следующий объект</span><a href="' + case_url(nxt) + '">' + nxt['title'] + ' →</a></div></div></section>\n' + CTA
    doc(case_url(cs), 'Погреб: ' + cs['title'] + ', ' + cs['city'] + ' — ПОGREB WINE', cs['lead'][:180], body, 'objects.html',
        ld=[crumbs_ld([('index.html', 'Главная'), ('objects.html', 'Объекты'), (case_url(cs), cs['city'])])], img=cs['hero'])

# ---------- journal index ----------
j=page_hero('Журнал','Журнал','Отвечаем на вопросы, которые задают перед заказом погреба: сколько стоит, что делать с грунтовыми водами, можно ли поставить погреб в готовый дом и как вообще хранить вино.')
j+='<section class="sec" style="padding-top:0"><div class="wrap"><div class="jgrid">'+''.join(art_card(a) for a in ARTICLES)+'</div></div></section>\n'+CTA
doc('journal.html','Журнал о винных погребах — ПОGREB WINE','Статьи о винных погребах: цена погреба в доме, грунтовые воды, хранение вина, погреб в готовом доме и в проекте, сравнение с винным шкафом.',j,'journal.html',
    ld=[crumbs_ld([('index.html','Главная'),('journal.html','Журнал')]),{"@context":"https://schema.org","@type":"Blog","name":"Журнал ПОGREB WINE","url":SITE+"journal.html","publisher":{"@id":SITE+"#org"},"blogPost":[{"@type":"BlogPosting","headline":a['title'],"url":SITE+art_url(a['slug'])} for a in ARTICLES]}])

# ---------- articles ----------
for a in ARTICLES:
    url=art_url(a['slug'])
    body=f'''<section class="page-hero art-hero"><div class="wrap"><div class="crumb"><a href="index.html">Главная</a> / <a href="journal.html">Журнал</a> / {a['short']}</div><h1>{a['title']}</h1><p class="page-lead">{a['lead']}</p><div class="art-meta">{DATE_RU} · {a['read']} мин чтения · ПОGREB WINE</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><figure class="art-cover"><img src="{a['img']}" alt="{a['alt']}"></figure>
<article class="article">{a['body']}</article></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><div><span class="kicker">Ещё в журнале</span><h2>Читать дальше</h2></div><p><a href="journal.html">Все статьи</a></p></div><div class="jgrid jgrid-2">{''.join(art_card(AMAP[s]) for s in a['related'])}</div></div></section>
'''+CTA
    ld=[crumbs_ld([('index.html','Главная'),('journal.html','Журнал'),(url,a['short'])]),
        {"@context":"https://schema.org","@type":"Article","headline":a['title'],"description":a['desc'],"image":SITE+a['img'],"datePublished":DATE_ISO,"dateModified":DATE_ISO,"inLanguage":"ru","author":{"@id":SITE+"#org"},"publisher":{"@id":SITE+"#org"},"mainEntityOfPage":SITE+url}]
    doc(url,a['title']+' — ПОGREB WINE',a['desc'],body,'journal.html',ld=ld,img=a['img'],ogtype='article')

exec(open(os.path.join(BASE,'konstruktor.py'),encoding='utf-8').read())

# ---------- sitemap / robots ----------
pri={'index.html':'1.0','pogreb.html':'0.9','price.html':'0.9','objects.html':'0.9','contacts.html':'0.8','architects.html':'0.8','journal.html':'0.7','konstruktor.html':'0.8'}
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for f in dict.fromkeys(PAGES):
    sm+=f'  <url><loc>{SITE}{"" if f=="index.html" else f}</loc><lastmod>{DATE_ISO}</lastmod><priority>{pri.get(f,"0.6")}</priority></url>\n'
sm+='</urlset>\n'
open(os.path.join(OUT,'sitemap.xml'),'w',encoding='utf-8').write(sm)
open(os.path.join(OUT,'robots.txt'),'w',encoding='utf-8').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
