import math



class Misc:
    def __init__(self, api):
        self.api = api
        
    def popular_spotify(self, limit="20", offset="0", type="track"):
        res = self.api.s.get("/profile/spotify/popular", 2, params=f"?locale={self.api.locale}&limit={limit}&offset={offset}&type={type}")
        return { "tracks": self.parse_spotify(res["data"]["popular_on_spotify_playlist"]), "playlist_uri": res["data"]["popular_on_spotify_playlist"]["uri"], "spotify_type": res["data"]["popular_on_spotify_playlist"]["type"], "description": res["data"]["popular_on_spotify_playlist"]["description"]}
    
    def parse_spotify(self, data):
        tracks = data["tracks"]
        new_tracks = []
        for track in tracks["items"]:
            album = track["track"]["album"]
            new_tracks.append({
                "added_at": track["added_at"],
                "album": {
                    "name": album["name"],
                    "release_date": album["release_date"],
                    "uri": album["uri"],
                    "images": self.api.util.parsePhotos(album["images"]),
                    "total_tracks": album["total_tracks"],
                    "open_spotify": album["external_urls"]["spotify"],
                },
                "track": {
                    "artists": track["track"]["artists"],
                    "duration_ms": track["track"]["duration_ms"],
                    "duration_s": track["track"]["duration_ms"]/1000,
                    "duration_m": math.ceil((track["track"]["duration_ms"]/1000)/60),
                    "name": track["track"]["name"],
                    "id": track["track"]["id"],
                    "uri": track["track"]["uri"],
                    "popularity": track["track"]["popularity"]
                }
            })
        return new_tracks
    
    def promo_code_eligibility(self, code):
        payload = {
            "code": code
        }
        res = self.api.s.post("/incentives/eligibility", 2, params="?locale="+self.api.locale, data=payload)
        return res