/* Онлайн-конструктор погреба ПОGREB WINE.
   Рисует погреб сверху (сквозь люк) и в разрезе по выбранным параметрам. Без библиотек. */
(function () {
  var form = document.getElementById('kzForm');
  if (!form) return;
  var stage = document.getElementById('kzStage');
  var pit = document.getElementById('kzPit');
  var hatch = document.getElementById('kzHatch');
  var cut = document.getElementById('kzCut');
  var NS = 'http://www.w3.org/2000/svg';

  var WOOD = { 'leather': '#3a302b', 'oak': '#b88752' };
  var GLASS = {
    clear: 'rgba(205,228,235,.12)', bronze: 'rgba(122,68,24,.52)',
    graphite: 'rgba(14,16,20,.66)', blue: 'rgba(24,62,116,.52)'
  };
  var MECH_PHOTO = {
    act: ['media/hero-hatch-open-poster.jpg', 'Люк на актуаторе: половина стекла прокручивается под вторую'],
    hinge: ['media/k-hinge.jpg', 'Половина стекла откинута на обратном шарнире'],
    act: ['media/k-act.jpg', 'Стекло приподнято актуатором'],
    rect: ['media/hatch-lift-poster.jpg', 'Прямоугольный люк на подъёмном приводе']
  };
  var MECH_VIDEO = {
    act: ['media/hero-hatch-open.mp4', 'Актуатор: стекло приподнимается, и половина люка прокручивается под вторую']
  };
  var CTRL_PHOTO = {
    panel: 'media/k-panel.jpg', remote: 'media/k-remote.jpg', finger: 'media/k-finger.jpg', smart: 'media/k-panel.jpg'
  };

  /* ---------- состояние ---------- */
  function readForm() {
    var c = { extra: [] };
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || !el.checked) return;
      if (el.type === 'checkbox') c.extra.push(el.value); else c[el.name] = el.value;
    });
    c.depthN = parseFloat(c.depth);
    return c;
  }
  function applyParams() {
    var q = new URLSearchParams(location.search);
    q.forEach(function (v, k) {
      if (k === 'extra') {
        v.split(',').forEach(function (x) {
          var el = form.querySelector('input[name="extra"][value="' + x + '"]'); if (el) el.checked = true;
        });
      } else {
        var el = form.querySelector('input[name="' + k + '"][value="' + v + '"]'); if (el) el.checked = true;
      }
    });
  }

  /* ---------- цвет ---------- */
  function hex2rgb(h) { h = h.replace('#', ''); return [parseInt(h.substr(0, 2), 16), parseInt(h.substr(2, 2), 16), parseInt(h.substr(4, 2), 16)]; }
  function shade(h, k, warm) {
    var c = hex2rgb(h);
    var r = c[0] * k + (warm ? 18 * (1 - k) : 0), g = c[1] * k + (warm ? 6 * (1 - k) : 0), b = c[2] * k;
    return 'rgb(' + Math.round(r) + ',' + Math.round(g) + ',' + Math.round(b) + ')';
  }
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  /* ---------- вид сверху сквозь люк ---------- */
  // Погреб рисуется как тоннель: чем глубже уровень, тем меньше круг и тем сильнее он смещён к зрителю,
  // поэтому дальняя стена видна широкой полосой, а ближняя почти скрыта.
  var BOTTLES = ['#4a0f19', '#2a3a22', '#651625', '#1d1a15', '#3a1a10', '#57121e'];
  function mix(a, b, t) {
    var x = hex2rgb(a), y = hex2rgb(b);
    return 'rgb(' + Math.round(x[0] + (y[0] - x[0]) * t) + ',' + Math.round(x[1] + (y[1] - x[1]) * t) + ',' + Math.round(x[2] + (y[2] - x[2]) * t) + ')';
  }
  function drawPit(c, depth) {
    var oval = c.shape === 'oval', rect = c.shape === 'rect';
    var W = oval ? 540 : 400, H = 400;
    var svg = el('svg', { viewBox: (-W / 2) + ' ' + (-H / 2) + ' ' + W + ' ' + H, preserveAspectRatio: 'none', 'aria-hidden': 'true' });
    var defs = el('defs', {}, svg);
    var R0 = 198, RC = 22, SH = 30;
    function F(d) { return 1 / (1 + 0.62 * d); }
    function R(d) { return R0 * F(d); }
    function Y(d) { return SH * d; }

    var lg = el('radialGradient', { id: 'kzLight', cx: 0, cy: Y(depth), r: R0, gradientUnits: 'userSpaceOnUse' }, defs);
    el('stop', { offset: 0, 'stop-color': '#ffb460', 'stop-opacity': '.42' }, lg);
    el('stop', { offset: .45, 'stop-color': '#ffb460', 'stop-opacity': '.12' }, lg);
    el('stop', { offset: 1, 'stop-color': '#ffb460', 'stop-opacity': '0' }, lg);
    var cg = el('radialGradient', { id: 'kzCol', cx: -7, cy: -7, r: RC + 8, gradientUnits: 'userSpaceOnUse' }, defs);
    el('stop', { offset: 0, 'stop-color': '#fffaf3' }, cg);
    el('stop', { offset: 1, 'stop-color': '#b9ad9f' }, cg);

    if (rect) el('rect', { x: -W / 2, y: -H / 2, width: W, height: H, fill: '#e9dccb' }, svg);
    var g = el('g', { transform: oval ? 'scale(1.36,1)' : '' }, svg);
    // стены тоннелем: светлые наверху, тёплые и тёмные внизу
    var n = 0;
    for (var d = 0; d <= depth + 0.001; d += 0.06) {
      var t = d / 3.2;
      el('circle', { cx: 0, cy: Y(d), r: R(d), fill: t < .45 ? mix('#f3eadc', '#c49a6c', t / .45) : mix('#c49a6c', '#3a2316', (t - .45) / .55) }, g);
      n++;
    }
    // пол внизу
    el('circle', { cx: 0, cy: Y(depth), r: R(depth), fill: shade(WOOD.oak, .42, true) }, g);
    el('circle', { cx: 0, cy: Y(depth), r: R(depth), fill: 'none', stroke: '#ffcf86', 'stroke-width': 3.2, opacity: .85 }, g);

    // ниши с бутылками, снизу вверх
    var rows = [];
    for (var dr = 0.1; dr < depth - 0.2; dr += 0.3) rows.push(dr);
    for (var ri = rows.length - 1; ri >= 0; ri--) {
      var d0 = rows[ri], d1 = d0 + 0.25, k = 1 - 0.62 * (d0 / 3);
      for (var a = 0; a < 360; a += 15) {
        var a0 = (a + (ri % 2) * 7.5) * Math.PI / 180, a1 = a0 + 13.2 * Math.PI / 180;
        var isBar = c.extra.indexOf('bar') > -1 && ri === 1 && a >= 225 && a < 300;
        var p0 = pt(d0, a0), p1 = pt(d0, a1), q1 = pt(d1, a1), q0 = pt(d1, a0);
        var path = 'M' + p0 + 'A' + R(d0) + ' ' + R(d0) + ' 0 0 1 ' + p1 + 'L' + q1 + 'A' + R(d1) + ' ' + R(d1) + ' 0 0 0 ' + q0 + 'Z';
        el('path', { d: path, fill: isBar ? shade('#f0bb6c', k) : shade('#22140d', k * .9) }, g);
        var am = (a0 + a1) / 2, dm = (d0 + d1) / 2;
        if (isBar) { var b0 = ptA(dm, am); el('circle', { cx: b0[0], cy: b0[1], r: 2.4 * F(dm), fill: '#fff8ec' }, g); continue; }
        if ((a / 15 + ri) % 7 === 3) continue;
        for (var bb = 0; bb < 2; bb++) {
          var pb = ptA(dm, a0 + (bb + 0.5) * (a1 - a0) / 2);
          el('circle', { cx: pb[0], cy: pb[1], r: 4.4 * F(dm), fill: BOTTLES[(a / 15 + bb * 3 + ri * 2) % BOTTLES.length] }, g);
          el('circle', { cx: pb[0] - 1.2 * F(dm), cy: pb[1] - 1.2 * F(dm), r: 1.3 * F(dm), fill: '#fff', opacity: .35 * k }, g);
        }
      }
    }
    function ptA(d, a) { return [R(d) * Math.cos(a), Y(d) + R(d) * Math.sin(a)]; }
    function pt(d, a) { var q = ptA(d, a); return q[0] + ' ' + q[1]; }

    // колонна уходит вниз
    var cb = RC * F(depth);
    el('path', { d: 'M' + (-RC) + ' 0L' + (-cb) + ' ' + Y(depth) + 'L' + cb + ' ' + Y(depth) + 'L' + RC + ' 0Z', fill: '#d8cdbf' }, g);

    // ступени по спирали, снизу вверх
    var wood = WOOD[c.wood];
    var N = Math.round(depth / 0.2), step = 27, start = 100;
    for (var i = N - 1; i >= 0; i--) {
      var dd = 0.18 + i * (depth - 0.24) / N;
      var s0 = (start + i * step) * Math.PI / 180, s1 = s0 + (step - 2) * Math.PI / 180;
      var k2 = 1 - 0.62 * (dd / 3);
      // тень и торец под ступенью
      el('path', { d: wedge(dd + 0.16, s0, s1, RC, F, Y, R), fill: 'rgba(20,10,5,.45)' }, g);
      var leather = c.wood === 'leather', frame = leather ? '#e6ddd0' : wood;
      el('path', { d: wedge(dd + 0.05, s0, s1, RC, F, Y, R), fill: shade(frame, k2 * .5, true) }, g);
      el('path', { d: wedge(dd, s0, s1, RC, F, Y, R), fill: shade(frame, k2, true) }, g);
      var sm = (s0 + s1) / 2, rin = RC * F(dd), rout = R(dd) - 2, cy = Y(dd);
      if (leather) {
        // белая ступень с кожаной накладкой внутри
        var pad = 2.2 * Math.PI / 180, r1 = rin + 14 * F(dd), r2 = rout - 7 * F(dd);
        var P = function (r, a) { return (r * Math.cos(a)) + ' ' + (cy + r * Math.sin(a)); };
        el('path', { d: 'M' + P(r1, s0 + pad) + 'L' + P(r2, s0 + pad) + 'A' + r2 + ' ' + r2 + ' 0 0 1 ' + P(r2, s1 - pad) + 'L' + P(r1, s1 - pad) + 'Z', fill: shade(wood, k2, true) }, g);
      }
      for (var gr = -1; gr <= 1 && !leather; gr += 2) {
        var ag = sm + gr * 0.12;
        el('line', { x1: rin * Math.cos(ag), y1: cy + rin * Math.sin(ag), x2: rout * Math.cos(ag), y2: cy + rout * Math.sin(ag), stroke: shade(wood, k2 * .8, true), 'stroke-width': 1.1 * F(dd) * 2, opacity: .45 }, g);
      }
      el('line', { x1: rin * Math.cos(s1), y1: cy + rin * Math.sin(s1), x2: rout * Math.cos(s1), y2: cy + rout * Math.sin(s1), stroke: '#fff4e4', 'stroke-width': 1.6 * F(dd) * 1.6, opacity: .6 * k2 }, g);
    }
    // верх колонны, свет
    el('circle', { cx: 0, cy: 0, r: RC, fill: 'url(#kzCol)' }, g);
    el('circle', { cx: 0, cy: 0, r: R0, fill: 'url(#kzLight)' }, g);
    if (!rect) el('circle', { cx: 0, cy: 0, r: R0 - 3, fill: 'none', stroke: '#ffe6bb', 'stroke-width': 4, opacity: .8 }, g);
    else el('rect', { x: -W / 2 + 3, y: -H / 2 + 3, width: W - 6, height: H - 6, fill: 'none', stroke: '#ffe6bb', 'stroke-width': 4, opacity: .75 }, svg);
    return svg;
  }
  function wedge(d, a0, a1, RC, F, Y, R) {
    var r1 = RC * F(d), r2 = R(d) - 1.5, cy = Y(d);
    function P(r, a) { return (r * Math.cos(a)) + ' ' + (cy + r * Math.sin(a)); }
    return 'M' + P(r1, a0) + 'L' + P(r2, a0) + 'A' + r2 + ' ' + r2 + ' 0 0 1 ' + P(r2, a1) + 'L' + P(r1, a1) + 'A' + r1 + ' ' + r1 + ' 0 0 0 ' + P(r1, a0) + 'Z';
  }

  /* ---------- разрез ---------- */
  function drawCut(c, depth, open) {
    var S = 100, fy = 205, sx = 340, sw = 190, cx = sx + sw / 2, bot = fy + depth * S;
    var svg = el('svg', { viewBox: '0 0 640 530', role: 'img', 'aria-label': 'Погреб в разрезе, глубина ' + fmt(depth) + ' м' });
    var defs = el('defs', {}, svg);
    var pat = el('pattern', { id: 'kzSoil', width: 18, height: 18, patternUnits: 'userSpaceOnUse' }, defs);
    el('rect', { width: 18, height: 18, fill: '#1b120d' }, pat);
    el('circle', { cx: 4, cy: 5, r: 1.2, fill: '#2d2018' }, pat);
    el('circle', { cx: 13, cy: 12, r: 1.6, fill: '#2a1d15' }, pat);
    var ig = el('linearGradient', { id: 'kzIn', x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    el('stop', { offset: 0, 'stop-color': '#5a3a22' }, ig);
    el('stop', { offset: 1, 'stop-color': '#24150e' }, ig);
    var gl = el('radialGradient', { id: 'kzGlow', cx: .5, cy: .2, r: .8 }, defs);
    el('stop', { offset: 0, 'stop-color': '#ffbf73', 'stop-opacity': '.35' }, gl);
    el('stop', { offset: 1, 'stop-color': '#ffbf73', 'stop-opacity': '0' }, gl);

    // комната и грунт
    el('rect', { x: 0, y: fy + 18, width: 640, height: 530 - fy, fill: 'url(#kzSoil)' }, svg);
    el('rect', { x: 0, y: fy, width: 640, height: 18, fill: '#3a2f2a' }, svg);
    el('rect', { x: 0, y: fy - 4, width: 640, height: 4, fill: '#8d7764' }, svg);
    // шахта
    el('rect', { x: sx - 12, y: fy, width: sw + 24, height: bot - fy + 14, fill: '#d9cdbd' }, svg);
    el('rect', { x: sx, y: fy, width: sw, height: bot - fy, fill: 'url(#kzIn)' }, svg);
    for (var y = fy + 30; y < bot; y += 30) {
      el('line', { x1: sx - 12, y1: y, x2: sx, y2: y, stroke: '#a89580', 'stroke-width': 1 }, svg);
      el('line', { x1: sx + sw, y1: y, x2: sx + sw + 12, y2: y, stroke: '#a89580', 'stroke-width': 1 }, svg);
    }
    // ниши на задней стене
    for (var yy = fy + 14; yy < bot - 26; yy += 33) {
      for (var xx = sx + 8; xx < sx + sw - 20; xx += 22) {
        if (Math.abs(xx + 7 - cx) < 16) continue;
        el('rect', { x: xx, y: yy, width: 16, height: 24, fill: '#1a0f0a', rx: 1 }, svg);
        el('circle', { cx: xx + 8, cy: yy + 8, r: 3, fill: BOTTLES[(xx + yy) % BOTTLES.length] }, svg);
        el('circle', { cx: xx + 8, cy: yy + 17, r: 3, fill: BOTTLES[(xx + yy + 2) % BOTTLES.length] }, svg);
      }
    }
    el('rect', { x: sx, y: fy, width: sw, height: bot - fy, fill: 'url(#kzGlow)' }, svg);
    // ступени: задние, колонна, передние
    var wood = WOOD[c.wood], N = Math.round(depth / 0.2), Rr = sw / 2 - 4;
    var back = el('g', {}, svg);
    el('rect', { x: cx - 9, y: fy, width: 18, height: bot - fy, fill: '#e8e0d6' }, svg);
    var front = el('g', {}, svg);
    for (var i = 0; i < N; i++) {
      var th = (i * 27 + 95) * Math.PI / 180;
      var sy = fy + (i + 1) * (depth * S) / (N + 1);
      var x2 = cx + Math.sin(th) * Rr, z = Math.cos(th);
      var grp = z < 0 ? back : front;
      var x1 = Math.min(cx, x2), w = Math.abs(x2 - cx);
      el('rect', { x: x1, y: sy, width: Math.max(w, 6), height: 7, fill: shade(wood, z < 0 ? .62 : 1, true), rx: 1.5 }, grp);
      el('rect', { x: x1, y: sy + 7, width: Math.max(w, 6), height: 3, fill: shade(wood, .45, true) }, grp);
    }
    el('rect', { x: sx, y: bot - 8, width: sw, height: 8, fill: shade(WOOD.oak, .7, true) }, svg);
    el('line', { x1: sx + 2, y1: bot - 9, x2: sx + sw - 2, y2: bot - 9, stroke: '#ffd08a', 'stroke-width': 2 }, svg);
    el('line', { x1: sx + 2, y1: fy + 20, x2: sx + sw - 2, y2: fy + 20, stroke: '#ffe2b0', 'stroke-width': 2 }, svg);
    el('rect', { x: sx - 12, y: bot, width: sw + 24, height: 14, fill: '#9d8f80' }, svg);

    // стекло
    var gcol = GLASS[c.glass], gx = sx - 6, gw = sw + 12;
    var glass = el('g', { 'class': 'kz-cut-glass' }, svg);
    var tr = '';
    if (c.mech === 'act' && open) {
      // половина приподнялась на пару миллиметров, вторая прокрутилась и ушла под неё
      el('rect', { x: gx + gw / 2, y: fy - 3, width: gw / 2, height: 7, fill: gcol, stroke: '#c9c3bc', 'stroke-width': 1.5, opacity: .85 }, glass);
      el('rect', { x: gx + gw / 2, y: fy - 9, width: gw / 2, height: 7, fill: gcol, stroke: '#c9c3bc', 'stroke-width': 1.5 }, glass);
      var arr = el('path', { d: 'M' + (gx + gw * .2) + ' ' + (fy - 22) + 'Q' + (gx + gw / 2) + ' ' + (fy - 46) + ' ' + (gx + gw * .8) + ' ' + (fy - 22), fill: 'none', stroke: '#e8b45a', 'stroke-width': 1.5, 'stroke-dasharray': '4 4' }, glass);
      el('path', { d: 'M' + (gx + gw * .8 - 7) + ' ' + (fy - 29) + 'l7 7l-9 2', fill: 'none', stroke: '#e8b45a', 'stroke-width': 1.5 }, glass);
    } else if (c.mech === 'hinge' && open) {
      el('rect', { x: gx + gw / 2, y: fy - 5, width: gw / 2, height: 7, fill: gcol, stroke: '#c9c3bc', 'stroke-width': 1.5 }, glass);
      el('rect', { x: gx, y: fy - 5, width: gw / 2, height: 7, fill: gcol, stroke: '#c9c3bc', 'stroke-width': 1.5, transform: 'rotate(100 ' + (gx + gw / 2) + ' ' + fy + ')' }, glass);
    } else {
      el('rect', { x: gx, y: fy - 5, width: gw, height: 7, fill: gcol, stroke: '#c9c3bc', 'stroke-width': 1.5, transform: tr }, glass);
    }
    // человек для масштаба
    var px = 250, ph = 1.8 * S;
    var man = el('g', { fill: '#5a4a44' }, svg);
    el('circle', { cx: px, cy: fy - ph + 12, r: 12 }, man);
    el('path', { d: 'M' + (px - 16) + ' ' + (fy - ph + 30) + 'h32l5 70h-8l-4 -46v120h-9l-3 -66l-3 66h-9v-120l-4 46h-8z' }, man);
    dim(svg, px - 40, fy - ph, fy, '1,8 м', true);
    dim(svg, sx + sw + 40, fy, bot, fmt(depth) + ' м');
    return svg;
  }
  function dim(svg, x, y1, y2, label, left) {
    var g = el('g', { stroke: '#a3958e', 'stroke-width': 1 }, svg);
    el('line', { x1: x, y1: y1, x2: x, y2: y2 }, g);
    el('line', { x1: x - 6, y1: y1, x2: x + 6, y2: y1 }, g);
    el('line', { x1: x - 6, y1: y2, x2: x + 6, y2: y2 }, g);
    var t = el('text', { x: left ? x - 10 : x + 10, 'text-anchor': left ? 'end' : 'start', y: (y1 + y2) / 2 + 5, fill: '#f2ebe3', 'font-size': 16, 'font-family': 'Golos Text, sans-serif' }, svg);
    t.textContent = label;
  }
  function fmt(d) { return (Math.round(d * 100) / 100).toString().replace('.', ','); }

  /* ---------- отрисовка ---------- */
  var cur = null, shownDepth = null, raf = 0, open = false, openT = 0;
  function render(depth) {
    var c = cur;
    pit.innerHTML = ''; pit.appendChild(drawPit(c, depth));
    cut.innerHTML = ''; cut.appendChild(drawCut(c, depth, open));
  }
  function animateDepth(to) {
    cancelAnimationFrame(raf);
    var from = shownDepth == null ? to : shownDepth, t0 = performance.now();
    if (from === to || matchMedia('(prefers-reduced-motion: reduce)').matches) { shownDepth = to; render(to); return; }
    (function tick(t) {
      var p = Math.min(1, (t - t0) / 650), e = 1 - Math.pow(1 - p, 3);
      shownDepth = from + (to - from) * e; render(shownDepth);
      if (p < 1) raf = requestAnimationFrame(tick);
    })(t0);
  }
  function setOpen(v) {
    open = v;
    stage.classList.toggle('is-open', v);
    var b = document.getElementById('kzOpen');
    b.setAttribute('aria-pressed', v ? 'true' : 'false');
    document.getElementById('kzOpenT').textContent = v ? 'Закрыть люк' : 'Открыть люк';
    if (cur) render(shownDepth);
  }

  function labelOf(name, val) {
    var inp = form.querySelector('input[name="' + name + '"][value="' + val + '"]');
    return inp ? inp.closest('label').querySelector('b').textContent : val;
  }
  function summary(c) {
    var rows = [];
    form.querySelectorAll('fieldset').forEach(function (fs) {
      var name = fs.id.replace('kz-', ''), title = fs.querySelector('legend').childNodes[1].textContent;
      var v = name === 'extra' ? c.extra.map(function (x) { return labelOf('extra', x); }).join(', ') : labelOf(name, c[name]);
      rows.push([title, v || 'нет']);
    });
    return rows;
  }
  function textOf(rows) {
    return 'Конфигурация погреба с сайта:\n' + rows.map(function (r) { return r[0] + ': ' + r[1]; }).join('\n');
  }

  function update(changed) {
    var prev = cur;
    cur = readForm();
    // смена механизма или формы: старый люк мгновенно закрываем без анимации,
    // иначе одновременно играют закрытие старого механизма и открытие нового
    var swap = changed === 'mech' || changed === 'shape';
    if (swap) {
      clearTimeout(openT);
      stage.classList.add('kz-instant');
      stage.classList.remove('is-open');
      open = false;
    }
    stage.dataset.shape = cur.shape;
    stage.dataset.mech = cur.mech;
    stage.style.setProperty('--kz-glass', GLASS[cur.glass]);
    // фото вживую
    var mp = MECH_PHOTO[cur.mech];
    var fig = document.getElementById('kzLiveMechFig'), hasV = !!MECH_VIDEO[cur.mech];
    fig.classList.toggle('has-video', hasV);
    if (hasV) { fig.setAttribute('role', 'button'); fig.tabIndex = 0; } else { fig.removeAttribute('role'); fig.removeAttribute('tabindex'); }
    document.getElementById('kzLiveMechK').textContent = hasV ? 'Механизм вживую · смотреть видео' : 'Механизм вживую · видео скоро';
    var mi = document.getElementById('kzLiveMech');
    if (mi.getAttribute('src') !== mp[0]) { mi.src = mp[0]; }
    mi.alt = mp[1];
    document.getElementById('kzLiveMechT').textContent = labelOf('mech', cur.mech);
    var ci = document.getElementById('kzLiveCtrl');
    if (ci.getAttribute('src') !== CTRL_PHOTO[cur.ctrl]) ci.src = CTRL_PHOTO[cur.ctrl];
    ci.alt = labelOf('ctrl', cur.ctrl);
    document.getElementById('kzLiveCtrlT').textContent = labelOf('ctrl', cur.ctrl);
    // итог
    var rows = summary(cur), dl = document.getElementById('kzSumList');
    dl.innerHTML = rows.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + r[1] + '</dd></div>'; }).join('');
    var text = textOf(rows);
    document.getElementById('kzSend').href = 'contacts.html?cfg=' + encodeURIComponent(text);
    form.dataset.text = text;
    // адрес страницы, чтобы сборкой можно было поделиться
    var q = new URLSearchParams();
    ['shape', 'mech', 'glass', 'depth', 'wood', 'ctrl'].forEach(function (k) { q.set(k, cur[k]); });
    if (cur.extra.length) q.set('extra', cur.extra.join(','));
    try { history.replaceState(null, '', '?' + q.toString()); } catch (e) {}
    // смена механизма: сразу показываем, как он открывается
    if (swap) {
      void stage.offsetWidth;
      stage.classList.remove('kz-instant');
      setOpen(false);
      openT = setTimeout(function () { setOpen(true); }, 120);
    }
    if (changed === 'depth' || !prev) animateDepth(cur.depthN); else render(shownDepth);
    pit.classList.remove('kz-fade'); void pit.offsetWidth; pit.classList.add('kz-fade');
  }

  form.addEventListener('change', function (e) { update(e.target.name); });
  document.getElementById('kzOpen').addEventListener('click', function () { clearTimeout(openT); setOpen(!open); });
  stage.querySelectorAll('.kz-tabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      stage.querySelectorAll('.kz-tabs button').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
      stage.querySelectorAll('.kz-view').forEach(function (v) { v.classList.toggle('is-on', v.dataset.view === b.dataset.view); });
    });
  });
  document.getElementById('kzCopy').addEventListener('click', function () {
    var t = form.dataset.text, done = function () { toast('Конфигурация скопирована'); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function () { fallback(t); done(); });
    else { fallback(t); done(); }
  });
  function fallback(t) {
    var ta = document.createElement('textarea'); ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} ta.remove();
  }
  function toast(msg) {
    var t = document.getElementById('toast'); if (!t) return;
    t.textContent = msg; t.classList.add('is-on'); setTimeout(function () { t.classList.remove('is-on'); }, 2200);
  }

  /* видео механизма во весь экран */
  var lb = document.getElementById('kzLb'), lbv = document.getElementById('kzLbV'), lastFocus = null;
  function openLb() {
    var v = MECH_VIDEO[cur.mech]; if (!v) return;
    lastFocus = document.activeElement;
    lbv.poster = v[0].replace('.mp4', '-poster.jpg'); lbv.src = v[0]; document.getElementById('kzLbCap').textContent = v[1];
    lb.hidden = false; document.documentElement.classList.add('kz-lock');
    var pr = lbv.play(); if (pr && pr.catch) pr.catch(function () {});
    document.getElementById('kzLbX').focus();
  }
  function closeLb() {
    lb.hidden = true; lbv.pause(); lbv.removeAttribute('src'); lbv.load();
    document.documentElement.classList.remove('kz-lock');
    if (lastFocus) lastFocus.focus();
  }
  var mfig = document.getElementById('kzLiveMechFig');
  mfig.addEventListener('click', function () { if (mfig.classList.contains('has-video')) openLb(); });
  mfig.addEventListener('keydown', function (e) { if ((e.key === 'Enter' || e.key === ' ') && mfig.classList.contains('has-video')) { e.preventDefault(); openLb(); } });
  document.getElementById('kzLbX').addEventListener('click', closeLb);
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) closeLb(); });

  applyParams();
  update();
  openT = setTimeout(function () { setOpen(true); }, 900);
})();
