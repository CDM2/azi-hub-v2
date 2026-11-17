# Permission service: contract for the spike

Written before the service, so the tests in `../tests/` can be written first. The service is the spike's stand-in for R-01 option D's permission layer: identity, the tier map, the tier-filtered second brain, and the one curated path out of the personal space.

## Rules it must enforce (N-02, N-03, N-08, F-24, founder input of 2026-11-15)

1. The organization a caller acts for comes from its token and nothing else. No tool takes an organization as an argument.
2. The database decides what a caller reads and writes: row-level security on every table an agent touches, forced, for a role that owns nothing and cannot bypass it. The service adds no filter of its own that the database does not also apply.
3. A sub-organization reads its own pages and global pages. A sibling's pages are never returned and their existence is not revealed.
4. The holding organization also reads its sub-organizations' pages (`holding_reads = all`, AZI Hub's current behaviour) or only their summaries (`holding_reads = summaries`).
5. The personal space reads everything in its organizations. No organization reads a personal page.
6. The only path from personal to an organization is a curated briefing of at most 2,000 characters, published by the personal space and approved by the human before the holding organization can see it. A switch turns briefings off; then nothing goes from personal to any organization and earlier briefings are hidden.
7. A second switch turns the personal space off. Its token stops working and the product runs as organizations only.
8. Health and finance pages can be stored only in the personal space. The database refuses them anywhere else.
9. Each page records how it came to exist: `human`, `agent` or `codebase`. The service sets this from the caller's kind; a caller cannot choose it.
10. Every call, allowed or denied, is written to an append-only audit log.

## Interfaces

**MCP over HTTP**, `POST /mcp`, JSON-RPC 2.0, header `Authorization: Bearer <token>`. Tools:

| Tool | Arguments | Returns |
| --- | --- | --- |
| `brain_whoami` | none | `{org, kind, actor}` |
| `brain_list` | `source_type?`, `kind?`, `limit?` | `{count, pages: [{id, org, title, kind, source_type, path}]}` |
| `brain_search` | `query`, `source_type?`, `limit?` | `{count, pages: [{id, org, title, kind, source_type, path, snippet}]}` |
| `brain_get` | `id` or `path` | `{page}`; a page the caller may not read gives the same error as one that does not exist |
| `brain_write` | `title`, `body`, `kind?`, `sensitivity?`, `visibility?` | `{id}`; always in the caller's own organization |
| `publish_briefing` | `content` | `{briefing_id, status: "pending"}`; personal space only |

Every tool also accepts `request_id`, which is copied into the audit log. Tool results are one text item holding JSON. Errors are tool results with `isError: true` and `{error: <code>}`; codes are `not_found`, `forbidden`, `invalid_arguments`, `disabled`.

**Admin over HTTP**, header `Authorization: Bearer <admin token>`. In the spike this stands in for the human's own console.

| Route | Body | Purpose |
| --- | --- | --- |
| `POST /admin/reset` | a fixture: `settings`, `orgs`, `principals`, `pages` | Wipe and load made-up data |
| `POST /admin/settings` | any of `personal_enabled`, `briefing_enabled`, `holding_reads` | Flip a switch |
| `POST /admin/approve_briefing` | `briefing_id`, `approver` | Human approval; creates the briefing page in the holding organization |
| `POST /admin/codebase_sync` | `org`, `upserts: [{path, title, body, kind, meta, content_sha}]`, `deletes: [path]` | The mapper's write path; pages are stored as `codebase` |
| `GET /admin/audit` | query `since_id` | Read the audit log |
| `GET /admin/pages_digest` | query `org`, `source_type` | `[{path, content_sha}]`, for comparing an incremental update with a full rebuild |

**Database**, schema `brain`: tables `orgs`, `principals`, `pages`, `briefings`, `settings`, `audit`. Function `brain.begin_session(token text)` binds the current transaction to the token's organization; nothing else can. Role `brain_app` is what the service uses for agent calls.
