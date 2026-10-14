# HOWTO — Local Decision Models

## 1. Ticket triage in an afternoon
Pull a decision model in your runtime, write one `choice` question with described options, run 100 labeled tickets through it, and run `python examples/calibrate_threshold.py results.csv`. Ship with the cutoff that keeps accuracy at your target; route the rest to the existing queue.

## 2. Replace an LLM "answer with one word" router
Turn each route into a described `choice` option. Run old router and decision model side by side on a week of traffic; promote when agreement is high and the fallback share is acceptable.

## 3. Check an agent's step
After a tool call, ask a `noul` question: "Did this output complete the requested step?" with the step and output in `state`. Below the cutoff, have the agent retry or escalate. Keep the decision model separate from the agent's own model.

## 4. Moderation with images
Use a vision-capable decision model, send base64 images with a short `state` describing the context, and ask `noul` questions per policy. Check the per-request size limit for images in your runtime.

## 5. Moving between runtimes
Point the client at the other server's base URL. Re-run calibration: a different model or quantization changes the confidence scale.
