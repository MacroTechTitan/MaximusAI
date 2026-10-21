# Package hallucination and slopsquatting — facts and sources (pulled 2026-10-21)

| Fact | Source |
|---|---|
| USENIX Security 2025 study: 16 code LLMs, 576,000 samples; hallucinated packages averaged at least 5.2% (commercial) and 21.7% (open-source); 205,474 unique invented names | https://arxiv.org/abs/2406.10279 |
| 2026 replication on five models released Oct 2025-Mar 2026: 199,845 generations, overall rates 4.62% to 6.10%, Python higher than JavaScript for every model; 127 names invented by all five (109 PyPI, 18 npm), 53 registrable as of April 2026; no agentic or retrieval setup tested | https://www.matthewswong.com/en/blog/slopsquatting-2026-frontier-models-package-hallucination/ (Oct 17, 2026) |
| Most-invented PyPI names in that replication include `aws-cdk` (real: `aws-cdk-lib`), `opentelemetry` (real: `opentelemetry-api`/`-sdk`), `rest-framework` (real: `djangorestframework`) | same |
| react-codeshift (Jan 2026): name never registered, a conflation of `jscodeshift` and `react-codemod`; first appeared in one commit of 47 LLM-generated agent skills; spread to 237 repositories; agents kept triggering `npx` installs after the researcher claimed it | https://www.aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks |
| Payloads typically run post-install scripts to steal API keys, cloud tokens, npm tokens; some fetch the payload from a URL at install time to evade static scanners; download count is not a reliable signal | same |
| Live check by the scout, 2026-10-21: `pypi.org/pypi/aws-cdk/json` returned 404; `registry.npmjs.org/react-codeshift` shows `time.created` 2026-01-14 | run of `examples/vet_package.py` |
| Trend coverage within 30 days: BleepingComputer (Oct 17), CSO Online (Oct 20), TechTarget (Oct 21), Xygeni (Oct 10-11) | https://www.bleepingcomputer.com/news/security/slopsquatting-phantom-domains-and-hallusquatting-are-the-same-ai-attack/amp/ · https://www.csoonline.com/article/4167465/supply-chain-attacks-take-aim-at-your-ai-coding-agents.html · https://www.techtarget.com/it-strategy/feature/Slopsquatting-explained-When-AI-code-turns-malicious · https://xygeni.io/blog/slopsquatting-evolution/ |
| npm `ignore-scripts`: npm does not run package.json scripts; explicit `npm run`/`test`/`start` still run their script but not pre/post scripts | https://docs.npmjs.com/cli/v11/using-npm/config#ignore-scripts |
| npm `min-release-age` (days) and `before` (date); `min-release-age-exclude` exempts names; a blocked audit fix keeps the vulnerable version and exits non-zero | https://docs.npmjs.com/cli/v11/using-npm/config |
| uv `exclude-newer` accepts RFC 3339 timestamps or durations such as `7 days`/`P7D`, compared against each file's upload time; `exclude-newer-package` sets per-package cutoffs or `false` to exempt | https://docs.astral.sh/uv/reference/settings/#exclude-newer |
| pip hash-checking mode: `--require-hashes`; all requirements and dependencies need hashes and `==` pins; sha256 recommended; also `--only-binary :all:` (pip docs v26.2.1) | https://pip.pypa.io/en/stable/topics/secure-installs/ |
| PyPI JSON API: `GET /pypi/<project>/json` with `releases` and per-file `upload_time_iso_8601` | https://docs.pypi.org/api/json/ |
| npm registry: `GET /{package}` returns the packument with `time` (`created`, `modified`) and `maintainers` | https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md |

Volatile: hallucination rates, setting names, and registry behaviour. Recheck before relying on them.
