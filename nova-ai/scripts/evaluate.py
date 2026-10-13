"""Tiny smoke evaluator: checks HTTP API availability, not model quality."""
import json, urllib.request
BASE = "http://127.0.0.1:8000"
def get(path):
    with urllib.request.urlopen(BASE + path, timeout=10) as r: return json.loads(r.read())
health = get("/api/health")
settings = get("/api/settings")
assert health.get("status") == "ok", health
assert settings.get("name"), settings
print(json.dumps({"smoke_test":"passed","health":health,"settings":settings},ensure_ascii=False,indent=2))
