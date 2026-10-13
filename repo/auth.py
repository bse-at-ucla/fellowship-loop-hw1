"""Token expiry helpers.

Tokens issued by the auth service carry an `exp` field: the Unix timestamp
(in whole seconds) at which the token stops being valid. Clients call
`is_expired` before every request so that they can refresh a token instead of
sending one the server is going to reject.

Boundary behaviour matters here. The server treats a token as invalid starting
at the exact second named by `exp`: a request that arrives at that second is
rejected, so the client must treat that second as already expired. Getting this
wrong produces the worst kind of bug: requests that fail only once in a while,
at exactly the wrong moment, and that nobody can reproduce on demand.

All timestamps are integers in seconds since 1970-01-01 UTC. Do not pass
milliseconds; convert first.
"""


def is_expired(exp, now):
    """Return True if a token with expiry `exp` is expired at time `now`."""
    return exp < now
