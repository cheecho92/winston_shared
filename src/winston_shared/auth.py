import json
import requests
import os
from urllib.parse import urlencode


# Use the Config dataclass to create the auth and token links cleanly
def url_parser(config, state):
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": " ".join(config.scopes),
        "state": state,
    }
    return f"{config.auth_uri}?{urlencode(params)}"


# Read the token JSON file as dict
def load_tokens(config):
    token_dir = os.getenv('TOKEN_DIR')
    with open(os.path.join(token_dir, config.token_file), "r") as f:
        tokens = json.load(f)
    return tokens


# Save POST response to a JSON file
def save_tokens(name, request_response):
    token_dir = os.getenv('TOKEN_DIR')
    with open(os.path.join(token_dir, f"{name}_token.json"), "w") as f:
        json.dump(request_response, f, indent=4)


# Generate the headers based on config profile
def generate_headers(config):
    if config.name == "twitch":
        params = {
        'Authorization': f"Bearer {config.access_token}",
        'Client-Id': config.client_id,
        'Content-Type': 'application/json'
        }
    else:
        params = {
        'Authorization': f"Bearer {config.access_token}",
        'Content-Type': 'application/json'
        }
    
    return params


# Handles the initial token generation and refresh tokens
def handle_tokens(config, code=None):
    token_path = os.path.join(os.getenv('TOKEN_DIR'), config.token_file)
    if os.path.exists(token_path):
        tokens = load_tokens(config)
        params = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"]
        }
    else:
        params = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": config.redirect_uri,
        }

    encoded_params = urlencode(params)
    req = requests.post(config.token_uri, headers=config.content_type, data=encoded_params)
    req.raise_for_status()
    response = req.json()

    if "refresh_token" not in response:
        response["refresh_token"] = tokens["refresh_token"]

    save_tokens(config.name, response)
    config.access_token = response["access_token"]
    config.refresh_token = response["refresh_token"]
    config.headers = generate_headers(config)
    return config


# Wrapper for REST methods that checks for API request errors
def api_call(config, method, url, **kwargs):
    req = method(url, **kwargs)
    if req.status_code == 401:
        handle_tokens(config)
        kwargs['headers'] = config.headers
        req = method(url, **kwargs)
    req.raise_for_status()
    return req