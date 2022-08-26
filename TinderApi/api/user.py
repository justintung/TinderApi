from ..exceptions import *
import json


class User:
    def __init__(self, api):
        self.api = api
    
    def get_user_by_id(self, user_id: str) -> dict:
        try:
            res = self.api.s.get(f"/user/{user_id}", 1)["results"]
            return {
                "name": res["name"],
                "birth_date": res["birth_date"],
                "id": res["_id"],
                "schools": res["schools"],
                "gender": "female" if res["gender"] == 1 else "male",
                "bio": res["bio"],
                "distance_in_miles": res["distance_mi"],
                "spotify_top_artists": self.api.util.parseSpotifyArtists(res["spotify_top_artists"]),
                "interests": res["user_interests"]["selected_interests"],
                "images": self.api.util.parsePhotos(res["photos"])
            }
        except:
            raise UserNotFound
    
    def get_user_by_username(self, username: str) -> dict:
        try:
            res = self.api.s.get("https://tinder.com/@"+username, -1, json=False).text
            webProfile = json.loads(
                res.split('window.__data=')[1].split("};")[0]+"}"
            )["webProfile"]
            webProfile["user"]["photos"] = self.api.util.parsePhotos(webProfile["user"]["photos"])
            return webProfile
        except:
            raise UserNotFound