/* SaaScend — site.js
   Progressive enhancement only. Every resting visual state is defined in CSS;
   JS adds motion, filtering, and the maturity check on top. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Nav: scroll state + mobile panel ---- */
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-scrolled', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  var burger = document.querySelector('.nav__burger');
  var panel = document.querySelector('.nav__panel');
  if (burger && panel) {
    burger.addEventListener('click', function () {
      var open = panel.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    panel.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        panel.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- Reveal on scroll ---- */
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

  /* ---- The stack assembles bottom-up: foundation first, agents last.
          Source order is L1..L5; CSS reverses it visually. ---- */
  document.querySelectorAll('.layers').forEach(function (group) {
    var layers = group.querySelectorAll('.layer');
    layers.forEach(function (l, i) {
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

  /* ---- Agent marketplace ---- */
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
        var shown = 0;
        grid.querySelectorAll('.agent').forEach(function (card) {
          var on = team === 'All' || card.dataset.team === team;
          card.hidden = !on;
          if (on) shown++;
        });
        setCount(shown, team);
      });
    }
    setCount(agents.length, 'All');
  }

  /* ---- Maturity check ---- */
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

    var render = function () {
      var item = QS[i];
      qEl.textContent = (i + 1) + '. ' + item.q;
      nEl.textContent = i + '/' + QS.length;
      fEl.style.width = (i / QS.length * 100) + '%';
      oEl.innerHTML = item.a.map(function (t, n) {
        return '<button class="quiz__opt" data-v="' + n + '">' + t + '</button>';
      }).join('');
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

  /* ---- Contact form: static site, so hand off to the real inbox ---- */
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
