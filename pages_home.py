# -*- coding: utf-8 -*-
"""Home page — a run of edge-to-edge tiles, one idea each.

Rewritten from the first build, which repeated a single section shell
(eyebrow / headline / lead / grid of bordered cards) six times. Structure
follows Apple's tile discipline; the sharp geometry, the solid accent field
and the boxed keyword come from Boldare. The artifact in every tile is the
GTM stack, which is neither of theirs.
"""

import pathlib
import re

LAYERS = [
    ("L1", "Systems &amp; data",  "One data model the whole business trusts &mdash; Salesforce, HubSpot, the warehouse.",
     "Data model · Field governance · Migrations · Dedupe"),
    ("L2", "Integrations",        "Observable flow between systems, not point-to-point guesswork.",
     "Named credentials · Platform events · Observable sync"),
    ("L3", "Automation",          "Documented, single-owner automation with defined guardrails.",
     "Flows · Apex · Single-writer rules · Guardrails"),
    ("L4", "Orchestration",       "A master agent that holds context and routes work across the stack.",
     "Context store · Routing · Approvals · Audit trail"),
    ("L5", "Agent workforce",     "33 specialised agents doing real GTM work, with human approval on consequential actions.",
     "33 agents · 4 GTM teams · Human in the loop"),
]

WEAK = [
    ("L1", "Systems &amp; data",  "unowned"),
    ("L2", "Integrations",        "partial"),
    ("L3", "Automation",          "undocumented"),
    ("L4", "Orchestration",       "absent"),
    ("L5", "Agent workforce",     "deployed anyway"),
]

def _roster():
    """All 33 agents, read from the same file the marketplace uses.
    A hand-typed subset once said "thirty-three" above a list of 22."""
    src = (pathlib.Path(__file__).parent / 'assets' / 'agents-data.js').read_text()
    items = re.findall(r'team:"(.*?)",\s*name:"(.*?)"', src)
    return [(n.replace(' Agent', ''), t) for t, n in items]


ROSTER = _roster()

def sequence():
    """The argument, pinned. One layer per scroll step, copy swapping beside it."""
    steps = "".join(
        '<div class="seq__step{live}" data-step="{i}">'
        '<div class="seq__id">{k} &middot; Layer {n} of 5</div>'
        '<div class="seq__name">{nm}</div>'
        '<p class="seq__note">{d}</p>'
        '<div class="seq__caps">{c}</div>'
        '</div>'.format(live=" is-live" if i == 0 else "", i=i, k=k, n=i + 1, nm=nm, d=d, c=c)
        for i, (k, nm, d, c) in enumerate(LAYERS))

    plates = "".join(
        '<div class="plate{built}" data-plate="{i}">'
        '<div class="plate__id">{k}</div><div class="plate__name">{nm}</div></div>'.format(
            built=" is-built is-current" if i == 0 else "", i=i, k=k, nm=nm)
        for i, (k, nm, _d, _c) in enumerate(LAYERS))

    return """
<section class="seq" id="stack" data-seq>
  <div class="seq__track">
    <div class="seq__stage">
      <div class="wrap">
        <div class="seq__grid">
          <div class="seq__copy">{steps}</div>
          <div>
            <div class="seq__plates">{plates}</div>
            <div class="seq__foot">
              <span>Built bottom-up</span>
              <span><b>AI sits at the top</b></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>""".format(steps=steps, plates=plates)


def body():
    weak = "".join(
        '<div class="weak__row{ok}"><div class="weak__id">{k}</div>'
        '<div class="weak__t">{t}</div><div class="weak__s">{s}</div></div>'.format(
            ok="", k=k, t=t, s=s) for k, t, s in WEAK)

    order = {"Sales": 0, "Customer Success": 1, "Marketing": 2, "Revenue Operations": 3}
    roster = "".join(
        '<div class="roster__item"><b>{n}</b><span class="roster__team">{t}</span></div>'.format(n=n, t=t)
        for n, t in sorted(ROSTER, key=lambda x: (order.get(x[1], 9), x[0])))

    return """
<section class="open">
  <div class="wrap">
    <h1 class="open__display">Build your revenue team&rsquo;s <span class="accent">AI workforce</span></h1>
    <p class="open__sub">We engineer the GTM systems underneath revenue teams. Then we deploy the
      agents that run on top. In that order, because the order is the whole argument.</p>
    <div class="open__act btn-row">
      <a class="btn btn--cyan" href="contact.html">Scope your project</a>
      <a class="btn btn--ghost-dark" href="agents.html">Explore 33 agents</a>
    </div>
    <div class="open__foot">
      <div><b>750+</b>clients</div>
      <div><b>2,000+</b>projects</div>
      <div><b>10+</b>countries</div>
      <div><b>30&ndash;75%</b>below a traditional SI</div>
    </div>
  </div>
</section>

{sequence}

<section class="tile field--paper">
  <div class="tile__in">
    <h2 class="tile__name">AI amplifies broken systems.<br>It doesn&rsquo;t <span class="mark">fix</span> them.</h2>
    <p class="tile__line">Deploy an agent onto a weak foundation and it makes the same bad calls,
      faster. This is the stack most teams actually have.</p>
    <div class="tile__art">
      <div class="weak">{weak}</div>
    </div>
  </div>
</section>

<section class="tile field--ice">
  <div class="tile__in tile__in--wide">
    <h2 class="tile__name">Build. Manage. Transform.</h2>
    <p class="tile__line">Three stages, one operating model. We meet your stack where it is and take
      it to an AI operating layer &mdash; without automating a mess on the way.</p>
    <div class="tile__art">
      <div class="tlist" style="text-align:left">
        <div class="trow"><div class="trow__k">Build</div>
          <div class="trow__v">Implement and migrate the systems, with a data model designed for the
            agents that come later. Salesforce, HubSpot, Revenue Cloud, CRM migrations, integrations.</div></div>
        <div class="trow"><div class="trow__k">Manage</div>
          <div class="trow__v">Operate and keep improving the foundation. Salesforce and HubSpot
            administration, RevOps support, data management, documentation as it ships.</div></div>
        <div class="trow"><div class="trow__k">Transform</div>
          <div class="trow__v">Deploy specialised agents on the managed foundation. Orchestration,
            sales, RevOps and Customer Success agents, with human approval on consequential actions.</div></div>
      </div>
    </div>
    <div class="tile__act">
      <a class="pill pill--fill" href="solutions.html">See all three</a>
    </div>
  </div>
</section>

<section class="tile field--abyss">
  <div class="tile__in tile__in--wide">
    <h2 class="tile__name">Thirty-three agents, <span class="mark">already built</span></h2>
    <p class="tile__line">Production-ready, plugged into the systems you already run. Deploy one, or
      build toward a full workforce.</p>
    <div class="tile__art">
      <div class="roster">{roster}</div>
    </div>
    <div class="tile__act">
      <a class="pill pill--fill" href="agents.html">Browse the marketplace</a>
      <a class="pill pill--line" href="contact.html">Ask for one we haven&rsquo;t built</a>
    </div>
  </div>
</section>

<section class="tile field--cyan">
  <div class="tile__in">
    <div class="bignum">30&ndash;75%</div>
    <h2 class="tile__name" style="margin-top:clamp(20px,3vw,32px);font-size:clamp(1.5rem,2.8vw,2.25rem)">
      below a traditional systems integrator</h2>
    <p class="tile__line">They bill large teams by the hour. We compress the mechanical work with our
      own agent pipeline under senior direction, and price the result instead of the effort.</p>
    <div class="tile__act">
      <a class="pill pill--fill" href="contact.html">Compare your SOW</a>
      <a class="pill pill--line" href="how-we-work.html#pricing">How pricing works</a>
    </div>
  </div>
</section>

<div class="tiles-2">
  <section class="tile field--paper">
    <div class="tile__in">
      <h2 class="tile__name">A forecast they finally trust</h2>
      <p class="tile__line">A scale-up had outgrown its Salesforce build. We re-architected the data
        model, rebuilt forecasting, then put a Forecast Agent on top.</p>
      <div class="tile__art">
        <div class="runs">
          <div class="run"><b>32%</b><span>faster cycle</span></div>
          <div class="run"><b>1 hr</b><span>was one day</span></div>
          <div class="run"><b>100%</b><span>automation owned</span></div>
        </div>
      </div>
    </div>
  </section>
  <section class="tile field--paper">
    <div class="tile__in">
      <h2 class="tile__name">A migration that lost nothing</h2>
      <p class="tile__line">A fintech outgrew one platform. Salesforce as system of record, HubSpot
        driving marketing, cut over without losing pipeline.</p>
      <div class="tile__art">
        <div class="runs">
          <div class="run"><b>0</b><span>pipeline lost</span></div>
          <div class="run"><b>3 wks</b><span>to production</span></div>
          <div class="run"><b>2&rarr;1</b><span>systems of record</span></div>
        </div>
      </div>
    </div>
  </section>
</div>

<section class="tile field--navy">
  <div class="tile__in">
    <blockquote class="tile__name" style="font-weight:600;font-size:clamp(1.375rem,3vw,2.25rem);letter-spacing:-0.025em;line-height:1.25">
      &ldquo;They fixed the foundation first, then put agents on top. That order is why we actually
      trust the output &mdash; the number in the CRM is finally the number we run on.&rdquo;</blockquote>
    <p class="tile__line" style="font-family:var(--mono);font-size:0.6875rem;letter-spacing:0.12em;text-transform:uppercase">
      VP Revenue Operations &middot; Global SaaS scale-up</p>
  </div>
</section>
""".format(sequence=sequence(), weak=weak, roster=roster)
