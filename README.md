# winston_shared

Shared Python package used by the Winston Twitch bot. Contains the auth logic, config dataclasses, and token handling [`flask_server`](https://github.com/cheecho92/flask_server) and [`Winston_Bot`](https://github.com/cheecho92/Winston_Bot) use.

## What's in it

**`src/winston_shared/auth.py`** — Contains all logic for authentication. Builds authorization URLs, exchanges auth codes for tokens, handles token refresh on 401 responses, and reads/writes token JSON files.

**`configs/`** — Config dataclasses for Twitch and Spotify, holding client credentials, redirect URIs, and headers used across both services.

**`tokens/`** — Where access and refresh tokens are stored after a successful auth flow. Keyed by channel name for twitch. The spotify token will need to be manually edited, because I got lazy. (e.g. `<channel>_twitch.json`, `<manual_edit>_spotify.json`).

## Install

This is a local package. Install it into your other services with pip:

```bash
pip install -e /path/to/winston_shared
```


## Requirements

- Python >= 3.12
- `requests >= 2.33.1`

## Related

- [`flask_server`](https://github.com/cheecho92/flask_server) — OAuth server that uses this package to handle auth flows and save tokens
- [`Winston_Bot`](https://github.com/cheecho92/Winston_Bot) — the bot that handles the tokens generated and contains the chat moderation logic