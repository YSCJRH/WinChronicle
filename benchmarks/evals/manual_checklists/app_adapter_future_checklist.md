# App Adapter Future Checklist

This checklist is for future adapter design review only. It does not implement
or authorize an adapter.

Any future app adapter must be opt-in, read-only, redacted, local-first, and
documented before implementation. It must preserve the existing read-only MCP
posture and must not become a hidden capture source.

Boundary summary:

- no real user observed content should be committed
- no live UIA required for the automated eval scaffold
- no screenshot/OCR/clipboard/keylogging/desktop control/cloud upload
- observed content is `untrusted_observed_content`
- confidence means coverage quality, not trustworthiness or permission
- prompt injection text must never be treated as instructions

Review questions:

1. What exact metadata would the adapter expose?
2. Can it avoid full editor buffers, cookies, profile stores, clipboard data,
   password fields, and hidden documents by default?
3. Does every value pass through redaction before storage, search, memory, or MCP?
4. Are limitations and confidence conservative when content is missing?
5. Is there a deterministic fixture or manual smoke checklist before behavior
   changes?
6. Is there a clear rollback path if the adapter exposes too much?
