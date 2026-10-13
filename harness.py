"""Day 1 homework: build the Layer 5 harness.

Implement execute_tool() and verify(), replacing each NotImplementedError.
Keep the function signatures and permission sets. The supplied agent.py handles
model calls, messages, retries, and stopping.

Run `python3 grade.py` to check your work. See README.md for the assignment.
"""
from pathlib import Path
from typing import Callable, Union

import tools

AUTO_ALLOWED: set[str] = {"read_file", "run_tests"}
NEEDS_APPROVAL: set[str] = {"edit_file", "run_bash"}


def execute_tool(
    repo: Union[str, Path],
    name: str,
    tool_input: dict[str, str],
    approve: Callable[[str, dict[str, str]], bool],
) -> tuple[str, bool]:
    """Execute one requested tool. Return (content: str, is_error: bool).

    repo is the project folder; name identifies a tool in tools.py; tool_input
    contains its arguments. approve(name, tool_input) is a supplied callback
    that returns whether a request is approved.

    Requirements:
    - AUTO_ALLOWED tools run without approval. NEEDS_APPROVAL tools require it.
    - Unknown or denied tools must not run.
    - A denied request returns ("denied: <name> was not approved", True).
    - Unknown tools return an explanatory error string and True.
    - Exceptions from approval or execution return ("error: <message>", True).
    - Successful calls return the tool's output and False. For run_tests, use
      its output text; failing tests do not count as a tool execution error.
    """
    # Suggested approach:
    # 1. Decide whether the request is recognized and permitted.
    # 2. Run the requested tool and adapt its result to this function's contract.
    # 3. Make sure denials and exceptions produce useful feedback.
    # Hint: inspect tools.py; not every tool returns the same kind of result.
    raise NotImplementedError


def verify(
    repo: Union[str, Path], tests_hash_at_start: str
) -> tuple[bool, str]:
    """Check the supplied acceptance policy. Return (ok: bool, output: str).

    repo is the project folder. tests_hash_at_start is the fingerprint of its
    original tests directory, supplied by the driver.

    Accept only if freshly run tests pass AND the test files are unchanged.
    Use tools.run_tests and tools.hash_dir to establish those facts. Return
    the test output when files are unchanged, or an explanation of the test
    modification when they differ. The driver handles retrying and stopping.
    """
    # Suggested approach:
    # Gather evidence about both test results and test integrity, then decide
    # whether the acceptance policy is satisfied and what feedback to return.
    # Hint: passing tests alone are not enough if those tests were changed.
    raise NotImplementedError


# Reflection: Write 3–5 sentences about the hardest scripted behavior to handle,
# which harness check (or supplied driver behavior) handled it, and why trusting
# the model's claim alone would be insufficient.
