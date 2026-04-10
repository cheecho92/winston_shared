from dataclasses import dataclass

'''
Config dataclass used by both winston_bot and flask_server via winston_shared.
Bot instances use fields (channel, bot, api_uri etc.)
Flask server uses OAuth fields (auth_uri, token_uri, redirect_uri etc.)
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
    spotify_client_id: str | None = None
    spotify_client_secret: str | None = None
    spotify_api_uri: str | None = None
    spotify_redirect_uri: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    headers: dict | None = None