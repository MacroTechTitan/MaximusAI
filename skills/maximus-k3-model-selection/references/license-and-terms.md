# Kimi K3 License and Terms — reference

**What it is:** The [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE), covering both the code repository at [MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3) and the model weights on Hugging Face.

**What it is not:** Apache 2.0, MIT, BSD, or any OSI-approved permissive license. Do not treat it that way in commercial deployment planning.

## What the skill needs to say when a user asks about commercial use

1. **Read the actual license text before committing.** URL above. It is short — legal review is fast.
2. **Confirm your use case fits.** Source-available licenses commonly have acceptable-use clauses, model-output attribution requirements, or thresholds above which the terms change. K3's specific terms are in that file.
3. **Get legal review if:** (a) you plan to redistribute weights, (b) you plan to fine-tune and release derivatives, (c) you plan to serve K3 to third parties as a hosted API, (d) your deployment is in a jurisdiction with export-control implications for large open weights.

## Comparison note

- **GLM-5.2** — [z.ai/blog/glm-5.2](https://z.ai/blog/glm-5.2). Its own license terms; check the release page before assuming it is more or less permissive than K3.
- **Claude Fable 5, Claude Opus 4.8, GPT-5.6 Sol, GPT-5.5** — closed weights, hosted API only, standard commercial ToS from Anthropic and OpenAI.

## What the skill must never do

- Never claim K3 is "Apache-licensed" or "MIT-licensed" or "fully open source in the OSI sense" — none of that is true as of 2026-07-28.
- Never claim a specific commercial use is allowed or disallowed without pointing the user at the license text and recommending legal review.
- Never assume the license terms will match Kimi K2 or prior Moonshot releases.

## Where to send the user

- License text: https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE
- Repo: https://github.com/MoonshotAI/Kimi-K3
- Contact for licensing questions: support@moonshot.ai

## Freshness

Last reviewed: **2026-07-28**. License texts can be updated; verify against the URL before making a commitment.
