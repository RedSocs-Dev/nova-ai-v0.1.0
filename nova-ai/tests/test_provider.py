import pytest
from app.providers import generate, ProviderError
from app.config import get_settings

@pytest.mark.asyncio
async def test_unknown_provider_fails_closed(monkeypatch):
    monkeypatch.setenv("NOVA_PROVIDER","unknown")
    get_settings.cache_clear()
    try:
        with pytest.raises(ProviderError):
            await generate([{"role":"user","content":"hello"}])
    finally:
        get_settings.cache_clear()
