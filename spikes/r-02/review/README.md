# REV-01 review: tests and measurements against the R-02 permission service

Written 2026-11-17 by the review session that attacked R-01 and R-02. The findings are in `docs/reviews/REV-01_R-01_AND_R-02.md`; IDs such as RV-06 point there. Nothing under `../service`, `../tests` or `../results` was changed. All data is made up and the tokens are the fixture's test values.

## What is here

| File | What it is |
| --- | --- |
| `test_rev01_attacks.py` | 24 tests on criteria 1 to 4, against the service directly. Each asserts what `../service/CONTRACT.md` or V-000 requires. A pass is an attack the service held. A fail is a defect, named in the test's first line. |
| `test_rev01_second_person.py` | 13 tests for V-000 F-31 and the service-level criteria of the shared-venture spike (P-000, note on R-03): a friend with one human token, then a second personal space, then a second holding organization. |
| `measure.py` | Three measurements that print and assert nothing: `timing` (RV-06), `scale` (RV-05), `matrix` (who reads what with two people). |
| `mutation_sweep.py` | 19 deliberate breaks of `../service/schema.sql`, one at a time, each run against the 35 existing tests (RV-11). |
| `fix-sketch-read-rule.sql` | A sketch of the smallest fix for RV-05. Not applied to the service. Its header says what it does and does not fix. |
| `common.py`, `run.sh` | Helpers, and one command that runs all of the above on a local PostgreSQL. |
| `results/` | Raw output of the run of 2026-11-17. |

## Results of 2026-11-17

PostgreSQL 16.15, Node 22.23.4, Python 3.13.18, in the review session's sandbox. R-02 ran on PostgreSQL 17; that difference was not tested.

| Run | Result | Raw output |
| --- | --- | --- |
| The 35 existing tests | 35 pass | `results/existing-35-tests.txt` |
| Attack tests | 24 run: 9 pass (attacks held), 15 fail (defects) | `results/review-attacks.txt` |
| Second-person tests | 13 run: 5 pass, 8 fail | `results/review-second-person.txt`, `results/second-person-matrix.txt` |
| Timing | A page that exists in another organization answers 513 to 521 microseconds slower than a missing page, with the same error text. Earlier runs gave 0.4 to 0.57 ms. | `results/timing.txt` |
| Scale | One caller's list of its own 4 pages: 4.9 ms with nothing else in the database, 2,853 ms after 10,000 pages are added to another organization | `results/scale.txt` |
| Mutation sweep | 19 rules weakened one at a time: the 35 tests notice 9 and miss 10 | `results/mutation-sweep.txt` |
| Read-rule sketch | Fixes scale (8 ms at 10,000 pages). Does not fix timing (0.36 ms remains). The 35 tests still pass. | `results/fix-sketch.txt` |

The failing tests are left failing on purpose. They are the acceptance tests for the fixes.

## How to run

```
SUPER_DSN=postgres://postgres:<password>@127.0.0.1:5432/brain ./run.sh
```

It needs a throwaway database you may wipe (it loads `../service/schema.sql`, which drops and recreates the schema `brain`), `psql`, Node 22 or newer and Python 3. It copies the service's two files to a temporary directory, installs the service's one dependency there (`pg` 8.23.1), starts the service, runs everything and writes `results/`. The whole run takes about two minutes.

Paperclip is not involved in anything here and was not run.

## What these tests cannot show

- Anything about Paperclip: whether an agent can act as the board, read another company's stored token, or approve its own request (RV-01). That needs Paperclip running, which this review was not allowed to do.
- Behaviour under PostgreSQL 17, under real load, or with a network between caller and service. The timing figures are from one machine with the caller on the same host.
- Whether the sketch is the right design. It shows the size of the fix, not its final form.
