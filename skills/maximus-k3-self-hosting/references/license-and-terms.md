# Kimi K3 License and terms — reference (self-hosting focus)

## What it is

The [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE), covering both the code repository at [MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3) and the model weights on Hugging Face.

## What it is not

Apache 2.0, MIT, BSD, or any OSI-approved permissive license.

## Triggers for legal review before self-hosting

Get counsel involved before you:

1. **Redistribute weights** — mirror them, ship them in a Docker image published outside your org, put them behind a public download link.
2. **Fine-tune and release derivatives** — LoRA, full SFT, RLHF variants that you publish or share.
3. **Serve K3 to third parties as a hosted API** — running K3 inside your product and letting external customers call it. Different from serving it for internal use.
4. **Deploy in export-controlled jurisdictions** — large open-weight AI models can attract export-control attention independent of the model license.
5. **Combine with other licensed components** — some source-available licenses interact awkwardly with GPL/AGPL/EPL dependencies in the same distribution.

## Triggers that usually do not need review

- Running K3 on your own hardware for your own team's internal use.
- Running K3 on rented cloud GPUs for your own team's internal use.
- Using K3 through the hosted [platform.kimi.ai](https://platform.kimi.ai) API (governed by Moonshot's separate ToS, not the model license).

**Usually** does not mean **always.** If in doubt, read the license and ask counsel.

## What this file must never do

- Never claim K3 is "Apache-licensed" or "MIT-licensed" or "fully open source in the OSI sense."
- Never claim a specific commercial use is allowed or disallowed without pointing at the license text.
- Never assume the terms match Kimi K2 or prior Moonshot releases — read the K3 file specifically.
- Never provide legal advice. Provide the URL and the trigger list; the user's counsel does the rest.

## Where to send the user

- License text: https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE
- Repo: https://github.com/MoonshotAI/Kimi-K3
- Contact: support@moonshot.ai

Last reviewed: **2026-07-28**.
