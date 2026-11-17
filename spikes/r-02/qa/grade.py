"""Grade one answer against questions.json. Standard library only. Used by the QA harness and testable on its own."""
import json, pathlib, re

QUESTIONS = {q["id"]: q for q in json.loads((pathlib.Path(__file__).parent / "questions.json").read_text())["questions"]}

def answer_line(text):
    lines = [l for l in (text or "").splitlines() if l.strip().upper().startswith("ANSWER:")]
    return lines[-1].split(":", 1)[1].strip()[:400] if lines else ""

def norm_item(s):
    s = s.strip().lower().strip("`'\"*. ")
    s = re.sub(r"^@toveli/", "", s)
    s = re.sub(r"^(apps|packages)/", "", s)
    return s

def grade(qid, text):
    """Returns (score between 0 and 1, correct bool, detail)."""
    q, ans = QUESTIONS[qid], answer_line(text)
    if not ans:
        return 0.0, False, "no ANSWER line"
    if q["type"] == "set":
        got = {norm_item(x) for x in re.split(r"[,;]| and ", ans) if norm_item(x)}
        want = set(q["key"])
        inter = len(got & want)
        score = inter / len(got | want) if got | want else 0.0
        return score, got == want, f"got {sorted(got)} want {sorted(want)}"
    hits = [any(re.search(alt, ans, re.I) for alt in group) for group in q["key"]]
    return sum(hits) / len(hits), all(hits), f"groups matched {sum(hits)}/{len(hits)}"

if __name__ == "__main__":
    # self-check: a reference answer for each question must grade as correct, and a wrong one must not
    ref = {"Q01":"ANSWER: pnpm 11.28.2, pinned in package.json (packageManager)","Q06":"ANSWER: No. Only .devcontainer/Dockerfile exists.",
           "Q07":"ANSWER: adapters, contracts, db, domain","Q09":"ANSWER: @toveli/contracts, @toveli/domain, mobile","Q18":"ANSWER: 426"}
    for qid, a in ref.items():
        assert grade(qid, a)[1], (qid, grade(qid, a))
    assert not grade("Q07", "ANSWER: adapters, contracts, db, domain, worker")[1]
    assert not grade("Q06", "ANSWER: Yes, the .devcontainer Dockerfile deploys it")[1]
    assert not grade("Q18", "The status is 426")[1]
    print("grader self-check passed")
