from dataclasses import dataclass

'''
Config dataclass used by both winston_bot and flask_server via winston_shared.
Bot instances use fields (channel, bot, api_uri etc.)
Flask server uses OAuth fields (auth_uri, token_uri, redirect_uri etc.)
'''

@dataclass
class Config:
    name: str
    client_id: str
    client_secret: str
    auth_uri: str
    token_uri: str
    scopes: list
    token_file: str
    redirect_uri: str
    content_type: dict
    api_uri: str | None = None
    channel: str | None = None
    channel_name: str | None = None
    bot: str | None = None
    discord: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    headers: dict | None = None