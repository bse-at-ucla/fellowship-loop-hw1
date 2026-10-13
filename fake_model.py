"""A scripted stand-in for an LLM. DO NOT EDIT.

Same interface as a real model API: model(messages) -> ONE assistant message.
It decides what to do next by looking only at the LAST message you send it, so
it is deterministic and the autograder can replay any scenario.
"""


class ProtocolError(Exception):
    """Raised when the harness breaks the message protocol."""


def _blocks(msg):
    c = msg["content"]
    return c if isinstance(c, list) else [{"type": "text", "text": c}]


class FakeModel:
    # personas: honest | liar | cheater | looper | dangerous
    def __init__(self, persona="honest"):
        self.persona = persona
        self.calls = 0
        self._ids = 0

    # ---- message builders
    def _text(self, text):
        return {"role": "assistant", "content": [{"type": "text", "text": text}]}

    def _tool(self, name, **tool_input):
        self._ids += 1
        return {"role": "assistant", "content": [
            {"type": "tool_use", "id": f"toolu_{self._ids:03d}", "name": name, "input": tool_input}]}

    # ---- the "thinking"
    def __call__(self, messages):
        self.calls += 1
        if self.calls > 40:
            raise ProtocolError("the model was called more than 40 times: your loop is not stopping")
        last = messages[-1]
        if last["role"] != "user":
            raise ProtocolError("the last message sent to the model must have role 'user'")
        results = [b for b in _blocks(last) if b.get("type") == "tool_result"]
        if results:
            return self._after_tool(messages, results[0])
        text = " ".join(b.get("text", "") for b in _blocks(last)).lower()
        if "verification failed" in text:
            return self._after_feedback()
        return self._first_move()

    def _first_move(self):
        p = self.persona
        if p == "liar":
            return self._text("Fixed! All tests pass.")
        if p == "looper":
            return self._tool("read_file", path="auth.py")
        if p == "dangerous":
            return self._tool("run_bash", command="touch PWNED")
        return self._tool("run_tests")

    def _after_feedback(self):
        if self.persona == "liar":
            return self._tool("run_tests")
        return self._text("Done.")

    def _after_tool(self, messages, res):
        prev = messages[-2] if len(messages) >= 2 else None
        uses = []
        if prev and prev["role"] == "assistant":
            uses = [b for b in _blocks(prev) if b.get("type") == "tool_use"]
        if not uses or uses[0]["id"] != res.get("tool_use_id"):
            raise ProtocolError(
                f"tool_result has tool_use_id={res.get('tool_use_id')!r} but the tool_use "
                f"right before it has id={uses[0]['id'] if uses else None!r}")
        used = uses[0]["name"]
        text = str(res.get("content", ""))
        err = bool(res.get("is_error"))
        p = self.persona

        if p == "looper":
            return self._tool("read_file", path="auth.py")
        if p == "dangerous" and used == "run_bash":
            return self._tool("run_tests")
        if p == "cheater":
            if used == "run_tests":
                if "FAILED" in text:
                    return self._tool("edit_file", path="tests/test_auth.py",
                                      old_text="self.assertTrue(is_expired(100, 100))",
                                      new_text="self.assertFalse(is_expired(100, 100))")
                return self._text("Done. All tests pass.")
            if used == "edit_file":
                return self._text("I wasn't allowed to edit that.") if err else self._tool("run_tests")

        # the honest flow (also used by liar and dangerous once they get going)
        if used == "run_tests":
            if "FAILED" in text:
                return self._tool("read_file", path="auth.py")
            return self._text("Done. All tests pass.")
        if used == "read_file":
            return self._tool("edit_file", path="auth.py", old_text="exp < now", new_text="exp <= now")
        if used == "edit_file":
            return self._text("The edit was denied, so I can't fix this.") if err else self._tool("run_tests")
        return self._text("Done.")
