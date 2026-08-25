/* SaaScend — site.js
   Progressive enhancement. Every resting visual state is defined in CSS.

   Motion policy (Apple's fluid-interface rules, translated to the web):
   • Predetermined, non-interruptible motion (scroll reveals, the hero stack
     assembling on load) stays in CSS — it runs off the main thread and keeps
     its frames while the page is still loading.
   • Anything a user can grab, press, or spam — the nav sheet, the stack
     layers, the marketplace filter — is spring-driven via Motion, because
     springs animate from the CURRENT on-screen value and can be re-targeted
     mid-flight without a jump.
   • Apple's two parameters, not mass/stiffness/damping:
       damping 1.0 / response 0.4  → { bounce: 0,   duration: 0.4 }  reposition
       damping 0.8 / response 0.3  → { bounce: 0.2, duration: 0.3 }  drawer
     Bounce is only spent where a real gesture carried momentum.
*/
(function () {
  'use strict';

  var M = window.Motion || {};
  var animate = M.animate;
  var hasMotion = typeof animate === 'function';
  /* Live, not read-once — someone can flip the OS setting mid-session. */
  var reduceMQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  var reduce = reduceMQ.matches;
  if (reduceMQ.addEventListener) {
    reduceMQ.addEventListener('change', function (e) { reduce = e.matches; });
  }

  /* Apple's spring presets (Designing Fluid Interfaces). */
  var SPRING_MOVE   = { type: 'spring', bounce: 0,   duration: 0.4 };
  var SPRING_DRAWER = { type: 'spring', bounce: 0.2, duration: 0.3 };
  var CROSSFADE     = { duration: 0.2, ease: [0.23, 1, 0.32, 1] };

  /* Reduced motion means a gentler, non-vestibular equivalent — not nothing. */
  function spring(cfg, velocity) {
    if (reduce) return CROSSFADE;
    if (!velocity) return cfg;
    var out = {};
    for (var k in cfg) out[k] = cfg[k];
    out.velocity = velocity;          // Motion takes absolute px/s
    return out;
  }

  /* Apple's momentum projection — exponential decay, NOT v²/2a.
     Tells you where a flick is GOING, so you snap to that, not to where
     the finger happened to leave the screen. */
  function project(velocity, decelerationRate) {
    var d = decelerationRate || 0.998;
    return (velocity / 1000) * d / (1 - d);
  }

  /* Progressive resistance past a boundary: real things slow before they stop. */
  function rubberband(overshoot, dimension, constant) {
    var c = constant || 0.55;
    return (overshoot * dimension * c) / (dimension + c * Math.abs(overshoot));
  }

  /* Tracks a short position/time history so we have real velocity at release. */
  function VelocityTracker() {
    this.samples = [];
  }
  VelocityTracker.prototype.push = function (v, t) {
    this.samples.push({ v: v, t: t });
    if (this.samples.length > 6) this.samples.shift();
  };
  VelocityTracker.prototype.velocity = function () {
    var s = this.samples;
    if (s.length < 2) return 0;
    var a = s[0], b = s[s.length - 1];
    var dt = b.t - a.t;
    if (dt <= 0) return 0;
    return (b.v - a.v) / dt * 1000;   // px/s
  };

  /* Reads the live on-screen translateY so an interrupted animation restarts
     from the presentation value instead of jumping to the logical one. */
  function currentY(el) {
    var m = new DOMMatrixReadOnly(getComputedStyle(el).transform);
    return m.m42 || 0;
  }

  /* ================= Nav: scroll state ================= */
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 12); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ================= Nav sheet =================
     A top sheet, so it enters downward and must dismiss upward along the same
     path (spatial consistency). Drag tracks the finger 1:1, rubber-bands past
     the open position, and hands its release velocity to the spring so there
     is no seam between dragging and animating. */
  var burger = document.querySelector('.nav__burger');
  var sheet  = document.querySelector('.nav__panel');
  var scrim  = document.querySelector('.nav__scrim');

  if (burger && sheet && scrim) {
    var open = false, dragging = false, sheetH = 0, startY = 0, offset = 0;
    var track = null, pid = null;

    function setOpen(state) {
      open = state;
      burger.setAttribute('aria-expanded', state ? 'true' : 'false');
      document.body.style.overflow = state ? 'hidden' : '';
    }

    function show() {
      sheet.hidden = false; scrim.hidden = false;
      sheetH = sheet.offsetHeight;
      setOpen(true);
      if (!hasMotion) { sheet.style.transform = 'none'; scrim.style.opacity = '1'; return; }
      animate(sheet, { transform: ['translateY(-100%)', 'translateY(0px)'] }, spring(SPRING_DRAWER));
      animate(scrim, { opacity: [0, 1] }, reduce ? CROSSFADE : { duration: 0.24, ease: [0.23, 1, 0.32, 1] });
    }

    function hide(velocity) {
      setOpen(false);
      if (!hasMotion) { sheet.hidden = true; scrim.hidden = true; return; }
      animate(scrim, { opacity: 0 }, reduce ? CROSSFADE : { duration: 0.2, ease: [0.23, 1, 0.32, 1] });
      animate(sheet, { transform: 'translateY(-100%)' }, spring(SPRING_DRAWER, velocity))
        .finished.then(function () {
          if (!open) { sheet.hidden = true; scrim.hidden = true; sheet.style.transform = ''; }
        });
    }

    burger.addEventListener('click', function () { open ? hide(0) : show(); });
    scrim.addEventListener('click', function () { hide(0); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && open) hide(0);
    });
    sheet.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && !dragging) hide(0);
    });

    /* 1:1 drag with pointer capture, so tracking survives leaving the sheet. */
    sheet.addEventListener('pointerdown', function (e) {
      if (!open || !hasMotion || reduce) return;
      pid = e.pointerId;
      startY = e.clientY;
      offset = currentY(sheet);        // respect where they grabbed from
      track = new VelocityTracker();
      track.push(e.clientY, e.timeStamp);
      dragging = false;
    });

    sheet.addEventListener('pointermove', function (e) {
      if (pid === null || e.pointerId !== pid) return;
      var dy = e.clientY - startY;
      /* ~10px of hysteresis before committing to a drag, so taps still tap. */
      if (!dragging) {
        if (Math.abs(dy) < 10) return;
        dragging = true;
        /* Capture keeps tracking alive when the pointer leaves the sheet.
           It throws if the pointer is already gone — the drag still works. */
        try { sheet.setPointerCapture(pid); } catch (err) {}
        sheet.style.willChange = 'transform';
      }
      track.push(e.clientY, e.timeStamp);
      var y = offset + dy;
      /* Dragging down past open is past the boundary — resist, don't stop hard. */
      if (y > 0) y = rubberband(y, sheetH);
      sheet.style.transform = 'translateY(' + y + 'px)';
    });

    function endDrag(e) {
      if (pid === null || (e && e.pointerId !== pid)) return;
      var wasDragging = dragging;
      try {
        if (sheet.hasPointerCapture && sheet.hasPointerCapture(pid)) {
          sheet.releasePointerCapture(pid);
        }
      } catch (err) {}
      pid = null;
      sheet.style.willChange = '';
      if (!wasDragging) { dragging = false; return; }

      var v = track.velocity();
      var y = currentY(sheet);
      /* Snap to where the gesture is going, and let velocity sign decide the
         commit — a fast upward flick dismisses even from barely-moved. */
      var projected = y + project(v);
      if (v < -320 || projected < -sheetH / 3) hide(v);
      else animate(sheet, { transform: 'translateY(0px)' }, spring(SPRING_DRAWER, v));

      setTimeout(function () { dragging = false; }, 0);
    }
    sheet.addEventListener('pointerup', endDrag);
    sheet.addEventListener('pointercancel', endDrag);
  }

  /* ================= Scroll reveals — CSS, deliberately =================
     Predetermined and never interrupted, so CSS transitions keep their frames
     while the rest of the page is still loading. JS only flips the class. */
  var reveals = document.querySelectorAll('.rv');
  if (reveals.length && 'IntersectionObserver' in window) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); ro.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { ro.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* The stack assembles bottom-up — foundation first, agents last. Also CSS:
     it fires during load, exactly when a JS animation would drop frames. */
  document.querySelectorAll('.layers').forEach(function (group) {
    group.querySelectorAll('.layer').forEach(function (l, i) {
      l.style.setProperty('--d', (reduce ? 0 : i * 95) + 'ms');
    });
    var fire = function () { group.classList.add('is-in'); };
    if ('IntersectionObserver' in window) {
      var o = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { fire(); o.disconnect(); }
      }, { threshold: 0.15 });
      o.observe(group);
    } else { fire(); }
  });

  /* ================= THE ARGUMENT — pinned scroll sequence =================
     The one orchestrated motion on the site. Scroll drives the assembly of the
     stack bottom-up: each step builds one layer and swaps the copy beside it.
     Position is read from scroll, so the motion is scrubbable in both
     directions and cannot desync from where the user actually is — no
     fire-once reveal, no animation the user can outrun.
     With no JS, or reduced motion, every step is shown stacked and every
     layer is already built. */
  var seq = document.querySelector('[data-seq]');
  if (seq) {
    var track = seq.querySelector('.seq__track');
    var steps = [].slice.call(seq.querySelectorAll('.seq__step'));
    var plates = [].slice.call(seq.querySelectorAll('.plate'));
    var total = steps.length;
    var last = -1;
    var queued = false;

    var paint = function () {
      queued = false;
      var r = track.getBoundingClientRect();
      var span = r.height - window.innerHeight;
      if (span <= 0) return;
      var p = (-r.top) / span;
      p = p < 0 ? 0 : (p > 1 ? 1 : p);
      /* Bias so the last step gets a full hold rather than a single frame. */
      var i = Math.floor(p * total);
      if (i > total - 1) i = total - 1;
      if (i === last) return;
      last = i;
      steps.forEach(function (el, n) { el.classList.toggle('is-live', n === i); });
      plates.forEach(function (el, n) {
        el.classList.toggle('is-built', n <= i);
        el.classList.toggle('is-current', n === i);
      });
    };

    var onScroll = function () {
      if (queued) return;
      queued = true;
      window.requestAnimationFrame(paint);
    };
    paint();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
  }

  /* ================= Stack layers: spring accordion =================
     Spammable, so it must be interruptible: Motion re-targets from the live
     height and the chevron carries the same spring, no velocity brick wall.
     height is the sanctioned exception — an accordion has no transform
     equivalent. */
  document.querySelectorAll('[data-layer]').forEach(function (layer) {
    var more = layer.querySelector('[data-layer-more]');
    var chev = layer.querySelector('[data-layer-chev]');
    if (!more) return;
    var isOpen = false;

    layer.addEventListener('click', function () {
      isOpen = !isOpen;
      layer.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      layer.classList.toggle('is-open', isOpen);

      var target = isOpen ? more.scrollHeight : 0;

      if (!hasMotion) { more.style.height = target ? 'auto' : '0px'; return; }
      animate(more, { height: target + 'px', opacity: isOpen ? 1 : 0 }, spring(SPRING_MOVE));
      if (chev) animate(chev, { transform: 'rotate(' + (isOpen ? 180 : 0) + 'deg)' }, spring(SPRING_MOVE));
    });
  });

  /* ================= Agent marketplace ================= */
  var grid = document.querySelector('[data-agents]');
  if (grid && window.SAASCEND_AGENTS) {
    var agents = window.SAASCEND_AGENTS;
    var teams = ['All', 'Sales', 'Marketing', 'Customer Success', 'Revenue Operations'];
    var esc = function (s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    };

    grid.innerHTML = agents.map(function (a) {
      return '<article class="agent" data-team="' + esc(a.team) + '">' +
        '<div class="agent__team">' + esc(a.team) + '</div>' +
        '<h3 class="t-h4">' + esc(a.name) + '</h3>' +
        '<p class="t-body">' + esc(a.desc) + '</p>' +
        '<div class="chips">' + a.stack.map(function (s) {
          return '<span class="chip">' + esc(s) + '</span>';
        }).join('') + '</div>' +
        '<div class="agent__gain">' + esc(a.gain) + '</div>' +
        '</article>';
    }).join('');

    var bar = document.querySelector('[data-agent-filters]');
    var count = document.querySelector('[data-agent-count]');
    var setCount = function (n, team) {
      if (count) {
        count.textContent = n + (n === 1 ? ' agent' : ' agents') +
          (team === 'All' ? ' across 4 GTM teams' : ' for ' + team);
      }
    };

    if (bar) {
      bar.innerHTML = teams.map(function (t) {
        var n = t === 'All' ? agents.length : agents.filter(function (a) { return a.team === t; }).length;
        return '<button class="filter' + (t === 'All' ? ' is-on' : '') + '" data-team="' + esc(t) + '">' +
          esc(t) + '<span class="filter__n">' + n + '</span></button>';
      }).join('');

      bar.addEventListener('click', function (e) {
        var btn = e.target.closest('.filter');
        if (!btn) return;
        var team = btn.dataset.team;
        bar.querySelectorAll('.filter').forEach(function (b) { b.classList.toggle('is-on', b === btn); });

        var shown = 0, i = 0;
        grid.querySelectorAll('.agent').forEach(function (card) {
          var on = team === 'All' || card.dataset.team === team;
          card.hidden = !on;
          if (!on) return;
          shown++;
          /* Short, capped stagger. Filtering is frequent enough that a long
             entrance would read as lag, so it stays under 300ms. */
          if (hasMotion && !reduce) {
            animate(card,
              { opacity: [0, 1], transform: ['translateY(8px)', 'translateY(0px)'] },
              { type: 'spring', bounce: 0, duration: 0.28, delay: Math.min(i, 8) * 0.018 });
          }
          i++;
        });
        setCount(shown, team);
      });
    }
    setCount(agents.length, 'All');
  }

  /* ================= Maturity check ================= */
  var quiz = document.querySelector('[data-quiz]');
  if (quiz) {
    var QS = [
      { q: 'Do you trust the forecast number in your CRM?',
        a: ['No — we run off spreadsheets', 'Sometimes, with caveats', 'Mostly', "Fully — it's the source of truth"] },
      { q: 'How connected are your GTM systems?',
        a: ['Siloed — data lives everywhere', 'A few integrations', 'Mostly connected', 'One trusted source of truth'] },
      { q: 'Is your automation documented and owned?',
        a: ["We don't know what runs", 'Partially', 'Mostly', 'Fully documented and owned'] },
      { q: 'How much time do reps lose to manual CRM admin?',
        a: ['Hours every day', 'A significant chunk', 'Some', 'Very little'] },
      { q: 'Have you deployed AI agents in your GTM stack?',
        a: ['None yet', 'Experimenting', 'A few in production', 'Several, orchestrated'] },
      { q: 'Can you measure the ROI of your GTM operations?',
        a: ['Not really', 'Roughly', 'Mostly', 'Precisely'] }
    ];
    var STAGES = [
      { max: 4,  name: 'Implement', move: 'Rebuild the data model before anything else. Until the schema is deliberate, every automation and every agent inherits the same ambiguity.', agents: ['Enrichment Agent', 'Lead Qualification Agent', 'Call Transcription Agent'] },
      { max: 9,  name: 'Manage', move: 'Put a single owner on the foundation. Documented automation and clear ownership are what turn a working org into an operable one.', agents: ['Call Transcription Agent', 'Data Analysis Agent', 'Customer Health Agent'] },
      { max: 13, name: 'Automate', move: 'Remove the mechanical work first — routing, hygiene, follow-up — so the agent layer lands on a process that already behaves.', agents: ['Deal Forecasting Agent', 'Account Research Agent', 'Ops Questions Agent'] },
      { max: 18, name: 'AI Workforce', move: 'Your foundation can carry orchestration. Move from isolated agents to a master orchestration layer holding context across the whole stack.', agents: ['Deal Forecasting Agent', 'Churn Risk Agent', 'Outbound BDR Agent'] }
    ];

    var i = 0, score = 0;
    var qEl = quiz.querySelector('[data-quiz-q]');
    var oEl = quiz.querySelector('[data-quiz-opts]');
    var nEl = quiz.querySelector('[data-quiz-n]');
    var fEl = quiz.querySelector('[data-quiz-fill]');
    var rEl = quiz.querySelector('[data-quiz-res]');
    var bEl = quiz.querySelector('[data-quiz-body]');

    /* Questions advance in place, so the swap gets a short cross-fade —
       enough to stop content teleporting, not enough to feel like a wait. */
    function enter(el) {
      if (!hasMotion || reduce) return;
      animate(el, { opacity: [0, 1], transform: ['translateY(6px)', 'translateY(0px)'] },
        { type: 'spring', bounce: 0, duration: 0.26 });
    }

    var render = function () {
      var item = QS[i];
      qEl.textContent = (i + 1) + '. ' + item.q;
      nEl.textContent = i + '/' + QS.length;
      fEl.style.width = (i / QS.length * 100) + '%';
      oEl.innerHTML = item.a.map(function (t, n) {
        return '<button class="quiz__opt" data-v="' + n + '">' + t + '</button>';
      }).join('');
      enter(bEl);
    };

    var finish = function () {
      var s = STAGES.find(function (st) { return score <= st.max; });
      nEl.textContent = QS.length + '/' + QS.length;
      fEl.style.width = '100%';
      bEl.style.display = 'none';
      rEl.classList.add('is-on');
      rEl.innerHTML =
        '<div class="t-sys">Your stage</div>' +
        '<div class="quiz__stage" style="margin-top:8px">' + s.name + '</div>' +
        '<p class="t-body" style="margin-top:20px;max-width:56ch">' + s.move + '</p>' +
        '<div class="t-sys" style="margin-top:28px">Start with these agents</div>' +
        '<div class="chips" style="margin-top:12px">' + s.agents.map(function (a) {
          return '<span class="chip">' + a + '</span>';
        }).join('') + '</div>' +
        '<div class="btn-row" style="margin-top:32px">' +
        '<a class="btn btn--cyan" href="contact.html">Scope this with an architect</a>' +
        '<button class="btn btn--ghost-dark" data-quiz-reset>Start over</button>' +
        '</div>';
      enter(rEl);
    };

    oEl.addEventListener('click', function (e) {
      var b = e.target.closest('.quiz__opt');
      if (!b) return;
      score += parseInt(b.dataset.v, 10);
      i++;
      if (i >= QS.length) finish(); else render();
    });

    rEl.addEventListener('click', function (e) {
      if (!e.target.closest('[data-quiz-reset]')) return;
      i = 0; score = 0;
      rEl.classList.remove('is-on');
      rEl.innerHTML = '';
      bEl.style.display = '';
      render();
    });

    render();
  }

  /* ================= Contact form ================= */
  var form = document.querySelector('[data-scope-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var body = [
        'Name: ' + (d.get('name') || ''),
        'Company: ' + (d.get('company') || ''),
        'Email: ' + (d.get('email') || ''),
        'Current stack: ' + (d.get('stack') || ''),
        'Stage: ' + (d.get('stage') || ''),
        '',
        d.get('detail') || ''
      ].join('\n');
      window.location.href = 'mailto:hello@saascend.com' +
        '?subject=' + encodeURIComponent('Scope a project — ' + (d.get('company') || d.get('name') || 'new enquiry')) +
        '&body=' + encodeURIComponent(body);
    });
  }
})();
