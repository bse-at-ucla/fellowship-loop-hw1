# Day 1 Homework: Build the Harness — Layer 5

**Needs:** Python 3.9+, nothing to install. **Edit and submit:** `harness.py`.

Build the boundary that executes a model's tool requests, enforces permissions,
and returns results or errors. The model and agent driver are provided; your
work is limited to the **Layer 5 harness** in the lecture diagram.

## The task

A tiny project in `repo/` has a failing test. A scripted model will request tools
to fix it. Some of its behaviors are untrustworthy: it may claim success without
fixing anything or change the tests to hide the problem.

Implement these two functions in `harness.py`:

| Function | Responsibility | Points |
|---|---|---|
| `execute_tool` | Handle tool requests, enforce permission rules, and report results or errors | 60 |
| `verify` | Check that the original tests pass without being modified | 40 |

Start with `execute_tool`, then work on `verify`. Their docstrings define the
inputs, outputs, and required behavior. Read `tools.py` to understand the available
tools. Work out how to connect them to meet those requirements.

The supplied `agent.py` handles model calls, messages, context, retries, and
stopping. You do not need to implement those behaviors or fix `repo/` yourself.

## Check your progress

From this folder, run:

```sh
python3 grade.py
```

Use `python3 grade.py -v` for error details. The starter scores **0/100**;
“not implemented” is expected. Partial credit is available as you complete the
requirements. All nine checks grade the two functions in `harness.py`, for a
total of **100 points**.

## Files and rules

- **`harness.py`:** your two functions and reflection. Keep the signatures and permission sets.
- **`tools.py`:** supplied tool implementations.
- **`fake_model.py`:** scripted model behaviors; no API keys or real AI calls needed.
- **`agent.py`:** supplied agent driver and context helpers.
- **`grade.py`:** grader.

Use only the Python standard library. Leave the supplied files and `repo/` unchanged.

## Submit

Add a 3–5 sentence comment in `harness.py`: which scripted behavior was hardest
to handle, which harness check (or supplied driver behavior) handled it, and why
trusting the model's claim alone would be insufficient.

**DM Rizwaan on Discord your `harness.py` as a file upload (NOT text code block!!) and a screenshot of your final `python3 grade.py` output.**
