from winston_shared.auth_dataclass import Config
from dotenv import load_dotenv
import os

load_dotenv('/home/cheecho/workspace/github.com/cheecho/winston_shared/.env')

cheehco = Config(
    name="cheehco",
    client_id=os.getenv("TWITCH_CLIENT_ID"),
    client_secret=os.getenv("TWITCH_SECRET"),
    auth_uri="https://id.twitch.tv/oauth2/authorize",
    token_uri="https://id.twitch.tv/oauth2/token",
    scopes=['user:write:chat', 'user:bot', 'channel:bot', 'user:read:chat', 'moderator:read:followers', 'moderator:manage:banned_users', 'moderator:read:suspicious_users'],
    api_uri="https://api.twitch.tv/helix/",
    channel=os.getenv("CHEEHCO_ID"),
    channel_name="cheehco",
    bot=os.getenv("BOT_ID"),
    discord=os.getenv("CHEEHCO_DISCORD"),
    token_file="cheehco_twitch_token.json",
    redirect_uri=os.getenv("TWITCH_REDIRECT"),
    content_type={'Content-Type': "application/x-www-form-urlencoded"},
    spotify_client_id=os.getenv("CHEEHCO_SPOTIFY_CLIENT_ID"),
    spotify_client_secret=os.getenv("CHEEHCO_SPOTIFY_SECRET"),
    spotify_redirect_uri=os.getenv("SPOTIFY_REDIRECT"),
)