# Reference — Inference Patterns

A catalog of the inference types used in the confidence ledger's `inference_type` field. Every derived claim in a Deep Research Pro output should be tagged with one of these. If a claim doesn't fit any of them, it's probably not actually an inference yet — it's a fact or a guess, and should be labeled as such.

---

## Direct citation

A source states the claim outright, in those terms. This is the weakest form of "inference" in this catalog — it's really aggregation, not reasoning. Still worth tagging explicitly, because a ledger full of direct citations with no triangulation, deduction, or adversarial pass is a signal the research never actually got to inference.

**Example:** "Company X's pricing page states $20/seat/month." — the page says it; nothing was derived.

**Rule of thumb:** fine as a supporting fact. Never sufficient alone for a claim with medium-or-higher stakes riding on it, unless corroborated by at least a second independent source or a survived adversarial pass.

## Triangulation

Three or more independent sources each state a different, individually-incomplete fact; combined, they imply an answer none of them states. Independence matters — three sources repeating the same original claim is not triangulation, it's one data point wearing three costumes.

**Example:** headcount (source 1) × sector revenue-per-employee benchmark (source 2) × a valuation-multiple back-solve from a funding announcement (source 3) triangulate a private company's approximate ARR. See `examples/triangulation-trace.md` for the full worked version.

**Check before tagging:** are the sources actually independent (different methodology, different original reporting), or do they all trace back to one press release or one analyst?

## Deduction

If A is true and B is true, C follows necessarily — not probably, necessarily, given the premises. Deduction is only as strong as its premises; a valid deduction from a shaky premise produces a confidently wrong conclusion.

**Example:** if cached tokens are billed at a 90% discount only on cache hits (A), and hit rate depends on prefix stability across requests (B), then total cost savings equal roughly `hit_rate × 90%`, not a flat 90% (C). See `examples/hypothesis-falsification-trace.md`.

**Check before tagging:** are both premises independently verified facts, not assumptions smuggled in?

## Elimination

Enumerate the plausible alternatives, rule out all but one with evidence. The strength of an elimination argument depends entirely on whether the enumeration was actually exhaustive — a common failure is eliminating the alternatives you thought of and missing the one you didn't.

**Example:** a cost-structure sanity check that rules out an ARR estimate being either implausibly low (unsustainable burn) or implausibly high (headcount too small for that revenue scale in the sector), narrowing the plausible band without pinpointing an exact figure.

**Check before tagging:** state the alternatives considered explicitly in the trace. If you can't list them, the elimination wasn't rigorous — it was a hunch.

## Base-rate reasoning

Combine a prior (how often does this class of event or outcome happen, in general) with case-specific evidence to reach a probability — not a binary yes/no. This is the correct pattern for forecasting questions ("what's the probability X happens by date Y").

**Example:** most funding rounds of a given size close within a certain timeframe of term-sheet signing (base rate); case-specific reporting suggests this round is on a normal timeline (case evidence) → moderately high probability it closes on the expected schedule, not a certainty.

**Check before tagging:** is the base rate itself sourced (historical data, published statistics), or is it a guess dressed as a prior? An unsourced "base rate" is not base-rate reasoning — it's an assumption.

## Expert consensus

Multiple domain experts converge on a view, weighted by both expertise and independence. The critical discipline here is distinguishing genuine independent consensus from an echo chamber — five commentators citing the same original analyst is one opinion, not five.

**Example:** independent security researchers, with no commercial relationship to each other or the vendor, separately assess a vulnerability's severity similarly.

**Check before tagging:** trace each "expert" opinion back to its origin. If two or more trace back to the same original source, they count as one data point in the consensus, not two.

## Negative evidence

The absence of an expected signal is itself evidence. If something would clearly be visible or announced were it true (a company would trumpet a metric if it were good, a regulator would have flagged an issue if it existed at the scale claimed), its absence is informative — weaker than positive evidence, but not nothing.

**Example:** a company that aggressively publicizes growth metrics goes conspicuously silent on a specific metric after a milestone quarter — the silence, combined with the company's established pattern of publicizing good news, is negative evidence about that metric's trajectory.

**Check before tagging:** negative evidence is only meaningful against an established baseline of what *would* be expected to surface. Absence of evidence with no such baseline is just absence of evidence — don't over-weight it.

## Analogical reasoning (use with explicit warnings)

Reasoning from a similar case to the case at hand: "company/technology/event A behaved this way under similar conditions, so B likely will too." This is the weakest pattern in this catalog and should be flagged as such every time it's used — analogies fail silently when the underlying conditions differ in ways that weren't checked.

**Example:** "Competitor A's pricing change led to X% churn; Company B is making a similar change, so expect roughly similar churn" — valid only to the extent the customer bases, switching costs, and market conditions are actually comparable, which needs to be checked, not assumed.

**Rule:** never assign "high" confidence to a claim resting solely on analogical reasoning. State the disanalogies you checked for, even the ones that didn't apply.

---

## Using this catalog in the ledger

Tag every derived claim with exactly one primary inference type (the one doing the most work). If a claim uses two patterns in sequence — e.g., base-rate reasoning to get a prior, then triangulation to adjust it — say so in the evidence summary rather than trying to force a single tag; the reasoning trace is where that nuance belongs.
