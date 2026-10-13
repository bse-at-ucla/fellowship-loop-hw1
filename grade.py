"""Autograder. Run: python grade.py   (add -v to see failure details)"""
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True

import tools  # noqa: E402

try:
    import harness  # noqa: E402
except Exception:
    print("Could not import harness.py:")
    traceback.print_exc()
    sys.exit(1)

VERBOSE = "-v" in sys.argv
RESULTS = []  # (part, name, earned, possible, note)


def fresh_repo():
    d = Path(tempfile.mkdtemp(prefix="hw_")) / "repo"
    shutil.copytree(HERE / "repo", d, ignore=shutil.ignore_patterns("__pycache__"))
    return d


def fix(repo):
    p = Path(repo) / "auth.py"
    p.write_text(p.read_text().replace("exp < now", "exp <= now"))


def check(part, name, points):
    def deco(fn):
        note = ""
        try:
            fn()
            earned = points
        except NotImplementedError:
            earned, note = 0, "not implemented yet"
        except AssertionError as e:
            earned, note = 0, str(e) or "check failed"
        except Exception as e:  # noqa: BLE001
            earned, note = 0, f"{type(e).__name__}: {e}"
            if VERBOSE:
                note += "\n" + traceback.format_exc()
        RESULTS.append((part, name, earned, points, note))
        return fn
    return deco


def never(*a):
    raise AssertionError("approve() was called but should not have been")


# ───────────────────────── Step 1 · tool boundary (60) ─────────────────────────
P1 = "Step 1 · tool boundary (60 pts)"


@check(P1, "execute_tool: read_file returns file text", 10)
def _():
    out, err = harness.execute_tool(fresh_repo(), "read_file", {"path": "auth.py"}, never)
    assert err is False and "def is_expired" in out, f"got {(out[:60], err)!r}"


@check(P1, "execute_tool: run_tests returns the test output", 10)
def _():
    out, err = harness.execute_tool(fresh_repo(), "run_tests", {}, never)
    assert err is False and "FAILED" in out, f"expected the unittest output, got {out[:80]!r}"


@check(P1, "execute_tool: unknown tool -> error, no crash", 10)
def _():
    out, err = harness.execute_tool(fresh_repo(), "format_disk", {}, lambda n, i: True)
    assert err is True and isinstance(out, str)


@check(P1, "execute_tool: a tool that raises -> error, no crash", 10)
def _():
    inp = {"path": "auth.py", "old_text": "NOT THERE", "new_text": "x"}
    out, err = harness.execute_tool(fresh_repo(), "edit_file", inp, lambda n, i: True)
    assert err is True and out.startswith("error"), f"got {(out[:60], err)!r}"


@check(P1, "execute_tool: read_file/run_tests never ask for approval", 10)
def _():
    r = fresh_repo()
    harness.execute_tool(r, "read_file", {"path": "auth.py"}, never)
    harness.execute_tool(r, "run_tests", {}, never)


@check(P1, "execute_tool: denied edit is NOT run, says so", 10)
def _():
    r = fresh_repo()
    seen = []
    inp = {"path": "auth.py", "old_text": "exp < now", "new_text": "exp <= now"}
    out, err = harness.execute_tool(r, "edit_file", inp, lambda n, i: seen.append((n, i)) or False)
    assert seen == [("edit_file", inp)], f"approve should be called once with (name, input), saw {seen!r}"
    assert err is True and out == "denied: edit_file was not approved", f"got {out!r}"
    assert "exp < now" in (r / "auth.py").read_text(), "the file was edited even though approval was denied"


# ───────────────────────── Step 2 · verification (40) ─────────────────────────
P2 = "Step 2 · fixed verification policy (40 pts)"


@check(P2, "verify: failing tests -> (False, output)", 12)
def _():
    r = fresh_repo()
    ok, out = harness.verify(r, tools.hash_dir(r / "tests"))
    assert ok is False and "FAILED" in out, f"got {(ok, out[:60])!r}"


@check(P2, "verify: fixed code, untouched tests -> (True, ...)", 12)
def _():
    r = fresh_repo()
    h = tools.hash_dir(r / "tests")
    fix(r)
    ok, out = harness.verify(r, h)
    assert ok is True, f"got {(ok, out[:80])!r}"


@check(P2, "verify: tests pass but tests were edited -> rejected", 16)
def _():
    r = fresh_repo()
    h = tools.hash_dir(r / "tests")
    t = r / "tests" / "test_auth.py"
    t.write_text(t.read_text().replace("assertTrue(is_expired(100, 100))", "assertFalse(is_expired(100, 100))"))
    ok, out = harness.verify(r, h)  # tests now pass against the buggy code
    assert ok is False, "you accepted a run where the tests were rewritten to pass"
    assert "test" in out.lower(), "output should tell the model the tests were modified"


# ───────────────────────── report ─────────────────────────
total = sum(r[2] for r in RESULTS)
possible = sum(r[3] for r in RESULTS)
part = None
for p, name, got, pts, note in RESULTS:
    if p != part:
        part = p
        sub = sum(r[2] for r in RESULTS if r[0] == p)
        sub_max = sum(r[3] for r in RESULTS if r[0] == p)
        print(f"\n{p}  [{sub}/{sub_max}]")
    print(f"  {'✓' if not note else '✗'} {got:>2}/{pts:<2} {name}")
    if note:
        print("        → " + note.replace("\n", "\n          "))
print(f"\nSCORE: {total}/{possible}")
