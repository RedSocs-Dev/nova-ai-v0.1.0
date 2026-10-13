from dataclasses import dataclass
import httpx
from .config import get_settings

@dataclass
class ModelReply:
    text: str
    model: str
    provider: str

class ProviderError(RuntimeError):
    pass

async def generate(messages: list[dict], model: str | None = None,
                   temperature: float = 0.7, max_tokens: int = 1024) -> ModelReply:
    """Call a real Ollama API or an OpenAI-compatible chat-completions endpoint."""
    cfg = get_settings()
    chosen_model = model or cfg.model
    base = cfg.base_url.rstrip("/")
    headers = {}
    if cfg.provider == "ollama":
        url = f"{base}/api/chat"
        payload = {"model": chosen_model, "messages": messages, "stream": False,
                   "options": {"temperature": temperature, "num_predict": max_tokens}}
    elif cfg.provider == "openai_compatible":
        url = f"{base}/v1/chat/completions"
        payload = {"model": chosen_model, "messages": messages, "temperature": temperature,
                   "max_tokens": max_tokens, "stream": False}
        if cfg.api_key:
            headers["Authorization"] = f"Bearer {cfg.api_key}"
    else:
        raise ProviderError(f"Fournisseur non pris en charge : {cfg.provider}")
    try:
        async with httpx.AsyncClient(timeout=cfg.timeout_seconds) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        if cfg.provider == "ollama":
            text = data.get("message", {}).get("content", "")
        else:
            text = data["choices"][0]["message"]["content"]
        if not isinstance(text, str) or not text.strip():
            raise ProviderError("Le fournisseur a renvoyé une réponse vide.")
        return ModelReply(text=text, model=chosen_model, provider=cfg.provider)
    except ProviderError:
        raise
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc:
        raise ProviderError(f"Échec de l'appel au modèle ({type(exc).__name__}). Vérifiez le fournisseur et sa disponibilité.") from exc

async def health() -> dict:
    cfg = get_settings()
    try:
        async with httpx.AsyncClient(timeout=min(cfg.timeout_seconds, 4)) as client:
            if cfg.provider == "ollama":
                r = await client.get(cfg.base_url.rstrip("/") + "/api/tags")
            else:
                r = await client.get(cfg.base_url.rstrip("/") + "/v1/models",
                                     headers={"Authorization": f"Bearer {cfg.api_key}"} if cfg.api_key else {})
            r.raise_for_status()
        return {"configured": True, "reachable": True, "provider": cfg.provider, "model": cfg.model}
    except Exception as exc:
        return {"configured": True, "reachable": False, "provider": cfg.provider, "model": cfg.model,
                "error_type": type(exc).__name__}
