# REV-01 fix pass: the permission service, fixed

The review `docs/reviews/REV-01_R-01_AND_R-02.md` left 23 failing tests against the R-02 permission service. This folder holds a fixed copy of that service and the tests that show it. The report is `docs/reviews/REV-01_FIX_PASS.md`; this file says what is here and how to run it.

Nothing under `spikes/r-02/` was changed. The R-02 service, its tests, the review's tests and all their results stay as they were, as evidence of what was found.

Paperclip was not installed or run. Made-up data only. No model was called.

## What is here

| Path | What it is |
| --- | --- |
| `service/schema.sql` | The database: tables, the functions that are the only way in, the log. Rewritten. |
| `service/server.mjs` | The service: one dependency (`pg` 8.23.1). Holds no permission logic. |
| `service/CONTRACT.md` | The rules the service must keep, with each change marked against the finding that caused it. |
| `tests/test_criteria_1_3.py` | R-02's 35 tests, copied. 6 changed. |
| `tests/test_rev01_attacks.py` | The review's 24 attack tests, copied. 6 changed, 3 added. |
| `tests/test_rev01_second_person.py` | The review's 13 second-person tests, copied. 1 changed. |
| `tests/test_fix_new_rules.py` | 29 new tests for the rules this pass added. |
| `CHANGED_ASSERTIONS.md` | Every changed assertion, one by one, with the reason. |
| `measure.py` | The review's scale and timing measurements, repeated, plus one inside the database. |
| `mutation_sweep.py` | 70 deliberate breaks of the schema and the server, each run against all 104 tests. |
| `run.sh` | One command for all of the above. |
| `results/` | Raw output of the run that the report quotes. |

## Run it

```
SUPER_DSN=postgres://postgres:<password>@127.0.0.1:5432/<throwaway database>  ./run.sh [results-directory]
```

Needs a local PostgreSQL where you may create roles (the review and this pass used 16.15), `psql`, Node 22 or newer and Python 3. The database is wiped. About 5 minutes without the mutation sweep (`SKIP_SWEEP=1`), about 40 with it.

`results/mutation-sweep-run-1.txt`, `-run-2.txt` and `-run-3-stopped.txt` are the sweep's three earlier runs, kept because each found a gap in the tests; the report's section 5 says what.

A line such as `OK (expected failures=2)` is a pass. The expected failures are the known limits: tests that assert a rule one would want, kept failing so the gap shows in every run.

## How the fixed service differs, in one paragraph

In R-02 the service's database login could select from the pages table and row-level security filtered the rows. That is why a caller could time a forbidden page against a missing one, read a query plan, and slow down as other organizations grew. Here the login cannot touch any table. It can call fourteen functions. Each tool function reads the caller's organization from a session that only a token can bind, works out nothing lazily, looks only at rows of organizations the caller may read, and writes its own log row before it returns. People and memberships are data, so "who may read" and "who may approve" are answered per person. The rest is in `service/CONTRACT.md`.

Two things in `schema.sql` look odd and are deliberate. Each has a comment, a test that fails without it, and a mutant in the sweep:

- `offset 0` in the list and search functions is a fence. It makes the database apply the read rule before it tries the search text on a row. Without it, a search by one venture took 3.5 ms before and 216 ms after another venture stored 24 million characters, because the text was being tried against those pages first.
- `set enable_seqscan = off` on the list and search functions makes them walk the index from the caller's own organizations. Without it a list by one venture went from 3.9 ms to 18.9 ms when another gained 20,000 pages.

Both were found while building this pass, not by the review. Whether either problem shows depends on which of its two kinds of plan PostgreSQL is using, so the tests for them force the unfavourable kind.
