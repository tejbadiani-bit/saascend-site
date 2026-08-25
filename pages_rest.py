# -*- coding: utf-8 -*-
"""Interior page bodies."""

def cards(items, dark=False, num=True):
    cls = "card card--dark rv" if dark else "card card--lift rv"
    out = []
    for i, (t, d) in enumerate(items):
        n = '<div class="card__num">%02d</div>' % (i + 1) if num else ""
        out.append('<article class="{c}">{n}<h3 class="t-h3">{t}</h3>'
                   '<p class="t-body">{d}</p></article>'.format(c=cls, n=n, t=t, d=d))
    return "".join(out)


def people(items):
    return "".join(
        '<article class="card card--lift rv person">'
        '<h3 class="t-h3">{n}</h3>'
        '<div class="person__role">{r}</div>'
        '<p class="t-body">{d}</p>'
        '</article>'.format(n=n, r=r, d=d)
        for n, r, d in items)


def split(p_title, p_items, o_title, o_items):
    def li(items, mark):
        return "".join('<li><span class="mk">%s</span><span>%s</span></li>' % (mark, x) for x in items)
    return """
<div class="split rv">
  <div class="panel panel--problem">
    <div class="t-sys" style="color:var(--ink-500)">The problem</div>
    <h3 class="t-h3" style="margin-top:10px">{pt}</h3>
    <ul class="panel__list">{pi}</ul>
  </div>
  <div class="panel panel--ours">
    <div class="t-sys">Our approach</div>
    <h3 class="t-h3" style="margin-top:10px">{ot}</h3>
    <ul class="panel__list">{oi}</ul>
  </div>
</div>""".format(pt=p_title, pi=li(p_items, "&times;"), ot=o_title, oi=li(o_items, "&check;"))


# ============================ SOLUTIONS ============================
BUILD_CAPS = [
    ("Salesforce implementation", "Multi-cloud builds &mdash; Sales, Service, Revenue &mdash; configured to your revenue process, not a template."),
    ("HubSpot implementation", "Connected marketing, sales and service, wired to a clean, shared data model."),
    ("CRM migration", "Move off legacy systems without losing history, ownership or reporting continuity."),
    ("Revenue Cloud", "Quote-to-cash on Salesforce &mdash; catalog, pricing and configuration built to scale."),
    ("Sales automation", "Automate the mechanical work &mdash; routing, follow-up, stage hygiene &mdash; so reps sell."),
    ("Marketing automation", "Lead capture, scoring and nurture flows that hand off cleanly to sales."),
    ("Integrations", "Connect the systems around your CRM into one coherent, observable data flow."),
    ("GTM architecture", "A deliberate data model that supports the next five years, not the next quarter."),
]
MANAGE_CAPS = [
    ("Salesforce administration", "Day-to-day ownership of the org &mdash; requests, releases, and the backlog that never gets to."),
    ("HubSpot administration", "Campaign, lifecycle and data operations run by people who know the platform."),
    ("RevOps support", "Forecast cadence, territory changes, comp questions &mdash; operational cover for the revenue team."),
    ("Continuous optimisation", "Quarterly improvement against real usage data, not a fixed statement of work."),
    ("Data management", "Deduplication, enrichment and hygiene as a standing service, so the model stays trustworthy."),
    ("Documentation &amp; ownership", "Every change documented as it ships, so you always own an operable system."),
]
TRANSFORM_CAPS = [
    ("Agent orchestration", "A master orchestration agent that holds context and routes work across the stack."),
    ("Sales agents", "Forecasting, scoring, research, multi-threading, quoting &mdash; deployed against your process."),
    ("RevOps agents", "Analysis, ops answers and reporting agents that remove the internal bottleneck."),
    ("Customer Success agents", "Health scoring, churn risk, case coaching and ticket deflection on live data."),
    ("Governance", "Human approval on consequential actions, defined guardrails, and an auditable trail."),
    ("Custom agent development", "A single agent built for one specific outcome when the marketplace doesn&rsquo;t cover it."),
]

def solutions_body():
    return """
<section class="strata strata--light">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Build &middot; 01</div>
      <h2 class="t-h1" style="color:var(--navy)">Build a GTM foundation designed for the agents that come next</h2>
      <p class="t-lead">Most teams build for today and rebuild in a year. We implement Salesforce,
        HubSpot and the systems around them with a data model and architecture ready for AI from
        day one.</p>
    </div>
    <div class="grid grid-4 mt-16">{build}</div>
    <div class="mt-16">{bsplit}</div>
  </div>
</section>

<section class="strata strata--ice" id="manage">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Manage &middot; 02</div>
      <h2 class="t-h1" style="color:var(--navy)">Operate the foundation, and keep improving it</h2>
      <p class="t-lead">A GTM system decays without an owner. Managed services give you senior
        operators on the stack every week &mdash; and a documented system you always own outright.</p>
    </div>
    <div class="grid grid-3 mt-16">{manage}</div>
  </div>
</section>

<section class="strata strata--abyss" id="transform">
  <div class="wrap on-dark">
    <div class="head rv">
      <div class="t-eyebrow">Transform &middot; 03</div>
      <h2 class="t-h1">Deploy the agents &mdash; on something worth trusting</h2>
      <p class="t-lead">Agents do real GTM work when the data model, the automation and the
        ownership underneath them are sound. That is the only condition we deploy under.</p>
    </div>
    <div class="grid grid-3 mt-16">{transform}</div>
    <div class="mt-16 rv">
      <a class="btn btn--cyan" href="agents.html">Browse the 33 agents</a>
    </div>
  </div>
</section>
""".format(build=cards(BUILD_CAPS, num=False),
           manage=cards(MANAGE_CAPS, num=False),
           transform=cards(TRANSFORM_CAPS, dark=True, num=False),
           bsplit=split(
               "Teams build for today and rebuild in a year.",
               ["Systems configured to a point-in-time process, not the revenue model.",
                "A data model that fractures the moment the org grows or reorganises.",
                "Automation bolted on after the fact, so the CRM number is never trusted.",
                "No path to AI &mdash; agents cannot operate on an inconsistent foundation."],
               "Build once, for where you&rsquo;re going.",
               ["A deliberate data model that stays coherent as the business scales.",
                "Clean, observable integrations &mdash; one source of truth across the stack.",
                "Automation designed in, so the number in the CRM is the number you run on.",
                "A foundation agents can trust, ready for the operating layer on top."]))


# ============================ AGENTS ============================
def agents_body():
    return """
<section class="strata strata--light">
  <div class="wrap">
    <div style="display:flex;flex-wrap:wrap;gap:var(--s6);align-items:end;justify-content:space-between">
      <div class="filters" data-agent-filters></div>
      <div class="t-sys" data-agent-count style="color:var(--ink-500)"></div>
    </div>
    <hr class="rule" style="margin:var(--s6) 0 var(--s10)">
    <div class="agents" data-agents></div>
    <noscript><p class="t-body mt-10">Enable JavaScript to filter the marketplace, or
      <a class="tlink" href="contact.html">ask us for the full catalogue</a>.</p></noscript>
  </div>
</section>

<section class="strata strata--ice strata--tight">
  <div class="wrap">
    <div class="head head--center rv">
      <div class="t-eyebrow">How deployment works</div>
      <h2 class="t-h2" style="color:var(--navy)">An agent is a deployment, not a download</h2>
    </div>
    <div class="grid grid-4 mt-12">{steps}</div>
  </div>
</section>
""".format(steps=cards([
        ("Fit check", "We confirm the systems and data the agent depends on actually exist, and are clean enough to reason against."),
        ("Foundation work", "Anything missing gets built first &mdash; fields, automation, ownership. No agent lands on a gap."),
        ("Deploy with guardrails", "Scoped permissions, human approval on consequential actions, and a logged trail of every decision."),
        ("Measure", "The agent&rsquo;s stated gain becomes a tracked number, reviewed against baseline."),
    ]))


# ============================ HOW WE WORK ============================
RUNGS = [
    ("S1", "Implement", "Build the GTM systems and data model correctly the first time."),
    ("S2", "Manage", "Operate the foundation with clear ownership and support."),
    ("S3", "Optimise", "Continuously improve the stack against real usage."),
    ("S4", "Automate", "Remove manual work with reliable, owned automation."),
    ("S5", "Agentify", "Deploy specialised agents on the managed foundation."),
    ("S6", "AI Workforce", "Orchestrated agents working across every revenue role."),
]
PRICING = [
    ("Fixed bid", "A defined scope for a defined price. You know the number before we start &mdash; no open meter."),
    ("Outcome-based", "Pricing tied to the result we deliver, not the hours we spend getting there."),
    ("Managed services", "A predictable monthly engagement that operates and optimises your stack over time."),
    ("Enterprise", "Multi-workstream transformation with governance, orchestration and executive alignment."),
]
FAQ = [
    ("Do we have to start at Implement?",
     "No. We meet you at your actual stage. If your foundation is solid we start at Optimise or "
     "Agentify. Most teams are a stage earlier than they think &mdash; we tell you the truth about "
     "that up front."),
    ("How is this cheaper than a traditional SI?",
     "We use AI agents throughout delivery &mdash; discovery, configuration, testing, documentation "
     "&mdash; with senior architects directing and reviewing. Fewer hours to the same outcome, "
     "passed through as fixed-bid pricing. Typically 30&ndash;75% lower cost."),
    ("Where does the AI layer fit?",
     "Agentify and AI Workforce are the last two stages, and only durable on a managed foundation. "
     "We will not deploy agents onto a broken data model &mdash; that just automates the mess."),
    ("Who owns the systems when you are done?",
     "You do. Everything is documented and owned as it ships. Managed services are a choice, "
     "not a lock-in."),
]

def how_body():
    rungs = "".join(
        '<div class="rung{c}"><div class="rung__k">{k}</div>'
        '<div><div class="rung__t">{t}</div><div class="rung__d">{d}</div></div></div>'.format(
            c=" rung--peak" if k == "S6" else "", k=k, t=t, d=d)
        for k, t, d in RUNGS)

    faq = "".join(
        '<details><summary>{q}<span class="pm">+</span></summary>'
        '<div class="faq__a">{a}</div></details>'.format(q=q, a=a) for q, a in FAQ)

    return """
<section class="strata strata--light">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">The maturity model</div>
      <h2 class="t-h1" style="color:var(--navy)">Six stages, one direction</h2>
      <p class="t-lead">You don&rsquo;t jump to an AI workforce. You build to it. Each stage is what
        makes the next one safe &mdash; so the model reads bottom-up, like the stack it describes.</p>
    </div>
    <div class="ladder mt-12 rv">{rungs}</div>
  </div>
</section>

<section class="strata strata--abyss" id="check">
  <div class="wrap on-dark">
    <div class="head rv">
      <div class="t-eyebrow">Where are you today?</div>
      <h2 class="t-h1">Find your stage in two minutes</h2>
      <p class="t-lead">Six questions. We&rsquo;ll place you on the model, name the one move that
        matters next, and point you at the agents to start with.</p>
    </div>
    <div class="quiz mt-12 rv" data-quiz>
      <div class="quiz__bar">
        <span class="t-sys">GTM maturity check</span>
        <div class="quiz__track"><div class="quiz__fill" data-quiz-fill></div></div>
        <span class="t-sys" data-quiz-n style="color:var(--on-dark-faint)">0/6</span>
      </div>
      <div data-quiz-body>
        <div class="quiz__q" data-quiz-q></div>
        <div class="quiz__opts" data-quiz-opts></div>
      </div>
      <div class="quiz__res" data-quiz-res></div>
      <noscript><p class="t-body">The maturity check needs JavaScript.
        <a class="tlink" href="contact.html">Ask an architect instead &rarr;</a></p></noscript>
    </div>
  </div>
</section>

<section class="strata strata--light" id="delivery">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Agentic delivery</div>
      <h2 class="t-h1" style="color:var(--navy)">The same outcome, fewer hours</h2>
      <p class="t-lead">We compress the mechanical work of delivery with our own agent pipeline
        &mdash; discovery, configuration, testing, documentation &mdash; under senior direction,
        and price the result rather than the effort.</p>
    </div>
    <div class="mt-16">{dsplit}</div>
  </div>
</section>

<section class="strata strata--ice" id="pricing">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Commercial models</div>
      <h2 class="t-h1" style="color:var(--navy)">Pricing that matches the work</h2>
      <p class="t-lead">No open meter. Choose the model that fits the engagement &mdash; or combine
        them across a transformation.</p>
    </div>
    <div class="grid grid-4 mt-12">{pricing}</div>
  </div>
</section>

<section class="strata strata--light">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Questions</div>
      <h2 class="t-h1" style="color:var(--navy)">How the engagement actually runs</h2>
    </div>
    <div class="faq mt-12" style="max-width:840px">{faq}</div>
  </div>
</section>
""".format(rungs=rungs, pricing=cards(PRICING, num=False), faq=faq,
           dsplit=split(
               "Traditional systems integrator",
               ["Headcount-driven scope, billed by the hour",
                "Large consulting teams on a long clock",
                "Time &amp; materials, unpredictable totals",
                "Timelines measured in months",
                "Documentation written at the end, if at all"],
               "SaaScend agentic delivery",
               ["Expert-directed, AI-accelerated execution",
                "Senior architects directing an agent pipeline",
                "Fixed-bid and outcome-based pricing",
                "Faster implementation, instrumented from day one",
                "Documentation produced as the work ships"]))


# ============================ ABOUT ============================
PRINCIPLES = [
    ("Better practices, not best practices", "There is no universal &ldquo;best.&rdquo; We fit the pattern to your business, your data and how your team actually works &mdash; and we can defend every decision."),
    ("Foundation before automation", "We never automate a mess. Clean the data model and the process first, then put agents on top of something worth trusting."),
    ("Experts direct the work", "Senior architects own every consequential decision. AI compresses the mechanical work; it does not replace the judgement that makes the work correct."),
    ("Outcomes, not hours", "Fixed-bid and outcome-based pricing. We are accountable for the result, not for keeping a meter running."),
    ("Systems that document themselves", "Discovery, configuration and documentation happen as we build &mdash; so you inherit a system you can operate, not a black box."),
    ("One number everyone trusts", "The measure of a GTM system is whether leadership runs on the number in the CRM. That is the bar we build to."),
]
LEADERSHIP = [
    ("Craig Jordan", "Founder &amp; CEO",
     "Sets the direction for agentic GTM delivery and owns the platform partnerships the practice is built on."),
    ("Tej Badiani", "VP Consulting &amp; Operations",
     "Owns the agentic delivery model end to end &mdash; the architects, the agent pipeline, and the quality bar on every engagement."),
    ("Dev Purdon", "Senior Director of Consulting",
     "Leads consulting delivery on client engagements, from discovery through UAT sign-off."),
    ("Allie Adams", "Director of Sales",
     "Owns scoping and commercials &mdash; the fixed-bid number you see before anything starts."),
]

EXPERTISE = [
    ("The stack is the strategy", "How you model accounts, stages and territories decides what you can measure and what you can automate. We treat the data model as a first-class deliverable."),
    ("Depth across the ecosystem", "Salesforce, HubSpot, RevOps and the surrounding tools &mdash; we know how they connect, where they conflict, and how to make them one system."),
    ("We have seen it break", "Thousands of projects means we recognise the failure modes early &mdash; duplicate fields, conflicting automation, forecasts nobody trusts &mdash; and design around them."),
]

def about_body():
    return """
<section class="strata strata--light">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Our mission</div>
      <h2 class="t-h1" style="color:var(--navy)">Give every revenue team a foundation strong enough to run AI on</h2>
      <p class="t-lead">Most GTM stacks were never designed for automation. We fix that &mdash;
        building and operating the systems of record so specialised agents can act on data the
        whole business trusts.</p>
    </div>
    <div class="metrics metrics--light mt-16 rv">
      <div class="metric"><b>750+</b><span>clients served</span></div>
      <div class="metric"><b>2,000+</b><span>projects delivered</span></div>
      <div class="metric"><b>10+</b><span>countries &middot; AMER + EMEA</span></div>
    </div>
  </div>
</section>

<section class="strata strata--ice">
  <div class="wrap">
    <div class="grid grid-2" style="gap:clamp(40px,6vw,80px);align-items:start">
      <div class="rv">
        <div class="t-eyebrow">Our story</div>
        <h2 class="t-h2" style="color:var(--navy);margin-top:16px">Built by operators, for operators</h2>
      </div>
      <div class="rv stack-4">
        <p class="t-body">SaaScend started inside revenue operations, not on a sales floor. We spent
          years untangling Salesforce orgs that had drifted, reconciling forecasts nobody believed,
          and rebuilding the plumbing revenue teams depend on every day.</p>
        <p class="t-body">One pattern held: the teams that scaled cleanly were the ones whose
          systems were designed with intent. So we built a consultancy around that discipline
          &mdash; strategic and tactical, weighted toward the systems themselves.</p>
        <p class="t-body">Then AI changed the ceiling. Agents can now do real GTM work &mdash; but
          only against data and process they can trust. That is why we became the Agentic GTM
          Company: build the foundation, manage it intelligently, and transform how the team works
          with an AI workforce on top.</p>
        <div class="chips" style="margin-top:8px">
          <span class="chip chip--cyan">Salesforce Global Strategic Agreement</span>
          <span class="chip">HubSpot solutions partner</span>
          <span class="chip">Anthropic partner</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="strata strata--light">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">What we believe</div>
      <h2 class="t-h1" style="color:var(--navy)">The principles behind every engagement</h2>
      <p class="t-lead">These are not slogans. They are the rules we design and deliver by.</p>
    </div>
    <div class="grid grid-3 mt-16">{principles}</div>
  </div>
</section>

<section class="strata strata--abyss">
  <div class="wrap on-dark">
    <div class="head rv">
      <div class="t-eyebrow">Why GTM expertise matters</div>
      <h2 class="t-h1">Generic consultants configure.<br>Systems experts architect.</h2>
      <p class="t-lead">GTM systems are where strategy meets the database. Getting them right takes
        people who have lived in the details &mdash; not a template applied from the outside.</p>
    </div>
    <div class="grid grid-3 mt-16">{expertise}</div>
  </div>
</section>

<section class="strata strata--light">
  <div class="wrap">
    <div class="head rv">
      <div class="t-eyebrow">Leadership</div>
      <h2 class="t-h1" style="color:var(--navy)">Who owns the outcome</h2>
      <p class="t-lead">Four people sign off on every engagement. You deal with them directly
        &mdash; not an account manager relaying decisions from someone you never meet.</p>
    </div>
    <div class="grid grid-4 mt-16">{leadership}</div>
  </div>
</section>
""".format(principles=cards(PRINCIPLES),
           expertise=cards(EXPERTISE, dark=True, num=True),
           leadership=people(LEADERSHIP))


# ============================ CONTACT ============================
def contact_body():
    return """
<section class="strata strata--light">
  <div class="wrap">
    <div class="grid grid-2" style="gap:clamp(40px,6vw,80px);align-items:start">
      <form class="form rv" data-scope-form>
        <div class="field">
          <label for="f-name">Your name</label>
          <input id="f-name" name="name" required autocomplete="name">
        </div>
        <div class="field">
          <label for="f-company">Company</label>
          <input id="f-company" name="company" required autocomplete="organization">
        </div>
        <div class="field">
          <label for="f-email">Work email</label>
          <input id="f-email" name="email" type="email" required autocomplete="email">
        </div>
        <div class="field">
          <label for="f-stack">Current stack</label>
          <input id="f-stack" name="stack" placeholder="Salesforce, HubSpot, Gong&hellip;">
        </div>
        <div class="field">
          <label for="f-stage">Where you are today</label>
          <select id="f-stage" name="stage">
            <option>Implement &mdash; building or rebuilding the systems</option>
            <option>Manage &mdash; running it, need an owner</option>
            <option>Optimise &mdash; it works, it could work better</option>
            <option>Automate &mdash; removing the manual work</option>
            <option>Agentify &mdash; ready to deploy agents</option>
            <option>Comparing an existing SOW</option>
          </select>
        </div>
        <div class="field">
          <label for="f-detail">What are you trying to fix?</label>
          <textarea id="f-detail" name="detail" placeholder="The forecast nobody trusts, the migration you keep deferring, the quoting process&hellip;"></textarea>
        </div>
        <div class="btn-row" style="margin-top:var(--s4)">
          <button class="btn btn--primary" type="submit">Send to an architect</button>
          <a class="btn btn--ghost" href="mailto:hello@saascend.com">hello@saascend.com</a>
        </div>
        <p class="t-small">Opens in your mail client with the details filled in &mdash; nothing is
          submitted to a third party.</p>
      </form>

      <aside class="rv stack-8">
        <div>
          <div class="t-sys">What happens next</div>
          <div class="ladder" style="margin-top:16px;flex-direction:column">
            <div class="rung"><div class="rung__k">01</div><div>
              <div class="rung__t">A real architect reads it</div>
              <div class="rung__d">Not a qualification form. The person who would run the work.</div></div></div>
            <div class="rung"><div class="rung__k">02</div><div>
              <div class="rung__t">45 minutes on your stack</div>
              <div class="rung__d">We name the stage you&rsquo;re actually at, and the one move that matters next.</div></div></div>
            <div class="rung"><div class="rung__k">03</div><div>
              <div class="rung__t">A fixed-bid scope</div>
              <div class="rung__d">A defined number before anything starts &mdash; or an honest no.</div></div></div>
          </div>
        </div>
        <div class="panel panel--ours">
          <div class="t-sys">Already have an SOW?</div>
          <h3 class="t-h3" style="margin-top:10px">Send it over instead</h3>
          <p class="t-body" style="margin-top:12px">We&rsquo;ll rebuild it against our agentic
            delivery model and show you cost and timeline side by side. Typically 30&ndash;75%
            lower than a traditional SI.</p>
        </div>
        <div>
          <div class="t-sys">Coverage</div>
          <p class="t-body" style="margin-top:12px">AMER and EMEA &middot; 750+ clients &middot;
            10+ countries. Salesforce Global Strategic Agreement partner.</p>
        </div>
      </aside>
    </div>
  </div>
</section>
"""
