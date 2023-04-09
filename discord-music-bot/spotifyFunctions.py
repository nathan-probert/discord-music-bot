import spotipy
import os
import base64
import requests


def get_token(CLIENT_ID, CLIENT_SECRET):
    token_url = "https://accounts.spotify.com/api/token"

    client_creds = (f"{CLIENT_ID}:{CLIENT_SECRET}")
    client_creds_b64 = base64.b64encode(client_creds.encode())

    token_data = {
        "grant_type": "client_credentials"
    }

    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    r = requests.post(token_url, data=token_data, headers=token_headers)
    response_data = r.json()
    access_token = response_data['access_token']
    
    # allows access to spotify (needed for getting playlist info)
    return access_token


async def makePlaylist(ctx, playlist_name, url):
    if not os.path.exists("playlists"):
            os.makedirs("playlists")

    filename = (f"playlists\\{playlist_name}.txt")
    # with open(filename, 'w+') as fileOut:
    with open("discord-music-bot\\secret.txt", 'r') as fileReader:
        content = fileReader.readlines()
    fileReader.close()

    username = content[1]
    access_token = get_token(content[2].strip(), content[3].strip())

    spotify = spotipy.Spotify(auth=access_token)

    results = spotify.user_playlist(username, url, fields='tracks,next,name')
    print(f"Writing {results['tracks']['total']} tracks to {filename}.")
    await ctx.send(f"Writing {results['tracks']['total']} tracks to {playlist_name}.")

    tracks = results['tracks']
    write_tracks(filename, tracks, spotify)


def write_tracks(filename, tracks, spotify):
    # Writes the information of all tracks in the playlist to a text file.

    with open(filename, 'w+') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    csv_line = track_name + " by " + track_artist + "\n"
                    try:
                        file_out.write(csv_line)
                    except UnicodeEncodeError:  # Most likely caused by non-English song names
                        print("Track named {} failed due to an encoding error. This is \
                            most likely due to this song having a non-English name.".format(track_name))
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                        track['name'], track['artists'][0]['name']))
                except TypeError:
                    print("type error")
            # 1 page = 50 results, check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break