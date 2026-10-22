(function(){
  /* always open a new page at the top (also inside preview frames) */
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch(e) {}
  if (!location.hash) { window.scrollTo(0, 0); try { document.documentElement.scrollIntoView({ block: 'start' }); } catch(e) {} }
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  var lenis = null;

  /* smooth scroll */
  if (!reduce && typeof window.Lenis !== 'undefined') {
    try {
      lenis = new Lenis({ lerp: 0.085, smoothWheel: true });
      if (hasGsap) {
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add(function(t){ lenis.raf(t * 1000); });
        gsap.ticker.lagSmoothing(0);
      } else {
        (function raf(t){ lenis.raf(t); requestAnimationFrame(raf); })(0);
      }
    } catch(e) { lenis = null; }
  }

  /* header + mobile nav */
  var head = document.querySelector('.site-head');
  function onScroll(){ head.classList.toggle('is-solid', (window.scrollY || 0) > 40); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var burger = document.querySelector('.burger');
  function setMenu(open){
    document.documentElement.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    if (lenis) { open ? lenis.stop() : lenis.start(); }
  }
  burger.addEventListener('click', function(){ setMenu(!document.documentElement.classList.contains('menu-open')); });

  /* anchor links */
  document.querySelectorAll('a[data-scroll]').forEach(function(a){
    a.addEventListener('click', function(e){
      var id = a.getAttribute('href');
      if (!id || id.charAt(0) !== '#') return;
      var el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      setMenu(false);
      if (lenis) lenis.scrollTo(el, { offset: id === '#top' ? 0 : -80, duration: 1.6 });
      else el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  /* play videos only while visible */
  var vids = document.querySelectorAll('video');
  if ('IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        var v = en.target;
        if (en.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function(){}); }
        else v.pause();
      });
    }, { threshold: 0.15 });
    vids.forEach(function(v){ v.muted = true; vio.observe(v); });
  }

  /* motion */
  if (hasGsap && !reduce) {
    gsap.registerPlugin(ScrollTrigger);

    if (document.querySelector('.hero h1 .ln')) gsap.from('.hero h1 .ln > span', { yPercent: 105, duration: 1.4, ease: 'expo.out', stagger: 0.09, delay: 0.1 });
    var hImg = document.getElementById('heroImg');
    if (hImg) {
      var hSec = hImg.closest('section');
      gsap.fromTo(hImg, { scale: 1.12 }, { scale: 1, duration: 2.8, ease: 'expo.out' });
      gsap.to(hImg, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: hSec, start: 'top top', end: 'bottom top', scrub: true } });
    }
    gsap.utils.toArray('.page-hero h1, .page-hero .page-lead').forEach(function(el, i){ gsap.from(el, { y: 36, duration: 1.3, ease: 'expo.out', delay: 0.05 + i * 0.08 }); });

    /* the iris: the hatch opens into the cellar */
    var mm = gsap.matchMedia();
    if (document.getElementById('irisStage'))
    mm.add({ desk: '(min-width: 701px)', mob: '(max-width: 700px)' }, function(ctx){
      var startR = ctx.conditions.desk ? 22 : 34;
      var cy = ctx.conditions.desk ? 50 : 42;
      var tl = gsap.timeline({
        scrollTrigger: { trigger: '#irisStage', start: 'top top', end: '+=140%', scrub: 1, pin: true, anticipatePin: 1 }
      });
      tl.fromTo('#irisMedia', { clipPath: 'circle(' + startR + '% at 50% ' + cy + '%)' }, { clipPath: 'circle(80% at 50% 50%)', ease: 'none' }, 0)
        .fromTo('#irisImg', { scale: 1.35, rotate: -28 }, { scale: 1, rotate: 0, ease: 'none' }, 0)
        .fromTo('#irisShade', { opacity: 0.2 }, { opacity: 1, ease: 'none' }, 0)
        .fromTo('.iris-copy h2', { y: 40 }, { y: 0, ease: 'none' }, 0);
    });

    /* gentle drift on large images */
    gsap.utils.toArray('.sea-bg video').forEach(function(el){
      gsap.fromTo(el, { yPercent: -6, scale: 1.12 }, { yPercent: 6, scale: 1.12, ease: 'none', scrollTrigger: { trigger: el.closest('.sea'), start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    if (document.querySelector('.reward-v')) gsap.from('.reward-v', { yPercent: 30, duration: 1.6, ease: 'expo.out', scrollTrigger: { trigger: '.band', start: 'top 70%' } });

    window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
  }

  /* cross-section focus */
  var svg = document.querySelector('.xs');
  var items = document.querySelectorAll('#parts li');
  function focusPart(name){
    if (!svg) return;
    svg.classList.toggle('is-focus', !!name);
    svg.querySelectorAll('.part').forEach(function(p){ p.classList.toggle('is-on', p.dataset.part === name); });
    svg.querySelectorAll('.hs').forEach(function(h){ h.classList.toggle('is-on', h.dataset.part === name); });
    items.forEach(function(li){ li.classList.toggle('is-on', li.dataset.part === name); });
  }
  items.forEach(function(li){
    li.addEventListener('mouseenter', function(){ focusPart(li.dataset.part); });
    li.addEventListener('mouseleave', function(){ focusPart(null); });
    li.addEventListener('click', function(){ focusPart(li.dataset.part); });
  });
  if (svg) svg.querySelectorAll('.hs').forEach(function(h){
    h.addEventListener('mouseenter', function(){ focusPart(h.dataset.part); });
    h.addEventListener('mouseleave', function(){ focusPart(null); });
    h.addEventListener('focus', function(){ focusPart(h.dataset.part); });
    h.addEventListener('blur', function(){ focusPart(null); });
    h.addEventListener('click', function(){ focusPart(h.dataset.part); });
    h.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); focusPart(h.dataset.part); } });
  });

  /* drag-to-scroll gallery */
  document.querySelectorAll('.strip').forEach(function(strip){
  if (strip) {
    var down = false, sx = 0, sl = 0, moved = false;
    strip.addEventListener('pointerdown', function(e){ if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = strip.scrollLeft; strip.classList.add('is-drag'); strip.setPointerCapture(e.pointerId); });
    strip.addEventListener('pointermove', function(e){ if (!down) return; var dx = e.clientX - sx; if (Math.abs(dx) > 3) moved = true; strip.scrollLeft = sl - dx; });
    function up(){ if (!down) return; down = false; strip.classList.remove('is-drag'); }
    strip.addEventListener('pointerup', up); strip.addEventListener('pointercancel', up);
    strip.addEventListener('wheel', function(e){ if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) e.stopPropagation(); }, { passive: true });
    strip.setAttribute('data-lenis-prevent-horizontal', '');
    var items = strip.querySelectorAll('figure');
    if (items.length > 1) {
      var nav = document.createElement('div'); nav.className = 'strip-nav';
      nav.innerHTML = '<button type="button" class="strip-btn" aria-label="Предыдущее фото">←</button><span class="strip-count"><b>1</b> / ' + items.length + ' фото</span><button type="button" class="strip-btn" aria-label="Следующее фото">→</button>';
      strip.parentNode.insertBefore(nav, strip.nextSibling);
      var hint = nav.nextElementSibling; if (hint && hint.classList.contains('strip-hint')) hint.style.display = 'none';
      var btns = nav.querySelectorAll('button'), cur = nav.querySelector('b');
      var idx = function(){ var best = 0, d = 1e9; for (var i = 0; i < items.length; i++) { var x = Math.abs(items[i].offsetLeft - strip.offsetLeft - strip.scrollLeft); if (x < d) { d = x; best = i; } } return best; };
      var go = function(k){ var i = Math.max(0, Math.min(items.length - 1, idx() + k)); strip.scrollTo({ left: items[i].offsetLeft - strip.offsetLeft, behavior: reduce ? 'auto' : 'smooth' }); };
      btns[0].addEventListener('click', function(){ go(-1); });
      btns[1].addEventListener('click', function(){ go(1); });
      var upd = function(){ var i = idx(); cur.textContent = i + 1; btns[0].disabled = i === 0; btns[1].disabled = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 4; };
      strip.addEventListener('scroll', function(){ window.requestAnimationFrame(upd); }, { passive: true });
      upd();
    }
  }
  });

  /* FAQ: open one at a time with a height animation */
  document.querySelectorAll('.faq details').forEach(function(d){
    var s = d.querySelector('summary'), a = d.querySelector('.ans');
    s.addEventListener('click', function(e){
      if (reduce || !a.animate) return;
      e.preventDefault();
      if (d.open) {
        var h = a.offsetHeight;
        a.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 420, easing: 'cubic-bezier(.2,.7,.1,1)' }).onfinish = function(){ d.open = false; if (hasGsap) ScrollTrigger.refresh(); };
      } else {
        d.open = true;
        var h2 = a.offsetHeight;
        a.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }], { duration: 520, easing: 'cubic-bezier(.2,.7,.1,1)' }).onfinish = function(){ if (hasGsap) ScrollTrigger.refresh(); };
      }
    });
    d.querySelector('.ans').style.overflow = 'hidden';
  });

  /* сборка из конструктора попадает в поле пожеланий */
  try {
    var cfgQ = new URLSearchParams(location.search).get('cfg'), fMsg = document.getElementById('f-msg');
    if (cfgQ && fMsg && !fMsg.value) fMsg.value = cfgQ;
  } catch (e) {}

  /* toast + copy */
  var toast = document.getElementById('toast'), tt;
  function say(msg){ toast.textContent = msg; toast.classList.add('is-on'); clearTimeout(tt); tt = setTimeout(function(){ toast.classList.remove('is-on'); }, 2200); }
  function copyText(text, okMsg){
    function fallback(){
      var ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      var ok = false; try { ok = document.execCommand('copy'); } catch(e) {}
      document.body.removeChild(ta);
      say(ok ? okMsg : 'Выделите текст и скопируйте вручную');
    }
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function(){ say(okMsg); }, fallback);
      else fallback();
    } catch(e) { fallback(); }
  }
  document.querySelectorAll('.copy').forEach(function(b){ b.addEventListener('click', function(){ copyText(b.dataset.copy, 'Скопировано'); }); });

  /* lead form */
  var form = document.getElementById('leadForm');
  if (form) {
  if (form.dataset.role === 'architect') { var ra = document.getElementById('r-arch'); if (ra) ra.checked = true; }
  var body = document.getElementById('formBody'), done = document.getElementById('formDone'), out = document.getElementById('leadText');
  function val(id){ return (document.getElementById(id).value || '').trim(); }
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var ok = true;
    var name = val('f-name'), phone = val('f-phone');
    document.getElementById('e-name').textContent = name ? '' : 'Напишите, как к вам обращаться';
    var digits = phone.replace(/\D/g, '');
    document.getElementById('e-phone').textContent = digits.length >= 10 ? '' : 'Укажите телефон, минимум 10 цифр';
    if (!name || digits.length < 10) ok = false;
    if (!ok) { (name ? document.getElementById('f-phone') : document.getElementById('f-name')).focus(); return; }
    var role = (form.querySelector('input[name="role"]:checked') || {}).value || '';
    var lines = ['Заявка на винный погреб', 'Кто: ' + role, 'Имя: ' + name, 'Телефон: ' + phone];
    if (val('f-city')) lines.push('Город: ' + val('f-city'));
    lines.push('Объект: ' + val('f-stage'));
    if (val('f-msg')) lines.push('Пожелания: ' + val('f-msg'));
    out.textContent = lines.join('\n');
    body.hidden = true; done.hidden = false;
    if (hasGsap) ScrollTrigger.refresh();
  });
  document.getElementById('copyLead').addEventListener('click', function(){ copyText(out.textContent, 'Заявка скопирована'); });
  document.getElementById('editLead').addEventListener('click', function(){ done.hidden = true; body.hidden = false; document.getElementById('f-name').focus(); });
  }

  /* page transitions between site pages */
  var curtain = document.createElement('div'); curtain.className = 'curtain'; curtain.setAttribute('aria-hidden', 'true'); document.body.appendChild(curtain);
  window.addEventListener('pageshow', function(){ curtain.classList.remove('is-on'); });
  document.querySelectorAll('a[href$=".html"]').forEach(function(a){
    a.addEventListener('click', function(e){
      if (reduce || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
      e.preventDefault(); setMenu(false);
      curtain.classList.add('is-on');
      var href = a.getAttribute('href');
      setTimeout(function(){ window.location.href = href; }, 420);
    });
  });
})();
