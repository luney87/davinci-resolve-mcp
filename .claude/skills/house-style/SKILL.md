---
name: house-style
description: The editorial and finishing preferences this project's work is judged against — cut rhythm, shot selection, delivery conventions, and the corrections that have already been given. Load before assembling, restructuring, or refining any cut so the same note does not have to be given twice.
user-invocable: false
---

# House Style

The craft guides in `docs/guides/` describe editing in general. This file
describes **how this editor wants it done** — the accumulated, specific
corrections that would otherwise have to be repeated every session.

Read it before any edit task. Append to it whenever a correction is given.

## The capture protocol

This file is only worth what gets written into it. When the user corrects an
editorial decision — rejects a cut, changes a shot choice, adjusts a duration,
says "not like that" — do not just fix it. Fix it, then add the rule here.

A useful entry has three parts:

- **The rule**, stated as an instruction, not an observation.
- **Why**, in the user's terms — what it was in service of.
- **The trap**, if there is one: what makes it easy to get wrong.

Write rules that are falsifiable. "Cut on motion" is a rule; "make it feel
dynamic" is not. If a correction is one-off and situational, it does not belong
here — this file is for what generalizes.

When an entry turns out to be wrong or too broad, edit it. A stale rule
confidently followed is worse than no rule.

---

## Pacing and rhythm

<!-- Hold lengths, when to cut early, what "too long" means for this material. -->

_Not yet captured._

## Shot selection

<!-- What earns a place in the cut; what gets dropped even when it's a good shot. -->

_Not yet captured._

## Cut points

<!-- Cut on motion vs on rest, handles, how much air before and after a beat. -->

_Not yet captured._

## Structure and openings

<!-- How a piece starts, what the first frames have to do, how it lands. -->

- **A cold-open teaser must tell the viewer what the episode is about, not
  collect "best moments."** Every bite must be a self-contained, concrete
  statement (a list, a number, a piece of advice), and the bites in sequence
  must read as one coherent mini-argument: topic → thesis → payoff. No
  mid-sentence fragments whose context lives elsewhere in the episode.
  **Why:** the editor rejected two intros built as highlight reels ("intro
  jak zwykle kompletnie bez sensu — słuchacz nie będzie miał pojęcia o czym
  mowa"). The approved WYWIAD 2 intro is the reference: "Make sure you know
  your competition." → channel list → challenges → "first paying customer
  within a year." **The trap:** a line that is impressive *inside* its answer
  ("Honestly, I spent 10 years in hospitality") is noise *outside* it — test
  each bite by asking what a first-time viewer learns about the episode from
  it alone.
- **An answer-bite needs its question (or an equivalent setup) in front of
  it.** Even a concrete list ("commercial real estate, mining, wholesalers…")
  reads as noise when the viewer doesn't know what prompted it — open the
  teaser with the interviewer's question or a framing line, then the answer.
  **Why:** second correction on the same intro: "początek jest zawieszony bez
  kontekstu — wymienia branże, ale dlaczego? Coś przed to wymienianie trzeba
  dać." **The trap:** the editor also said a teaser may run a few seconds
  over the nominal length ("może być intro trochę dłuższe niż 30 sekund") —
  don't sacrifice the setup line to hit a round number.

## Rejected by default

Things not to add unless explicitly asked. Seeded from the rough-cut deliverable
contract in the `resolve-rough-cut` skill, which exists because this work gets
thrown away:

- Titles, captions, and text cards
- Transitions (an assembly is hard cuts)
- Effects and speed ramps
- Music beds
- Grading on a cut that was asked for as an assembly

## Delivery conventions

<!-- Aspect ratios, timeline naming, versioning, where renders go. -->

_Not yet captured._

---

## Where personal grading taste lives

Colour and look preferences are **not** kept here — this file travels with the
repository. Grading taste lives in the user-level `colorist-assistant` skill and
in persistent memory. Load those for look selection, grade transfer, and the
Resolve API traps around them.

If any entry below would be specific to one person rather than to this project's
work, it belongs in the user-level skill instead, and this file should be
gitignored rather than committed.
