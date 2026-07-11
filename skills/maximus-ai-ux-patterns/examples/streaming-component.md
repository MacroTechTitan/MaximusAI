# Example: Streaming Output Component

A React component implementation for streaming AI output using Server-Sent Events (SSE), with proper state management, stop/resume, and error handling.

---

## Architecture overview

```
User input
    ↓
POST /api/chat → returns SSE stream
    ↓
useStreamingResponse hook
    ↓
StreamingMessage component
    ↓
renders tokens progressively
    ↓
settled state: retry/edit/copy controls appear
```

---

## API endpoint (Next.js App Router)

```typescript
// app/api/chat/route.ts
import Anthropic from "@anthropic-ai/sdk";
import { NextRequest } from "next/server";

const client = new Anthropic();

export async function POST(req: NextRequest) {
  const { messages, system } = await req.json();

  const encoder = new TextEncoder();

  const readable = new ReadableStream({
    async start(controller) {
      try {
        const stream = client.messages.stream({
          model: "claude-haiku-3-5",
          max_tokens: 1024,
          system,
          messages,
        });

        for await (const event of stream) {
          if (event.type === "content_block_delta") {
            const chunk = JSON.stringify({ type: "delta", text: event.delta.text });
            controller.enqueue(encoder.encode(`data: ${chunk}\n\n`));
          }
          if (event.type === "message_stop") {
            controller.enqueue(encoder.encode(`data: ${JSON.stringify({ type: "done" })}\n\n`));
          }
        }
      } catch (err) {
        const errChunk = JSON.stringify({ type: "error", message: (err as Error).message });
        controller.enqueue(encoder.encode(`data: ${errChunk}\n\n`));
      } finally {
        controller.close();
      }
    },
  });

  return new Response(readable, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
```

---

## React hook: useStreamingResponse

```typescript
// hooks/useStreamingResponse.ts
import { useCallback, useRef, useState } from "react";

export type StreamState = "idle" | "streaming" | "done" | "error" | "stopped";

export interface StreamingState {
  content: string;
  state: StreamState;
  error: string | null;
  start: (messages: Message[], system?: string) => void;
  stop: () => void;
  reset: () => void;
}

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function useStreamingResponse(): StreamingState {
  const [content, setContent] = useState("");
  const [state, setState] = useState<StreamState>("idle");
  const [error, setError] = useState<string | null>(null);
  const readerRef = useRef<ReadableStreamDefaultReader | null>(null);

  const stop = useCallback(() => {
    readerRef.current?.cancel();
    setState("stopped");
  }, []);

  const reset = useCallback(() => {
    setContent("");
    setState("idle");
    setError(null);
  }, []);

  const start = useCallback(async (messages: Message[], system = "") => {
    reset();
    setState("streaming");

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages, system }),
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      readerRef.current = reader;
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const data = JSON.parse(line.slice(6));

          if (data.type === "delta") {
            setContent((prev) => prev + data.text);
          } else if (data.type === "done") {
            setState("done");
          } else if (data.type === "error") {
            setError(data.message);
            setState("error");
          }
        }
      }
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        setError((err as Error).message);
        setState("error");
      }
    }
  }, [reset]);

  return { content, state, error, start, stop, reset };
}
```

---

## StreamingMessage component

```tsx
// components/StreamingMessage.tsx
import { useEffect, useRef } from "react";
import { StreamState } from "../hooks/useStreamingResponse";

interface Props {
  content: string;
  state: StreamState;
  error: string | null;
  onRetry: () => void;
  onEdit: () => void;
  onStop: () => void;
}

export function StreamingMessage({ content, state, error, onRetry, onEdit, onStop }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom during streaming
  useEffect(() => {
    if (state === "streaming") {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [content, state]);

  if (error) {
    return (
      <div className="message-error" role="alert">
        <p>Something went wrong. {error}</p>
        {/* Show partial content if any was received before the error */}
        {content && (
          <div className="partial-content">
            <p className="partial-label">Partial response:</p>
            <div className="content">{content}</div>
          </div>
        )}
        <button onClick={onRetry} className="btn-retry">Try again</button>
      </div>
    );
  }

  return (
    <div className="message-container" aria-live="polite" aria-atomic="false">
      {/* Main content area */}
      <div className="message-content">
        {content}
        {/* Pulsing cursor while streaming */}
        {state === "streaming" && (
          <span className="streaming-cursor" aria-hidden="true" />
        )}
      </div>

      {/* Scroll anchor */}
      <div ref={bottomRef} />

      {/* Controls: only visible when settled */}
      {(state === "done" || state === "stopped") && (
        <div className="message-controls" role="toolbar" aria-label="Response options">
          <button onClick={onRetry} title="Regenerate response">
            ↺ Retry
          </button>
          <button onClick={onEdit} title="Edit your message">
            ✎ Edit
          </button>
          <button
            onClick={() => navigator.clipboard.writeText(content)}
            title="Copy to clipboard"
          >
            ⎘ Copy
          </button>
        </div>
      )}

      {/* Stop button: only visible while streaming */}
      {state === "streaming" && (
        <div className="message-controls">
          <button onClick={onStop} title="Stop generating">
            ◼ Stop
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## CSS (streaming cursor animation)

```css
/* streaming-cursor.css */
.streaming-cursor {
  display: inline-block;
  width: 2px;
  height: 1.1em;
  background-color: currentColor;
  margin-left: 1px;
  vertical-align: text-bottom;
  animation: cursor-blink 0.9s ease-in-out infinite;
}

@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* Disable animation when prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .streaming-cursor {
    animation: none;
    opacity: 1;
  }
}
```

---

## Design notes

- **Controls hidden during streaming**: retry/edit/copy are disabled during generation. A user copying a partial response gets a truncated string — prevent this by keeping controls hidden until `state === "done"`.
- **Stop preserves partial output**: when the user stops streaming, the partial output stays visible with a "stopped" state. Do not clear the content — partial output is often useful.
- **Error shows partial output**: if the stream errors after partial content, show both the partial content and the error. Don't discard what arrived.
- **Aria-live region**: the `aria-live="polite"` on the message container ensures screen readers announce content updates without interrupting the user. Use `polite` (not `assertive`) for streaming content.
- **Scroll behavior**: auto-scroll during streaming is expected behavior (ChatGPT, Claude). Pause auto-scroll if the user manually scrolls up — they're reading, not waiting.

---

## Testing checklist

- [ ] First token renders in <500ms on a fast connection
- [ ] Cursor pulses during streaming
- [ ] Stop button cancels the stream, partial output preserved
- [ ] Controls appear immediately when stream ends
- [ ] Error state shows partial output + retry button
- [ ] Streaming works at 50kbps (throttle in DevTools)
- [ ] Screen reader announces content (use NVDA or VoiceOver to verify)
- [ ] Cmd+Z doesn't clear the streaming output
