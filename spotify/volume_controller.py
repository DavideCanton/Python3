import time
import spotipy
import spotipy.util as util
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

from _tokens import USERNAME, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

SCOPES = "user-read-playback-state user-read-currently-playing"
token = util.prompt_for_user_token(
    USERNAME,
    SCOPES,
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI
)

sessions = AudioUtilities.GetAllSessions()
spotify_session = None
current_volume = None
for session in AudioUtilities.GetAllSessions():
    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
    if session.Process and session.Process.name() == "Spotify.exe":
        spotify_session = volume
        current_volume = spotify_session.GetMasterVolume()

if not spotify_session:
    raise Exception('Can\'t find Spotify')
else:
    print("Found running instance of spotify, current volume =", current_volume)

if token:
    sp = spotipy.Spotify(auth=token)
    while True:
        try:
            play = sp.current_playback()
            play_type = play['currently_playing_type']
            if play_type == 'ad':
                spotify_session.SetMasterVolume(0, None)
                print("Playing ad...")
            elif play_type == 'track':
                item = play['item']
                artist = item['album']['artists'][0]['name']
                name = item['name']
                spotify_session.SetMasterVolume(current_volume, None)
                print(f"Playing {name} from {artist}...")
        except Exception as e:
            print(f"Got error: {e}")
        time.sleep(5)
else:
    print("Can't get token for", username)
