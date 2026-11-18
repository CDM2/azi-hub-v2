# Permission service: contract after the REV-01 fix pass

This replaces `spikes/r-02/service/CONTRACT.md` for the service in this folder. The R-02 contract and service are unchanged and stay as evidence. Rules are numbered as in R-02 where they survive; a changed or new rule says so and names the review finding (`docs/reviews/REV-01_R-01_AND_R-02.md`).

## Rules it must enforce (N-02, N-03, N-08, F-24 to F-27, F-31, founder input of 2026-11-17)

1. The organization a caller acts for comes from its token and nothing else. **Changed (RV-18):** `brain_get` takes an optional `org`. It can only narrow a lookup to an organization the token may already read. It never widens one.
2. **Changed (RV-05, RV-06, RV-19).** The database decides what a caller reads and writes, and it does so in functions. The service's database login has no privilege on any table. It can call the functions listed under "Database" and nothing else. Each function reads the caller's organization from a session that only `brain.begin_session(token)` can bind. Row-level security stays switched on with no policy for that login, as a second lock against a grant made by mistake. R-02 put the rule in row-level security policies on a table the login could query; that let the login time a query, read a query plan and slow every reader down as the table grew.
3. A sub-organization reads its own pages and the approved global pages of the holding organization above it. A sibling's pages are never returned and their existence is not revealed. **Changed (RV-06):** a lookup of a page in an organization the caller may not read runs the same statements as a lookup of a page that does not exist, and no statement compares the id or path of such a page. A read does not visit another organization's rows.
4. **Changed (RV-03).** An organization reads its direct sub-organizations as each one allows: `all`, `summaries` or `none`. A sub-organization's own setting wins. Without one, the default is `none` when the sub-organization has a member who does not control the organization above (a second person), and the deployment's `holding_reads` (`all` or `summaries`) otherwise.
5. **Changed (RV-03).** A person's personal space reads every organization that person belongs to, and nobody else's. No organization and no other person reads a personal page. "Belongs" is decided by walking up from the organization: the first organization that has a member list decides. The person belongs if they are on that list; when the list is on an organization above, they must be an owner on it. So an owner of a holding organization belongs to its ventures, a plain member of it does not, and a venture with its own member list is closed to anyone not on that list.
6. **Changed (RV-15, founder input 2026-11-17).** Text leaves a personal space only as a push of at most 2,000 characters that the person approves. The target is an organization the person belongs to: `to` names it, and without `to` it is the one top-level organization the person owns. An agent cannot approve, including the agent of that personal space. Another person cannot approve. The person is shown the text before deciding. A push's text and route cannot change after it is written, and it is decided once. Two switches turn this off, one for the deployment and one per person: with either off nothing new is offered or approved and earlier briefings from that person are hidden.
7. **Changed (RV-03, RV-15).** The personal space has two switches, one for the deployment and one per person. With either off, that space's tokens stop working and nothing pending from it can be approved. Other people are unaffected.
8. Health and finance pages can be stored only in a personal space. The database refuses them anywhere else.
9. Each page records how it came to exist: `human`, `agent` or `codebase`. The service sets this from the caller. **New:** it also records the person behind the token, when there is one (`written_by`).
10. **Changed (RV-07, RV-08, RV-19, founder input 2026-11-17).** Every call is written to one append-only log: every tool call, allowed or denied; every other protocol message; every refused token; and every operator action that changes or shows data. The function that performs an allowed call writes its row in the same transaction, so the service cannot return pages without a row. A row for an allowed read lists the pages returned, never their text. The service's login cannot write an "allowed" row by any other route, and cannot write any row without a bound session except the fixed "token refused" row. A request id that cannot be stored exactly as sent is refused. Each row carries a hash of the row before it; `GET /admin/audit_verify` walks the chain.
11. **New (RV-02).** A global page written by an agent, or by a person who does not control the holding organization, is stored but is read only inside that organization until a person who controls it approves. A person who controls it publishes directly.
12. **New (V-000 section 6).** A sub-organization can offer a report of at most 2,000 characters to the organization above. A person who controls the sub-organization must approve it. This is the only way text leaves a venture whose parent reads `none`.
13. **New.** A token that stands for a person works only while that person belongs to the token's organization.

## Interfaces

**MCP over HTTP**, `POST /mcp`, JSON-RPC 2.0, header `Authorization: Bearer <token>` and no other form (RV-17). Tools:

| Tool | Arguments | Returns |
| --- | --- | --- |
| `brain_whoami` | none | `{org, kind, actor, person}` |
| `brain_list` | `source_type?`, `kind?`, `limit?` | `{count, pages: [{id, org, title, kind, source_type, path}]}` |
| `brain_search` | `query`, `source_type?`, `limit?` | `{count, pages: [{id, org, title, kind, source_type, path, snippet}]}` |
| `brain_get` | `id` or `path`, `org?` | `{page, other_orgs?}`; `other_orgs` lists other readable organizations holding the same path |
| `brain_write` | `title`, `body`, `kind?`, `sensitivity?`, `visibility?` | `{id}`, plus `status: "pending_approval"` for a global page that waits |
| `publish_briefing` | `content`, `to?` | `{briefing_id, status: "pending", to}`; personal space only |
| `push_to_parent` | `content` | `{push_id, status: "pending", to}`; sub-organization only |
| `pending_approvals` | none | `{pushes: [...], pages: [...]}` with their text; a person's token only |
| `approve_push` | `push_id`, `decision?` | `{push_id, status, page_id}`; a person's token only |
| `approve_page` | `page_id`, `decision?` | `{page_id, status}`; a person's token only |

Every tool also accepts `request_id` (at most 100 characters, no control characters), which is copied into the log. Errors are tool results with `isError: true` and `{error: <code>}`: `not_found`, `forbidden`, `invalid_arguments`, `disabled`. A push or page the caller may not decide gives `not_found`, the same as one that does not exist.

**Admin over HTTP**, header `Authorization: Bearer <admin token>`. In the spike this stands in for the operator's console. Every route except the two that read the log writes a log row with actor `operator`.

| Route | Body or query | Purpose |
| --- | --- | --- |
| `POST /admin/reset` | a fixture: `settings`, `orgs`, `people`, `memberships`, `principals`, `pages` | Wipe and load made-up data. A personal space with no person is refused. |
| `POST /admin/settings` | `personal_enabled`, `briefing_enabled`, `holding_reads` for the deployment; with `org`, `holding_reads` (`all`, `summaries`, `none`, `default`) for a sub-organization or `personal_enabled`, `briefing_enabled` for the person whose personal space it is | Flip a switch. An unknown key or value is refused and nothing changes. |
| `POST /admin/approve_briefing` | `briefing_id`, `approver`, `decision?` | The operator records a named person's decision on a push. The person must exist and have the authority. |
| `POST /admin/approve_page` | `page_id`, `approver`, `decision?` | The same for a pending global page. |
| `GET /admin/pushes` | `status?` | Pushes with their text. |
| `POST /admin/codebase_sync` | `org`, `upserts`, `deletes` | The mapper's write path; pages are stored as `codebase`. |
| `GET /admin/audit` | `since_id?`, `page_id?` | Read the log; `page_id` answers "who was handed this page". Not itself logged. |
| `GET /admin/audit_verify` | none | `{ok, rows_checked, first_bad_id}`. Not itself logged. |
| `GET /admin/pages_digest` | `org`, `source_type?` | `[{path, content_sha}]`. |

The two approval routes exist so that R-02's tests still run. In a product a person approves with their own sign-in (the `approve_push` and `approve_page` tools model that), and an operator override like these routes would need its own decision.

**Database**, schema `brain`. Tables: `settings`, `orgs`, `people`, `memberships`, `principals`, `sessions`, `pages`, `pushes`, `audit`. The login `brain_app` may execute `begin_session`, the ten `t_*` tool functions, `audit_denied`, `audit_rpc` and `audit_auth_failure`. Functions whose names end in `_` are internal and are not granted to it.

## What this contract does not promise

- Text an agent has read stays readable in any copy the agent wrote down. Switching briefings off hides the page the service delivered; it cannot find a copy. The log shows who was handed the page.
- The log is append-only against the service's two logins and tamper-evident against a superuser. It is not tamper-proof: a superuser can still delete the whole log, and then the chain shows only that rows are missing from the start.
- Someone who holds the database password and a valid token can read and then roll back, which leaves no row. A token alone cannot.
- The database login can ask PostgreSQL how large the pages table is.
- A parent reading `summaries` can tell by timing (between 1 and 2 microseconds) whether an id belongs to some page of its own venture.
- Nothing here covers what an agent does inside Paperclip without calling this service, or what Paperclip stores (RV-01, RV-04, RV-08, RV-10). Those need Paperclip running and are not part of this pass.
