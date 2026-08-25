# -*- coding: utf-8 -*-
"""Home page body."""

# The signature: five load-bearing layers. Source order is L1..L5 (foundation
# first); CSS reverses it so it reads bottom-up on screen and assembles in
# that order — which is the argument the company actually makes.
LAYERS = [
    ("L1", "Systems &amp; data",   "Salesforce, HubSpot, warehouse &mdash; one data model the business trusts.",
     ["Data model", "Field governance", "Migrations", "Dedupe"], False),
    ("L2", "Integrations",         "Observable data flow between systems, not point-to-point guesswork.",
     ["Named credentials", "Platform events", "Observable sync"], False),
    ("L3", "Automation",           "Documented, single-owner automation with defined guardrails.",
     ["Flows", "Apex", "Single-writer rules", "Guardrails"], False),
    ("L4", "Orchestration",        "A master agent that holds context and routes work across the stack.",
     ["Context store", "Routing", "Approvals", "Audit trail"], False),
    ("L5", "Agent workforce",      "33 specialised agents doing real GTM work, with human approval on consequential actions.",
     ["33 agents", "4 GTM teams", "Human in the loop"], True),
]

def stackfig():
    rows = "".join(
        '<button class="layer{cls}" type="button" aria-expanded="false" data-layer>'
        '<div class="layer__id">{k}</div>'
        '<div class="layer__main">'
        '<div class="layer__name">{n}</div>'
        '<div class="layer__note">{d}</div>'
        '<div class="layer__more" data-layer-more><div class="chips">{c}</div></div>'
        '</div>'
        '<svg class="layer__chev" data-layer-chev width="14" height="14" viewBox="0 0 14 14" '
        'fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<path d="M3 5.5 7 9.5l4-4"/></svg>'
        '</button>'.format(
            cls=" layer--top" if top else "", k=k, n=n, d=d,
            c="".join('<span class="chip">%s</span>' % x for x in caps))
        for k, n, d, caps, top in LAYERS)
    return """
<figure class="stackfig" style="margin:0">
  <figcaption class="stackfig__cap">
    <span class="t-sys">The GTM stack</span>
    <span class="t-sys" style="color:var(--on-dark-faint)">Tap a layer</span>
  </figcaption>
  <div class="layers">{rows}</div>
  <div class="stackfig__foot">
    Every layer is load-bearing. <b>AI sits at the top</b> &mdash; which is why we build
    upward from L1 and never the other way round.
  </div>
</figure>""".format(rows=rows)

PARTNERS = [
    ("Salesforce", "Global Strategic Agreement partner &mdash; multi-cloud engineering with top-tier product access."),
    ("HubSpot",    "Solutions partner &mdash; marketing, sales and service on one source of truth."),
    ("Anthropic",  "We build revenue agents on Claude, deployed with governance and human oversight."),
    ("Aircall",    "Voice wired into the CRM, so every conversation becomes routed, logged data."),
]

FAILURES = [
    ("01", "Untrusted data",      "Nobody trusts the CRM, so everyone builds their own version of reality."),
    ("02", "Disconnected systems","Critical information lives across dozens of platforms that don&rsquo;t talk."),
    ("03", "Manual operations",   "Teams spend their time managing process instead of driving growth."),
    ("04", "AI without a floor",  "Agents are only as effective as the systems and data behind them."),
]

PILLARS = [
    ("Build", "Implement and migrate modern GTM systems designed for AI adoption from day one.",
     ["Salesforce", "HubSpot", "Revenue Cloud", "CRM migrations", "Integrations"], "solutions.html"),
    ("Manage", "Operate and continuously optimise the foundation with ongoing managed services.",
     ["Salesforce admin", "HubSpot admin", "RevOps support", "Optimisation", "Data management"], "solutions.html#manage"),
    ("Transform", "Deploy specialised AI agents that automate work and accelerate revenue.",
     ["Orchestration", "Sales agents", "RevOps agents", "Forecasting", "Customer Success"], "solutions.html#transform"),
]

FEATURED = [
    ("Sales", "Deal Forecasting Agent", "Predicts deal outcomes and close timing from pipeline signals, activity patterns and history.", "Reduce forecast variance by up to 25%"),
    ("Sales", "Call Transcription Agent", "Turns a finished call into a logged meeting, new contacts and updated deal fields.", "30&ndash;40 min saved per rep, daily"),
    ("Customer Success", "Churn Risk Agent", "Flags accounts at risk from behavioural, usage and engagement signals.", "Intervene before contracts are at risk"),
    ("Revenue Operations", "Data Analysis Agent", "Finds the trends and performance drivers across the funnel, on demand.", "Days of analysis delivered in minutes"),
    ("Sales", "Outbound BDR Agent", "Researches, prioritises and personalises outbound at rep scale.", "2x pipeline capacity, no new headcount"),
    ("Sales", "Sales Quote Agent", "Generates accurate quotes against your real pricing and approval rules.", "Accurate quotes, zero manual errors"),
]

CASES = [
    ("Global SaaS Scale-up", "B2B SaaS",
     "Rebuilding a stalled Salesforce org into a forecastable revenue engine",
     "The company had outgrown its original build. We re-architected the data model, rebuilt "
     "forecasting, and gave leadership a number they could trust &mdash; then layered a "
     "Forecast Agent on top.",
     [("32%", "faster cycle"), ("1 day &rarr; 1 hr", "to a reconciled report"), ("100%", "automation owned")],
     ["Salesforce", "RevOps", "AI"]),
    ("Series C Fintech", "Financial Services",
     "Migrating a fintech to a unified Salesforce + HubSpot motion",
     "A fintech had outgrown a single-platform setup. We designed a connected architecture "
     "&mdash; Salesforce as system of record, HubSpot driving marketing &mdash; and migrated "
     "without losing pipeline.",
     [("0", "open pipeline lost"), ("3 weeks", "to production"), ("2 &rarr; 1", "systems of record")],
     ["Salesforce", "HubSpot", "Migration"]),
]


def body():
    partners = "".join(
        '<div class="rv"><div class="t-h4" style="color:var(--on-dark)">{n}</div>'
        '<p class="t-small" style="margin-top:8px">{d}</p></div>'.format(n=n, d=d)
        for n, d in PARTNERS)

    failures = "".join(
        '<article class="card card--lift rv"><div class="card__num">{k}</div>'
        '<h3 class="t-h3">{t}</h3><p class="t-body">{d}</p></article>'.format(k=k, t=t, d=d)
        for k, t, d in FAILURES)

    pillars = "".join(
        '<article class="pillar rv"><div class="pillar__k">{k}</div>'
        '<div class="pillar__body"><h3 class="t-h2" style="color:var(--navy)">{t}</h3>'
        '<p class="t-lead" style="max-width:54ch">{d}</p>'
        '<div class="chips">{c}</div>'
        '<a class="tlink" href="{h}">Explore {t} <span class="arw">&rarr;</span></a>'
        '</div></article>'.format(
            k="0%d" % (i + 1), t=t, d=d, h=h,
            c="".join('<span class="chip">%s</span>' % x for x in items))
        for i, (t, d, items, h) in enumerate(PILLARS))

    featured = "".join(
        '<article class="agent rv"><div class="agent__team">{tm}</div>'
        '<h3 class="t-h4">{n}</h3><p class="t-body">{d}</p>'
        '<div class="agent__gain">{g}</div></article>'.format(tm=tm, n=n, d=d, g=g)
        for tm, n, d, g in FEATURED)

    cases = "".join(
        '<article class="card card--lift rv" style="padding:var(--s8)">'
        '<div class="agent__team">{c} &middot; {v}</div>'
        '<h3 class="t-h3" style="margin-top:12px">{t}</h3>'
        '<p class="t-body">{d}</p>'
        '<div class="metrics metrics--light" style="margin-top:28px;gap:var(--s4)">{m}</div>'
        '<div class="chips" style="margin-top:28px">{ch}</div>'
        '</article>'.format(
            c=c, v=v, t=t, d=d,
            m="".join('<div class="metric"><b style="font-size:1.5rem">%s</b><span>%s</span></div>' % (a, b) for a, b in mets),
            ch="".join('<span class="chip chip--cyan">%s</span>' % x for x in chips))
        for c, v, t, d, mets, chips in CASES)

    return """
<section class="hero">
  <div class="wrap">
    <div class="hero__grid">
      <div class="hero__copy">
        <div class="t-eyebrow">Agentic GTM</div>
        <h1 class="t-display hero__display">Build your revenue<br class="brk">team&rsquo;s <span class="accent">AI workforce</span></h1>
        <p class="t-lead hero__sub" style="color:var(--on-dark-soft)">
          We engineer the GTM systems underneath modern revenue teams &mdash; then deploy the
          agents that run on top. In that order, because the order is the whole point.</p>
        <div class="btn-row">
          <a class="btn btn--cyan" href="contact.html">Scope your project</a>
          <a class="btn btn--ghost-dark" href="agents.html">Explore 33 agents</a>
        </div>
        <div class="hero__meta">
          <div><b>750+</b><span class="t-sys">clients</span></div>
          <div><b>2,000+</b><span class="t-sys">projects</span></div>
          <div><b>10+</b><span class="t-sys">countries</span></div>
          <div><b>30&ndash;75%</b><span class="t-sys">below a traditional SI</span></div>
        </div>
      </div>
      <div>{stack}</div>
    </div>
  </div>
</section>

<section class="strata strata--dark strata--tight" id="partners">
  <div class="wrap on-dark">
    <div class="t-sys">Platform partners</div>
    <div class="grid grid-4 mt-10">{partners}</div>
  </div>
</section>

<section class="strata strata--light">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">The real cost</div>
      <h2 class="t-h1">AI amplifies broken systems. It doesn&rsquo;t fix them.</h2>
      <p class="t-lead">Most AI initiatives fail because the systems underneath them were never
        ready. Dirty data, disconnected platforms, manual process, and four versions of the
        truth &mdash; then an agent on top of all of it, making the same bad calls faster.</p>
    </div>
    <div class="grid grid-4 mt-16">{failures}</div>
  </div>
</section>

<section class="strata strata--ice" id="what-we-do">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">What we do</div>
      <h2 class="t-h1">Build. Manage. Transform.</h2>
      <p class="t-lead">Three stages, one operating model. We meet your stack where it is today
        and take it to an AI operating layer &mdash; without automating a mess along the way.</p>
    </div>
    <div class="mt-12">{pillars}</div>
  </div>
</section>

<section class="strata strata--light" id="agents">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">The agent marketplace</div>
      <h2 class="t-h1">Deployable agents for every GTM role</h2>
      <p class="t-lead">Production-ready agents that plug into the systems you already run.
        Deploy one, or build toward a full AI workforce.</p>
      <div class="chips" style="margin-top:20px">
        <span class="chip chip--cyan">33 agents live</span>
        <span class="chip">4 GTM teams</span>
        <span class="chip">New agents monthly</span>
      </div>
    </div>
    <div class="agents mt-12">{featured}</div>
    <div class="mt-10"><a class="tlink" href="agents.html">Browse all 33 agents <span class="arw">&rarr;</span></a></div>
  </div>
</section>

<section class="strata strata--abyss" id="orchestration">
  <div class="wrap on-dark">
    <div class="head rv">
      <div class="t-eyebrow">Why agentic delivery</div>
      <h2 class="t-h1">The same outcome, at a fraction of the cost and time</h2>
      <p class="t-lead">Traditional systems integrators bill large teams by the hour. Our delivery
        model compresses the mechanical work under senior direction &mdash; and passes the saving
        through as fixed-bid pricing.</p>
    </div>
    <div class="versus mt-16 rv">
      <div class="vcol">
        <div class="vcol__hd"><div class="t-sys" style="color:var(--on-dark-faint)">The old way</div>
          <div class="t-h3" style="color:var(--on-dark);margin-top:6px">Traditional systems integrator</div></div>
        <ul>
          <li>Headcount-driven, open-ended scope</li>
          <li>Large consulting teams</li>
          <li>Time &amp; materials billing</li>
          <li>Timelines measured in months</li>
          <li>High, unpredictable cost</li>
        </ul>
      </div>
      <div class="vcol vcol--ours">
        <div class="vcol__hd"><div class="t-sys">The SaaScend way</div>
          <div class="t-h3" style="color:var(--white);margin-top:6px">Agentic delivery</div></div>
        <ul>
          <li>Expert-directed, AI-accelerated</li>
          <li>Senior architects directing an agent pipeline</li>
          <li>Fixed-bid and outcome-based pricing</li>
          <li>Faster implementation, instrumented from day one</li>
          <li class="vcol__win">30&ndash;75% lower cost</li>
        </ul>
      </div>
    </div>
    <div class="card card--dark rv" style="margin-top:var(--s10);padding:clamp(28px,3.4vw,48px)">
      <div class="sow">
        <div>
          <div class="t-sys">Agentic quoting &middot; Scope-to-Quote</div>
          <h3 class="t-h2" style="color:var(--on-dark);margin-top:12px">Already have an SOW? Compare it in minutes.</h3>
          <p class="t-body" style="max-width:52ch;margin-top:16px">Scope-to-Quote rebuilds any statement
            of work against our agentic delivery model &mdash; fixed-bid, and far cheaper than a
            traditional SI. Upload it and see cost and timeline side by side.</p>
          <div class="btn-row" style="margin-top:28px">
            <a class="btn btn--cyan" href="contact.html">Compare my SOW</a>
            <a class="btn btn--ghost-dark" href="how-we-work.html#pricing">How pricing works</a>
          </div>
        </div>
        <div class="sow__fig">
          <div class="sow__hd"><span>Side by side</span><span>Illustrative</span></div>
          <div class="sow__row"><span class="sow__k">Your current SOW</span><span class="sow__v">$180k</span></div>
          <div class="sow__row"><span class="sow__k">Traditional SI</span><span class="sow__v">$180k</span></div>
          <div class="sow__row"><span class="sow__k">SaaScend fixed bid</span><span class="sow__v">$45k&ndash;$126k</span></div>
          <div class="sow__row sow__row--win"><span class="sow__k">Typical saving</span><span class="sow__v">30&ndash;75%</span></div>
          <div class="sow__note">Your exact fixed bid comes from the SOW itself</div>
        </div>
      </div>
  </div>
</section>

<section class="strata strata--light" id="outcomes">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Customer outcomes</div>
      <h2 class="t-h1">Measurable results across the GTM stack</h2>
      <p class="t-lead">Implementation, managed services and AI &mdash; the work, and the numbers behind it.</p>
    </div>
    <div class="grid grid-2 mt-12">{cases}</div>
  </div>
</section>

<section class="strata strata--abyss strata--tight">
  <div class="wrap on-dark">
    <div class="quote rv">
      <p class="quote__t">&ldquo;They fixed the foundation first, then put agents on top. That order
        is why we actually trust the output &mdash; the number in the CRM is finally the number we
        run on.&rdquo;</p>
      <div class="quote__who"><b>VP Revenue Operations</b>Global SaaS scale-up</div>
    </div>
  </div>
</section>
""".format(stack=stackfig(), partners=partners, failures=failures,
           pillars=pillars, featured=featured, cases=cases)
