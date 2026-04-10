#!/usr/bin/env python3.13
import requests
import json
from winston_shared.auth import api_call


EVENTSUB_TYPES = [
    {'type': 'channel.chat.message', 'version': '1', 'condition_key': 'user_id'},
    {'type': 'channel.follow', 'version': '2', 'condition_key': 'moderator_user_id'},
    {'type': 'channel.suspicious_user.message', 'version': '1', 'condition_key': 'moderator_user_id'},
]

# List comprehension to build event subs dicts
def build_eventsubs(streamer, session_id):
    return [{
        'type': sub['type'],
        'version': sub['version'],
        'condition': {
            'broadcaster_user_id': streamer.channel,
            sub['condition_key']: streamer.bot
        },
        'transport': {
            'method': 'websocket',
            'session_id': session_id
        }
    } for sub in EVENTSUB_TYPES]


# Gather the user information for broadcaster and poster
def get_user_info(poster, streamer):
    req = api_call(
        streamer, requests.get,
        f"{streamer.api_uri}users?login={poster}&login={streamer.channel_name}",
        headers=streamer.headers
    )

    response = req.json()

    if len(response['data']) == 1:
        return

    users = {u['login']: u for u in response['data']}
    broadcaster = users[streamer.channel_name]
    user = users[poster]

    broadcaster_display_name = broadcaster['display_name']
    user_id = user['id']
    user_display_name = user['display_name']
    return broadcaster_display_name, user_id, user_display_name


# function for twitch chat API post
def chat_post(streamer, message):
    api_call(
        streamer,
        requests.post,
        f"{streamer.api_uri}chat/messages",
        headers=streamer.headers,
        json={"broadcaster_id": streamer.channel, "sender_id": streamer.bot, "message": message}
    )


# Ban user. Intercept 400 (user cannot be banned) and 409 (someone else is banning the user) errors
def ban_user(poster, streamer, message):
    user_info = get_user_info(poster, streamer)

    # The streamer tried to ban themselves.
    if user_info is None:
        chat_post(streamer, message['moderation']['self_ban'])
        return
    else:
        broadcaster_display_name, user_id, user_display_name = user_info

    try:
        req = api_call(
            streamer,
            requests.post,
            f"{streamer.api_uri}moderation/bans?broadcaster_id={streamer.channel}&moderator_id={streamer.bot}",
            headers=streamer.headers,
            json={'data': {'user_id': user_id}}
        )

        chat_post(streamer, message['moderation']['ban_success'].format(user_display_name=user_display_name))

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            chat_post(streamer, message['moderation']['ban_failed'].format(broadcaster_display_name=broadcaster_display_name, user_display_name=user_display_name))
        elif e.response.status_code == 409:
            chat_post(streamer, message['moderation']['ban_conflict'].format(broadcaster_display_name=broadcaster_display_name, user_display_name=user_display_name))
        else:
            raise


# monitor events and return their payload
def eventsub_handler(streamer, event):
    event = json.loads(event)
    payload = event['payload']

    if 'session' in payload:
        session_id = payload['session']['id']
        for sub in build_eventsubs(streamer, session_id):
            api_call(
                streamer,
                requests.post,
                f"{streamer.api_uri}eventsub/subscriptions",
                headers=streamer.headers,
                json=sub
            )
    return event['payload']


# Parse through returned eventsub_handler payload. Drop the parse if session_keepalive
def parse_payload(payload):
    if 'event' not in payload:
        raise KeyError(("No event in payload. Continuing."))
    event_type = payload['subscription']['type']

    if event_type == "channel.follow":
        follower = payload['event']['user_name']
        return event_type, follower, None, None

    if event_type == "channel.suspicious_user.message":
        poster = payload['event']['user_name']
        return event_type, None, poster, None

    poster = payload['event']['chatter_user_name']
    text = payload['event']['message']['text']
    if "https://open.spotify.com/track" not in text:
        text = text.lower()
    return event_type, None, poster, text