# Example: Citation UI

Implementation patterns for source attribution in AI-generated output. Covers superscript citations (Perplexity pattern), inline source chips, and a source panel.

---

## Attribution pattern selection guide

| Context | Pattern | Example product |
|---|---|---|
| Dense factual content, multiple sources per response | Superscript citations + numbered list | Perplexity |
| Conversational, mobile-first | Inline source chips | Bing Copilot |
| Long research documents | Source panel (side-by-side) | Perplexity Deep Research |
| Single authoritative source | Inline citation link | Many RAG chatbots |

---

## Pattern 1: Superscript citations (Perplexity pattern)

### Backend: attach source metadata to response

```python
# response_with_sources.py
from dataclasses import dataclass


@dataclass
class Source:
    index: int
    url: str
    title: str
    domain: str
    snippet: str  # 1-2 sentence preview


@dataclass
class CitedResponse:
    text: str            # "The Eiffel Tower is 330m tall[1] and was built in 1889[2]."
    sources: list[Source]


def build_cited_response(raw_text: str, retrieved_chunks: list[dict]) -> CitedResponse:
    """
    Build a CitedResponse by mapping [N] markers in the model output
    to source metadata from retrieved chunks.

    The LLM should be instructed to add [N] markers inline:
    system prompt: "Cite each claim with [N] where N is the source number.
                    Use only sources provided in the context."
    """
    sources = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        sources.append(Source(
            index=i,
            url=chunk["url"],
            title=chunk["title"],
            domain=_extract_domain(chunk["url"]),
            snippet=chunk["text"][:200].strip() + "…",
        ))
    return CitedResponse(text=raw_text, sources=sources)


def _extract_domain(url: str) -> str:
    from urllib.parse import urlparse
    return urlparse(url).netloc.removeprefix("www.")
```

### Frontend: render citations

```tsx
// components/CitedResponse.tsx
import { useState } from "react";

interface Source {
  index: number;
  url: string;
  title: string;
  domain: string;
  snippet: string;
}

interface Props {
  text: string;
  sources: Source[];
}

/**
 * Renders text with [N] citation markers as superscript links.
 * On hover: shows a tooltip with source title, domain, and snippet.
 * On click: opens source in a new tab.
 */
export function CitedResponse({ text, sources }: Props) {
  const [activeTooltip, setActiveTooltip] = useState<number | null>(null);

  // Parse text and replace [N] markers with citation components
  const parts = text.split(/(\[\d+\])/g);

  return (
    <div className="cited-response">
      <p className="response-text">
        {parts.map((part, i) => {
          const match = part.match(/^\[(\d+)\]$/);
          if (!match) return <span key={i}>{part}</span>;

          const index = parseInt(match[1]);
          const source = sources.find((s) => s.index === index);
          if (!source) return <span key={i}>{part}</span>;

          return (
            <span key={i} className="citation-wrapper">
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="citation-superscript"
                onMouseEnter={() => setActiveTooltip(index)}
                onMouseLeave={() => setActiveTooltip(null)}
                aria-label={`Source ${index}: ${source.title}`}
              >
                <sup>{index}</sup>
              </a>
              {activeTooltip === index && (
                <div className="citation-tooltip" role="tooltip">
                  <div className="tooltip-domain">
                    <img
                      src={`https://www.google.com/s2/favicons?domain=${source.domain}`}
                      alt=""
                      className="favicon"
                      width={14}
                      height={14}
                    />
                    <span>{source.domain}</span>
                  </div>
                  <p className="tooltip-title">{source.title}</p>
                  <p className="tooltip-snippet">{source.snippet}</p>
                </div>
              )}
            </span>
          );
        })}
      </p>

      {/* Source list at the bottom */}
      {sources.length > 0 && (
        <div className="source-list" aria-label="Sources">
          <h3 className="source-list-heading">Sources</h3>
          <ol className="source-items">
            {sources.map((source) => (
              <li key={source.index} className="source-item">
                <img
                  src={`https://www.google.com/s2/favicons?domain=${source.domain}`}
                  alt=""
                  width={14}
                  height={14}
                />
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="source-link"
                >
                  {source.title}
                </a>
                <span className="source-domain">{source.domain}</span>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}
```

### CSS

```css
/* citation.css */
.citation-superscript {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 0.75em;
  vertical-align: super;
  line-height: 0;
  padding: 0 1px;
  cursor: pointer;
}

.citation-superscript:hover sup {
  text-decoration: underline;
}

.citation-wrapper {
  position: relative;
  display: inline;
}

.citation-tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  width: 280px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 10px 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  z-index: 100;
  pointer-events: none;
}

.tooltip-domain {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
  font-size: 0.75rem;
  color: var(--color-muted);
}

.tooltip-title {
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0 0 4px;
  line-height: 1.3;
}

.tooltip-snippet {
  font-size: 0.8rem;
  color: var(--color-muted);
  margin: 0;
  line-height: 1.4;
  /* Clamp to 3 lines */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.source-list {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.source-list-heading {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-muted);
  margin: 0 0 8px;
}

.source-items {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.source-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
}

.source-link {
  color: var(--color-primary);
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 240px;
}

.source-link:hover {
  text-decoration: underline;
}

.source-domain {
  color: var(--color-muted);
  font-size: 0.75rem;
  flex-shrink: 0;
}
```

---

## Pattern 2: Inline source chips (conversational)

For conversational interfaces where superscript markers feel too academic:

```tsx
// InlineSourceChip.tsx
interface ChipProps {
  source: Source;
}

export function InlineSourceChip({ source }: ChipProps) {
  return (
    <a
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      className="source-chip"
      title={source.title}
    >
      <img
        src={`https://www.google.com/s2/favicons?domain=${source.domain}`}
        alt=""
        width={12}
        height={12}
      />
      <span>{source.domain}</span>
    </a>
  );
}
```

```css
.source-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  background: var(--color-surface-raised);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  font-size: 0.72rem;
  color: var(--color-muted);
  text-decoration: none;
  vertical-align: middle;
  margin: 0 2px;
}

.source-chip:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}
```

---

## Streaming citations

For streaming responses, render citations as they arrive rather than waiting for the full response:

```typescript
// Parse citations out of streaming chunks
function parseStreamingCitations(
  accumulatedText: string,
  sources: Source[]
): { displayText: string; citationsFound: Source[] } {
  const foundIndices = new Set<number>();
  const matches = accumulatedText.matchAll(/\[(\d+)\]/g);

  for (const match of matches) {
    const index = parseInt(match[1]);
    const source = sources.find((s) => s.index === index);
    if (source) foundIndices.add(index);
  }

  return {
    displayText: accumulatedText,
    citationsFound: sources.filter((s) => foundIndices.has(s.index)),
  };
}
// Render the source list progressively as citationsFound grows.
// This is the Perplexity pattern: citations appear in the source list
// as they are referenced in the streaming text.
```

---

## Accessibility notes

- Citation superscripts must have `aria-label` attributes: "Source 1: [title]". Screen readers don't read superscript numbers meaningfully without this.
- Tooltips should be keyboard-accessible: focus the citation link to show the tooltip (`:focus` triggers same as `:hover`).
- Source list should have `aria-label="Sources"` so screen reader users can navigate to it.
- External links must have `target="_blank"` AND `rel="noopener noreferrer"` for security.
- Never use color alone to distinguish citations — use the superscript position as the primary visual signal.
