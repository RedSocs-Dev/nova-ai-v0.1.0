from pydantic import BaseModel, Field, ConfigDict

class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str = Field(min_length=1, max_length=20000)
    model: str | None = Field(default=None, max_length=120)
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1024, ge=1, le=8192)

class ConversationRename(BaseModel):
    title: str = Field(min_length=1, max_length=160)

class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

class SettingsView(BaseModel):
    name: str
    provider: str
    model: str
    base_url: str
    memory_enabled: bool
