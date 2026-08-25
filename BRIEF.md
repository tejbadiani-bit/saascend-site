# SaaScend site — working brief

Live: https://tejbadiani-bit.github.io/saascend-site/
Repo: tejbadiani-bit/saascend-site · source of truth is `build.py` + `pages_*.py`,
never the generated `.html`.

This is a **revision brief**, not a build brief. The site exists and is verified.
Read the baseline before changing anything, and do not rebuild what already works.

---

## Baseline — what exists and is settled

SaaScend is the Agentic GTM Company. We engineer the GTM systems underneath
revenue teams — Salesforce, HubSpot, RevOps — then deploy the AI agents that run
on top. That order is the whole argument, and the site is built around it.

Six pages: home, solutions, agents, how we work, about, contact. Static, no
build step beyond `python3 build.py`, served from GitHub Pages.

**Signature, already built:** the GTM stack as five load-bearing layers
(L1 systems & data → L2 integrations → L3 automation → L4 orchestration →
L5 agent workforce). Source order is L1-first and CSS reverses it, so it reads
bottom-up and assembles bottom-up. Each layer is a spring accordion revealing
the concrete deliverables at that layer. This is the one bold element — keep
everything around it quiet, and do not add a second signature.

**Design system, settled:** navy `#031F49`, deeper ground `#01142F`, cyan
`#00ACD4`, action blue `#1071C3`, ice `#EBF9FF`. Montserrat display with tight
negative tracking at large sizes, Open Sans body, JetBrains Mono for anything
the machine owns — layer ids, system names, metric units, counts. Alternating
light/ice/navy/abyss strata. Hairline rules do the structural work; cards are
mostly borderless. `text-wrap: balance` on all headings.

**Motion policy, settled:** Motion is vendored at `assets/vendor/motion.js` —
no CDN. Springs only where something is grabbable or spammable: the mobile nav
sheet (1:1 drag, pointer capture, ~10px hysteresis, rubber-banded boundary,
momentum projection, release-velocity handoff, exits along its entry path), the
stack layers, the marketplace filter, the quiz steps. Apple's two parameters:
`bounce 0 / duration 0.4` reposition, `bounce 0.2 / duration 0.3` drawer.
Predetermined motion (scroll reveals, the hero assembly) stays in CSS so it
holds frames during load. Reduced motion degrades to a cross-fade and is read
live. Every resting state is correct with JavaScript disabled.

**Content, settled:** real copy from saascend.com, the real 33-agent catalogue
in `assets/agents-data.js`, real numbers (750+ clients, 2,000+ projects, 10+
countries, 30–75% below a traditional SI).

Use the `apple-design`, `emil-design-eng` and `frontend-design` skills. Read
them before writing code. `impeccable` is also installed — use it *or*
`frontend-design`, never both on the same task; they conflict by design.

---

## Audience and register — unchanged

VP RevOps, CROs and RevOps leads at B2B SaaS scale-ups and mid-market
enterprises, AMER + EMEA. Evaluating an implementation partner or an AI agent
programme; many are holding a traditional SI's SOW they think is too expensive.
Technical enough to smell vagueness.

Premium, restrained, engineered. Trustworthy because it is specific, not because
it says "trusted". No hype, no gradient-blob SaaS look. Reference the discipline
of Linear (typographic restraint, dark surfaces that earn their contrast) and
Stripe (diagrams that carry real information) — the discipline, not the layouts.

---

## Closed — 2026-08-25

- **Social card.** `assets/og-card.jpg` (1200×630, 114KB). Higgsfield GPT Image 2
  generated the five-strata background; the wordmark, headline and rule are
  composited on top as real type rather than generated text. Wired as `og:image`
  and `twitter:image` (summary_large_image) with canonical + `og:url` per page.
- **Favicon.** Derived from the real logo mark rather than generated, so it
  cannot fight the wordmark: `assets/favicon.svg` plus 32/180/192/512 PNGs and
  `site.webmanifest`. Verified legible at 16px.
- **Leadership.** Real people, real titles: Craig Jordan (Founder & CEO),
  Tej Badiani (VP Consulting & Operations), Dev Purdon (Senior Director of
  Consulting), Allie Adams (Director of Sales). Name-led cards with the title in
  mono. No headshots — supply four and they can be added.
- **Housekeeping.** `sitemap.xml`, `robots.txt`, `site.webmanifest`.

## Still open

### Proof needs sourcing, not inventing
The two case studies (32% faster cycle, 1 day → 1 hr, 100% automation owned; 0
pipeline lost, 3 weeks to production, 2 → 1 systems of record) and the
unattributed VP RevOps testimonial were lifted from saascend.com. Confirm they
are approved for reuse and correctly attributed. There is still no client-logo
strip — deliberately, since the names on the live site look like placeholders.
Real cleared logos remain the single strongest addition available.

### Leadership scope lines need a read
The one-line accountability description under each name was written here, not
supplied. Check all four say something true before this goes anywhere public.

### Decisions needed from you
Analytics (which, if any) and a custom domain. Both are one commit once chosen.

### Leadership headshots
Four photos would complete the section. Do not generate synthetic headshots for
real named people.

**Standing rule: do not invent client logos, testimonials, headshots or case
figures. Leave the gap and tell me what you need.**

### Accepted, not fixed
At ≤390px the about-page heading breaks as "Generic consultants / configure. /
Systems experts / architect." Left alone on purpose — it is a two-sentence
antithesis, and isolating the verbs *configure* and *architect* carries the
contrast rather than reading as a widow.

## Asset creation — use the Higgsfield CLI

`higgsfield` is installed. If it errors with `No workspace selected` or
`request failed`, stop and ask for `higgsfield auth login` — do not substitute
stock or hand-rolled placeholder art.

```bash
higgsfield account status
higgsfield workspace list
higgsfield workspace set <workspace_id>
```

Default to GPT Image 2 for these — it is the right model for graphic design,
typography and on-image text. Pass `--wait` so the command blocks and prints
the URL.

**Social card** (`assets/og-card.png`, 1200×630, referenced from `og:image` and
`twitter:image` on all six pages):

```bash
higgsfield generate create gpt_image_2 \
  --prompt "Abstract architectural cross-section of five stacked horizontal \
strata, thin luminous cyan seams along each layer boundary, deep navy #031F49 \
ground fading to #01142F, precise engineered geometry, no text, no logos, \
generous negative space in the upper left for an overlaid wordmark, restrained \
premium editorial feel, flat graphic not photographic" \
  --aspect_ratio 16:9 --resolution 2k --wait
```

**Favicon source** (`assets/icon-512.png`, square, must stay legible at 16px):

```bash
higgsfield generate create gpt_image_2 \
  --prompt "Minimal square app icon, single ascending peak mark formed by two \
converging strokes, cyan #00ACD4 on deep navy #031F49, thick confident \
geometry that survives being scaled to 16 pixels, flat vector, centred, no \
text, no gradients" \
  --aspect_ratio 1:1 --resolution 2k --wait
```

The peak mark must read as the existing SaaScend "A" mark — check it against
`assets/saascend-logo.png` before wiring it in, and regenerate rather than
shipping something that fights the logo.

A hero background texture is **optional and probably unnecessary** — the layer
diagram is already carrying the hero. Only add one if you can show it improves
the composition; the CSS radial washes currently do that job at zero weight.

Download each result, commit it to `assets/`, and reference it by relative path.
Nothing loads from an external host at runtime except Google Fonts.

---

## Verification — regression, not first-look

Build with `python3 build.py`, serve locally, then use Playwright:

- Desktop **1440** and mobile **390**. Emulate mobile properly — a narrow
  headless window renders desktop layout and hides real overflow.
- No horizontal scroll on any page at either width.
- No headline widows. The hero display must break where the markup breaks it.
- The four proof stats stay above the fold on a **720px-tall** laptop.
- Drive the interactive parts and prove they work, don't assume:
  the stack accordion interrupts mid-flight and reverses from its live height,
  the nav sheet tracks 1:1 and dismisses on an upward flick, the marketplace
  filter updates both grid and count, the maturity check completes all six
  questions and lands on a stage.
- Zero console errors on all six pages.
- Confirm the site still renders correctly with JavaScript disabled.

Report what you changed and what you deliberately left alone.
