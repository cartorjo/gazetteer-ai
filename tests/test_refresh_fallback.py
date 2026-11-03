"""Exercise the auto-detect branch of refresh_stars.py: /repos answers 403 (not a rate limit),
so every entry must be refreshed through the search API in the same run. Hits the live API
for search; run with: uv run python tests/test_refresh_fallback.py"""

import contextlib
import io
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import _common  # noqa: E402
import refresh_stars  # noqa: E402

real_get = _common.github_get


def fake_get(session, url, params=None, retries=6):
    if "/repos/" in url:
        resp = requests.Response()
        resp.status_code = 403
        resp._content = b'{"message":"GitHub access to this repository is not enabled for this session."}'
        resp.headers["X-RateLimit-Remaining"] = "4999"
        return resp
    return real_get(session, url, params=params, retries=retries)


refresh_stars.github_get = fake_get
refresh_stars.save_projects = lambda projects: None  # do not touch data/projects.yaml
sys.argv = ["refresh_stars.py", "--no-snapshot"]
projects = _common.load_projects()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = refresh_stars.main()
out = buf.getvalue()
print(out.strip().splitlines()[-1])
assert rc == 0, out
assert f"search route: {len(projects)} entries looked up, {len(projects)} refreshed" in out, out
print("ok")
