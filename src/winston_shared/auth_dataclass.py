from dataclasses import dataclass

'''
Config dataclass used by both winston_bot and flask_server via winston_shared.
Each service (bot, broadcaster, spotify) gets its own Config object.
Not all fields are used by every config — unused fields default to None.
'''

@dataclass
class Config:
    name: str
    auth_uri: str
    token_uri: str
    token_file: str
    redirect_uri: str
    content_type: dict
    scopes: list | None = None
    client_id: str | None = None
    client_secret: str | None = None
    api_uri: str | None = None
    channel: str | None = None
    channel_name: str | None = None
    bot: str | None = None
    discord: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    headers: dict | None = None