#!/usr/bin/env python3.13
import requests
from winston_shared.twitch_calls import chat_post
from winston_shared.auth import api_call


# Retrieve the song link, name, and artist name
def get_song_info(track_id, poster, spotify, bot, message):
    track_id = track_id.split("?")[0]
    try:
        req = api_call(
            spotify,
            requests.get,
            f"{spotify.api_uri}tracks/{track_id}",
            headers=spotify.headers
        )

        response = req.json()
        song_uri = response["uri"]
        artist_name = response['artists'][0]['name']
        song_name = response["name"]
        return song_uri, song_name, artist_name

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            chat_post(bot, message['spotify']['invalid_link'].format(poster=poster))
            raise ValueError("Invalid Spotify ID")
        else:
            raise


# Add song to the queue
def add_to_queue(song_uri, song_name, artist_name, poster, spotify, bot, message):
    try:
        req = api_call(
            spotify,
            requests.post,
            f"{spotify.api_uri}me/player/queue?uri={song_uri}",
            headers=spotify.headers
        )
        chat_post(bot, message['spotify']['added_to_queue'].format(poster=poster, song_name=song_name, artist_name=artist_name))

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            chat_post(bot, message['spotify']['player_off'].format(poster=poster))
        else:
            raise


# Display current song, or alert chatter that spotify isn't active
def check_queue(poster, text, spotify, bot, message):
    req = api_call(
        spotify,
        requests.get,
        f"{spotify.api_uri}me/player/queue",
        headers=spotify.headers
    )
    response = req.json()

    if response['currently_playing']:
        if text == "!song":
            song_name = response['currently_playing']['name']
            artist_name = response['currently_playing']['album']['artists'][0]['name']
            chat_post(bot, message['spotify']['current_song'].format(poster=poster, song_name=song_name, artist_name=artist_name))
        elif text == "!next":
            try:
                song_name = response['queue'][0]['name']
                artist_name = response['queue'][0]['album']['artists'][0]['name']
                chat_post(bot, message['spotify']['next_song'].format(poster=poster, song_name=song_name, artist_name=artist_name))
            except IndexError:
                chat_post(bot, message['spotify']['no_queue'].format(poster=poster))
    else:
        chat_post(bot, message['spotify']['player_inactive'].format(poster=poster))