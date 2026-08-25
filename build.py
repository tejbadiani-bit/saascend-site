#!/usr/bin/env python3
"""Assembles the SaaScend static site from one shell + per-page bodies."""
import pathlib, re

OUT = pathlib.Path(__file__).parent

NAV = [("index.html", "Home"), ("solutions.html", "Solutions"),
       ("agents.html", "Agents"), ("how-we-work.html", "How we work"),
       ("about.html", "About")]

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#01142F">
<link rel="icon" href="assets/saascend-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Open+Sans:wght@400;600&family=JetBrains+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/site.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body>
<a class="btn" href="#main" style="position:absolute;left:-9999px">Skip to content</a>

<header class="nav">
  <div class="wrap nav__in">
    <a class="nav__logo" href="index.html" aria-label="SaaScend — home">
      <img src="assets/saascend-logo-white.png" alt="SaaScend">
    </a>
    <nav class="nav__links">
      {navlinks}
      <a class="btn btn--cyan nav__cta" href="contact.html">Scope your project</a>
    </nav>
    <button class="nav__burger" aria-label="Menu" aria-expanded="false">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
        <path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>
<div class="nav__panel">
  <div class="wrap">
    {navpanel}
    <a href="contact.html" style="color:var(--cyan)">Scope your project &rarr;</a>
  </div>
</div>

<main id="main" class="page">
{body}
</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <div>
        <div class="foot__logo"><img src="assets/saascend-logo-white.png" alt="SaaScend"></div>
        <p class="t-body" style="margin-top:20px;max-width:34ch;color:var(--on-dark-soft)">
          SaaScend is the Agentic GTM Company. We engineer the GTM systems underneath modern
          revenue teams &mdash; then deploy the agents that run on top.</p>
      </div>
      <div class="foot__col">
        <h4>Solutions</h4>
        <a href="solutions.html">GTM systems implementation</a>
        <a href="solutions.html#manage">Managed services</a>
        <a href="solutions.html#transform">Agentic transformation</a>
        <a href="how-we-work.html">How we work</a>
      </div>
      <div class="foot__col">
        <h4>Agents</h4>
        <a href="agents.html">Agent marketplace</a>
        <a href="index.html#orchestration">The agentic layer</a>
        <a href="how-we-work.html#delivery">Agentic delivery</a>
        <a href="how-we-work.html#pricing">Commercial models</a>
      </div>
      <div class="foot__col">
        <h4>Company</h4>
        <a href="about.html">About</a>
        <a href="index.html#outcomes">Customer outcomes</a>
        <a href="contact.html">Scope your project</a>
        <a href="mailto:hello@saascend.com">hello@saascend.com</a>
      </div>
    </div>
    <div class="foot__base">
      <span>&copy; 2026 SaaScend &middot; The Agentic GTM Company</span>
      <span>AMER &middot; EMEA</span>
    </div>
  </div>
</footer>

<script src="assets/agents-data.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
"""

CLOSER = """
<section class="strata strata--dark">
  <div class="wrap on-dark">
    <div class="head head--center rv">
      <div class="t-sys">Get started</div>
      <h2 class="t-h1">Ready to build your AI workforce?</h2>
      <p class="t-lead">We start with the systems underneath &mdash; then layer the agents that
        transform how your revenue team works. Tell us where you are.</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn btn--cyan" href="contact.html">Scope your project</a>
        <a class="btn btn--ghost-dark" href="agents.html">Explore agents</a>
      </div>
    </div>
  </div>
</section>
"""

def page(slug, title, desc, body):
    navlinks = "".join(
        '<a class="nav__link{}" href="{}">{}</a>'.format(
            " is-active" if h == slug else "", h, t) for h, t in NAV)
    navpanel = "".join('<a href="{}">{}</a>'.format(h, t) for h, t in NAV)
    (OUT / slug).write_text(SHELL.format(
        title=title, desc=desc, navlinks=navlinks, navpanel=navpanel, body=body))
    print("wrote", slug, len(body), "bytes of body")

def masthead(sys, h1, lead, accent=""):
    """Short navy masthead for interior pages."""
    return f"""
<section class="strata strata--tight" style="background:
    radial-gradient(900px 500px at 92% -20%, rgba(0,172,212,0.18), transparent 62%),
    var(--abyss); padding-top:clamp(56px,7vw,88px); padding-bottom:clamp(48px,6vw,72px)">
  <div class="wrap on-dark">
    <div class="head stack-4">
      <div class="t-sys">{sys}</div>
      <h1 class="t-h1">{h1}{accent}</h1>
      <p class="t-lead" style="max-width:52ch">{lead}</p>
    </div>
  </div>
</section>
"""

# ============================ ASSEMBLE ============================
if __name__ == "__main__":
    import pages_home, pages_rest as R

    page("index.html",
         "SaaScend — Build the revenue team of the future",
         "SaaScend is the Agentic GTM Company. We engineer the GTM systems underneath modern "
         "revenue teams — Salesforce, HubSpot, RevOps — then deploy the AI agents that run on top.",
         pages_home.body() + CLOSER)

    page("solutions.html",
         "Solutions — Build, Manage, Transform | SaaScend",
         "Implement and migrate modern GTM systems, operate them with managed services, and "
         "deploy specialised AI agents on top. Three stages, one operating model.",
         masthead("Solutions",
                  "Three stages, one ",
                  "We meet your stack where it is today and take it to an AI operating layer — "
                  "without automating a mess along the way.",
                  '<span style="color:var(--cyan)">operating model</span>')
         + R.solutions_body() + CLOSER)

    page("agents.html",
         "Agent marketplace — 33 GTM agents | SaaScend",
         "33 production-ready AI agents for sales, marketing, customer success and revenue "
         "operations — deployed onto a foundation they can trust.",
         masthead("Agent marketplace",
                  "Deployable agents for every ",
                  "Production-ready agents that plug into the systems you already run. Deploy one, "
                  "or build toward a full AI workforce.",
                  '<span style="color:var(--cyan)">GTM role</span>')
         + R.agents_body() + CLOSER)

    page("how-we-work.html",
         "How we work — the maturity model | SaaScend",
         "Six stages from first build to a full AI workforce, agentic delivery at 30–75% below a "
         "traditional SI, and fixed-bid pricing. Take the two-minute maturity check.",
         masthead("How we work",
                  "One model from first build to a full ",
                  "Every engagement runs on the same maturity model. We meet you at your stage and "
                  "move you up it — deliberately, with a foundation that holds at every step.",
                  '<span style="color:var(--cyan)">AI workforce</span>')
         + R.how_body() + CLOSER)

    page("about.html",
         "About SaaScend — the Agentic GTM Company",
         "Built by operators, for operators. We modernise the GTM systems underneath revenue "
         "teams, then deploy the AI agents that run on top.",
         masthead("About SaaScend",
                  "We build the systems that make AI ",
                  "SaaScend is the Agentic GTM Company. We modernise the GTM systems underneath "
                  "revenue teams — then deploy specialised agents on top that automate work and "
                  "accelerate growth.",
                  '<span style="color:var(--cyan)">trustworthy</span>')
         + R.about_body() + CLOSER)

    page("contact.html",
         "Scope your project | SaaScend",
         "Tell us what you're building. A senior architect reads every enquiry and comes back "
         "with a fixed-bid scope — or an honest no.",
         masthead("Scope your project",
                  "Tell us what you&rsquo;re ",
                  "A senior architect reads every enquiry. You get 45 minutes on your actual stack, "
                  "then a fixed-bid scope — or an honest no.",
                  '<span style="color:var(--cyan)">building</span>')
         + R.contact_body())
