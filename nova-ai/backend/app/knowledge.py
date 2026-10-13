"""Small, transparent local document store; lexical retrieval baseline, not semantic embeddings."""
import hashlib, re
from datetime import datetime, timezone
from .db import db

ALLOWED = {".txt", ".md", ".csv", ".json", ".html"}

def utcnow():
    return datetime.now(timezone.utc).isoformat()

def ingest(filename: str, raw: bytes, max_bytes: int = 2_000_000) -> dict:
    from pathlib import PurePath
    if len(raw) > max_bytes:
        raise ValueError("Fichier trop volumineux (limite : 2 Mo).")
    ext = PurePath(filename).suffix.lower()
    if ext not in ALLOWED:
        raise ValueError("Format non pris en charge dans cette version. Utilisez TXT, MD, CSV, JSON ou HTML.")
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("Le fichier doit être encodé en UTF-8.") from exc
    if not content.strip():
        raise ValueError("Le document est vide.")
    digest = hashlib.sha256(raw).hexdigest()
    with db() as conn:
        existing = conn.execute("SELECT id FROM documents WHERE sha256=?", (digest,)).fetchone()
        if existing:
            return {"id": existing["id"], "filename": filename, "duplicate": True}
        cur = conn.execute("INSERT INTO documents(filename,content,sha256,created_at) VALUES(?,?,?,?)",
                           (filename[:255], content, digest, utcnow()))
        return {"id": cur.lastrowid, "filename": filename[:255], "duplicate": False}

def retrieve(query: str, limit: int = 4) -> list[dict]:
    terms = {t.lower() for t in re.findall(r"\w{3,}", query)}
    if not terms:
        return []
    with db() as conn:
        rows = conn.execute("SELECT id,filename,content FROM documents").fetchall()
    ranked = []
    for row in rows:
        chunks = [x.strip() for x in re.split(r"\n\s*\n", row["content"]) if x.strip()]
        for i, chunk in enumerate(chunks):
            words = {t.lower() for t in re.findall(r"\w{3,}", chunk)}
            score = len(terms & words)
            if score:
                ranked.append({"document_id": row["id"], "filename": row["filename"],
                               "text": chunk[:3000], "score": score, "chunk": i})
    return sorted(ranked, key=lambda x: x["score"], reverse=True)[:limit]
