# Maximus AI

Collection of AI agents and tools built by [Macro Tech Titan](https://github.com/MacroTechTitan).

## Agents

| Agent | Description | Stack |
|---|---|---|
| [`agents/recruiter-deep-find`](./agents/recruiter-deep-find) | Recruiter intake form + live deep-search powered by Perplexity Sonar. Sources candidates from DevOps agencies, dev shops, outsourcing firms, MSPs, and technical staffing agencies. | React + Vite, Express, Perplexity Sonar API |
| [`agents/find-shareholders`](./agents/find-shareholders) | Input one or more company names (public or private), get institutional shareholders (funds) and named individuals at those funds. Exports CSVs shaped for Folk and Apollo enrichment. | React + Vite, Express, Perplexity Sonar API |

## Layout

```
MaximusAI/
└── agents/
    └── <agent-name>/        each agent is a self-contained project
        ├── package.json
        ├── README.md
        └── …
```

Each agent ships standalone — you can clone the whole repo or copy just one `agents/<name>/` directory into another project.

## Getting started

Pick an agent:

```bash
git clone https://github.com/MacroTechTitan/MaximusAI.git
cd MaximusAI/agents/recruiter-deep-find
npm run install:all
cp .env.example .env   # add your API keys
npm run dev
```

See each agent's own README for details.

## License

MIT
