import json, urllib.request, urllib.error
url = "http://127.0.0.1:8000/api/health"
try:
    with urllib.request.urlopen(url, timeout=5) as response:
        print(json.dumps(json.loads(response.read()), indent=2, ensure_ascii=False))
except (OSError, urllib.error.URLError) as exc:
    raise SystemExit(f"NOVA API inaccessible à {url}: {exc}")
