# SaaScend — Agentic GTM marketing site

Static marketing site for SaaScend, the Agentic GTM Company. No build step, no
dependencies: plain HTML, one stylesheet, one script.

## Design direction

The site's signature is **the load-bearing stack** — five numbered layers (L1 systems &
data → L5 agent workforce) that assemble bottom-up on load. Layer order is the company's
actual argument ("foundation before automation"), so the structural device carries
information rather than decorating it.

Three type roles: **Montserrat** for voice (display, headings, buttons), **Open Sans** for
prose, and **JetBrains Mono** for anything the machine owns — layer ids, metric units,
integration chips, filter counts. Navy strata alternate with ice/white so no two adjacent
sections share a tone.

Motion follows strong ease-out curves (`cubic-bezier(0.23, 1, 0.32, 1)`), UI transitions
stay under 300ms, only `transform`/`opacity` animate, and every resting state is defined in
CSS — JS only adds `.is-in`. `prefers-reduced-motion`, `prefers-reduced-transparency` and
visible keyboard focus are all honoured.

## Pages

| File | Contents |
| --- | --- |
| `index.html` | Hero + the stack, partners, the real cost, Build/Manage/Transform, agent preview, agentic delivery + Scope-to-Quote, outcomes, testimonial |
| `solutions.html` | Build, Manage, Transform in depth |
| `agents.html` | All 33 agents, filterable by GTM team |
| `how-we-work.html` | Maturity model, the six-question maturity check, delivery model, pricing, FAQ |
| `about.html` | Mission, story, six principles, foundation-first, leadership |
| `contact.html` | Scope-your-project form (hands off to `hello@saascend.com`) |

## Assets

- `assets/site.css` — the whole design system, tokens first
- `assets/site.js` — nav, reveals, stack stagger, agent filter, maturity check, form handoff
- `assets/agents-data.js` — the 33-agent catalogue
- `assets/saascend-logo-white.png` — brand master (white text, for dark grounds)

## Editing

Page bodies live in `pages_home.py` / `pages_rest.py`; the shell (head, nav, footer, CTA)
lives in `build.py`. Regenerate all six pages with:

```
python3 build.py
```

Edit the generators, not the HTML — the HTML is output.

## Local preview

```
python3 -m http.server 4331
```
