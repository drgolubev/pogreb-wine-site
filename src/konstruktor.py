# Онлайн-конструктор погреба: страница konstruktor.html.
# Варианты и подписи меняются здесь, рисунок и логика в konstruktor.js (ключи вариантов должны совпадать).
# Формат шага: (ключ, заголовок, подсказка, тип, [(значение, название, пояснение, цвет-образец или '')]).

KZ_STEPS = [
 ('shape', 'Форма люка', 'Люк лежит вровень с чистовым полом', 'radio', [
   ('round', 'Круглый', 'Ø 1,9 м, классика спиральных погребов', ''),
   ('oval', 'Овальный', 'Вытянутый, для просторной гостиной', ''),
   ('rect', 'Прямоугольный', 'Под плитку и строгие интерьеры', ''),
 ]),
 ('mech', 'Как открывается люк', 'Все три механизма автоматические', 'radio', [
   ('lift', 'Подъём с поворотом', 'Стекло поднимается и отъезжает в сторону', ''),
   ('hinge', 'Обратный шарнир', 'Половина стекла откидывается на петле', ''),
   ('act', 'Актуатор', 'Стекло приподнимается на приводе, как крышка', ''),
 ]),
 ('glass', 'Стекло', 'Закалённый триплекс, по нему можно ходить', 'swatch', [
   ('clear', 'Прозрачное', 'Видно всё до последней ступени', '#cfe0e4'),
   ('bronze', 'Бронза', 'Тёплый оттенок, как у старого стекла', '#8a5a2b'),
   ('graphite', 'Графит', 'Строго и немного загадочно', '#2b2e33'),
   ('blue', 'Синее', 'Холодный глубокий тон', '#2f5680'),
 ]),
 ('depth', 'Глубина', 'Чем глубже, тем больше ниш для бутылок', 'radio', [
   ('2', '2 м', '', ''), ('2.25', '2,25 м', '', ''), ('2.5', '2,5 м', '', ''),
   ('2.75', '2,75 м', 'оптимально', ''), ('3', '3 м', '', ''),
 ]),
 ('wood', 'Ступени', 'Только натуральное дерево', 'swatch', [
   ('oak-light', 'Светлый дуб', '', '#d8b98b'),
   ('oak', 'Натуральный дуб', '', '#b88752'),
   ('walnut', 'Орех', '', '#7a4d2c'),
   ('oak-dark', 'Морёный дуб', '', '#3f2a1d'),
 ]),
 ('ctrl', 'Чем открывать', 'Можно совместить несколько способов', 'radio', [
   ('panel', 'Сенсорная кнопка', 'На стене, входит в комплект', ''),
   ('remote', 'Пульт', 'Открыть люк с дивана', ''),
   ('finger', 'Отпечаток пальца', 'Биометрический сканер, без ключей', ''),
   ('smart', 'Умный дом и Алиса', 'KNX или Z-Wave, со смартфона и голосом', ''),
 ]),
 ('extra', 'Дополнительно', 'Можно выбрать несколько', 'check', [
   ('bar', 'Бар в нише', 'Бокалы и крепкое рядом с вином', ''),
   ('boxes', 'Высокие ниши для ящиков', 'Нижний ряд под деревянные ящики', ''),
   ('safe', 'Встроенный сейф', 'Для самых ценных бутылок', ''),
   ('climate', 'Датчики климата', 'Температура, влажность, CO₂ и протечка в телефоне', ''),
   ('vent', 'Приточная вентиляция', 'Свежий воздух без сквозняков', ''),
   ('etz', 'Этажерка из пола', 'Для гостиной или террасы', ''),
   ('barrel', 'Этажерка в бочке', 'На колёсиках, можно выкатить на улицу', ''),
 ]),
]
KZ_DEFAULT = {'shape': 'round', 'mech': 'lift', 'glass': 'bronze', 'depth': '2.75', 'wood': 'oak', 'ctrl': 'panel'}


def kz_step(i, step):
    key, title, hint, kind, opts = step
    cls = 'kz-opts-' + ('swatch' if kind == 'swatch' else 'depth' if key == 'depth' else 'list')
    typ = 'checkbox' if kind == 'check' else 'radio'
    out = []
    for val, name, note, color in opts:
        checked = ' checked' if KZ_DEFAULT.get(key) == val else ''
        sw = '<i class="kz-sw" style="--sw:' + color + '"></i>' if color else ''
        nt = '<small>' + note + '</small>' if note else ''
        out.append('<label class="kz-opt"><input type="' + typ + '" name="' + key + '" value="' + val + '"' + checked + '>'
                   + '<span class="kz-opt-in">' + sw + '<span class="kz-opt-t"><b>' + name + '</b>' + nt + '</span></span></label>')
    return ('<fieldset class="kz-step" id="kz-' + key + '"><legend><span class="kz-num">' + str(i + 1).zfill(2) + '</span>' + title + '</legend>'
            '<p class="kz-hint">' + hint + '</p><div class="kz-opts ' + cls + '">' + ''.join(out) + '</div></fieldset>')


kz_steps_html = ''.join(kz_step(i, s) for i, s in enumerate(KZ_STEPS))

kz = page_hero('Конструктор', 'Соберите свой погреб',
               'Выберите форму люка, механизм, стекло, глубину, дерево ступеней и способ открывания. Рисунок меняется вместе с выбором, а готовую сборку можно отправить нам на расчёт.')
kz += '''<section class="sec kz-sec" style="padding-top:0"><div class="wrap kz-grid">
  <div class="kz-stage-col">
    <div class="kz-stage" id="kzStage">
      <div class="kz-tabs" role="tablist" aria-label="Вид">
        <button type="button" role="tab" aria-selected="true" data-view="room">В комнате</button>
        <button type="button" role="tab" aria-selected="false" data-view="cut">В разрезе</button>
      </div>
      <div class="kz-view kz-room is-on" id="kzRoom" data-view="room">
        <div class="kz-wall" aria-hidden="true"></div>
        <div class="kz-scene" aria-hidden="true">
          <div class="kz-floor">
            <div class="kz-hatch" id="kzHatch">
              <div class="kz-pit" id="kzPit"></div>
              <div class="kz-glass" id="kzGlass"><div class="kz-g kz-g1"><i></i></div><div class="kz-g kz-g2"><i></i></div></div>
            </div>
          </div>
        </div>
        <div class="kz-room-glow" aria-hidden="true"></div>
      </div>
      <div class="kz-view kz-cut" id="kzCut" data-view="cut"></div>
      <div class="kz-stage-bar">
        <button type="button" class="kz-open" id="kzOpen" aria-pressed="false"><span class="kz-open-ic" aria-hidden="true"></span><span id="kzOpenT">Открыть люк</span></button>
        <span class="kz-stage-note" id="kzNote">Рисунок условный, точный проект готовим после замера</span>
      </div>
    </div>
    <div class="kz-live">
      <figure class="kz-live-card"><img id="kzLiveMech" src="media/k-lift.jpg" alt="" loading="lazy"><figcaption><span>Механизм вживую</span><b id="kzLiveMechT">Подъём с поворотом</b></figcaption></figure>
      <figure class="kz-live-card"><img id="kzLiveCtrl" src="media/k-panel.jpg" alt="" loading="lazy"><figcaption><span>Чем открывать</span><b id="kzLiveCtrlT">Сенсорная кнопка</b></figcaption></figure>
    </div>
  </div>
  <form class="kz-form" id="kzForm" onsubmit="return false">
''' + kz_steps_html + '''
    <div class="kz-sum" id="kzSum" aria-live="polite">
      <span class="kicker">Ваш погреб</span>
      <dl class="kz-sum-list" id="kzSumList"></dl>
      <div class="kz-price"><span>Стоимость</span><b>от 3,5 млн ₽</b><small>Точную сумму назовём после замера: она зависит от глубины, формы, механизма и условий на участке</small></div>
      <div class="kz-sum-act"><a class="btn btn-wine" id="kzSend" href="contacts.html">Отправить на расчёт</a><button type="button" class="btn btn-line" id="kzCopy">Скопировать</button></div>
    </div>
  </form>
</div></section>
<script src="konstruktor.js"></script>
''' + CTA
doc('konstruktor.html', 'Конструктор винного погреба онлайн — ПОGREB WINE',
    'Соберите спиральный винный погреб онлайн: форма и механизм люка, цвет стекла, глубина, дерево ступеней, управление и умный дом. Рисунок меняется вместе с выбором.',
    kz, 'konstruktor.html', ld=[crumbs_ld([('index.html', 'Главная'), ('konstruktor.html', 'Конструктор')])], img='media/k-lift.jpg')
