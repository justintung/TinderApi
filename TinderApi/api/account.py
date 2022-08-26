from datetime import datetime
import json
from ..exceptions import *


class Account:
    def __init__(self, api):
        self.api = api
        
    def get_me(self) -> dict:
        res = self.api.s.get("/profile", 2, params=f"?locale={self.api.locale}&include=user,account")
        self.api.debugger.Log(f"Logged in as {json.dumps(res['data']['account'])}")
        return res["data"]["user"]
    
    def liked_you(self, pageToken=None):
        res = self.api.s.get("/fast-match", 2, params=f"?locale={self.api.locale}"+f"page_token={pageToken}" if pageToken else "")
        users = self.api.util.parseSwipes(res["data"]["results"])
        return {"users": users, "pageToken": res["data"]["next_page_token"]}
    
    def verify_email(self, email_token):
        payload = {
            "token": email_token
        }
        res = self.api.s.post("/account/account-email/confirm", 2, data=payload)
        return res
    
    def set_username(self, username: str) -> dict:
        payload = {
            "username": username
        }
        res = self.api.s.put("/profile/username", 1, data=payload)
        return res

    def set_lifestyles(self, descriptors: list):
        """Sets the livestyle option in ur profile

        Args:
            descriptors (list): List of descriptors, to get available ones use TinderApi.account.lifestyle_selections()
            Example:
                   set_lifestyles(
                       descriptors=[ {"id": "id_of_zodiac", "choice_selections": [{"id": "id_of_selection_in_zodiac_descriptor"}] } ]
                   )
        """
        payload = {
            "selected_descriptors": [descriptors]
        }
        res = self.api.s.post("/profile/user?locale="+self.api.locale, data=payload)
        return res["data"]
        

    def set_location(self, longitude: float, latitude: float) -> dict:
        payload = {
            "lat": latitude,
            "lon": longitude
        }
        res = self.api.s.post("/passport/user/travel", 1, data=payload)
        return res

    def set_school(self, school_name):
        if len(school_name) > 128:
            raise InputStringTooLong(school_name)
        payload = {
            "schools": [
                {"displayed": True if len(school_name) else False, "name": school_name},
            ]
        }
        res = self.api.s.post("/profile/school", 2, params=f"?locale={self.api.locale}", data=payload)
        return res["data"]["user"]

    def set_job(self, job_title="", company=""):
        if len(job_title) > 128 or len(company) > 128:
            raise InputStringTooLong(job_title if len(job_title) > 128 else company)
        payload = {
            "jobs": [
                {
                    "company": {"displayed": True if len(company) else False, "name": company},
                    "title": {"displayed": True if len(job_title) else False, "name": job_title}
                }
            ]
        }
        res = self.api.s.post("/profile/job", 2, params=f"?locale={self.api.locale}", data=payload)
        return res["data"]["user"]
    
    def set_city(self, city, region, latitude=0, longitude=0):
        payload = {
            "name": city,
            "region": region,
            "coords": {
                "latitude": latitude,
                "longitude": longitude
            }
        }
        res = self.api.s.post("/profile/city?locale="+self.api.locale, data=payload)
        return res["meta"]["status"]

    def set_spotify_anthem(self, track_id):
        """Sets your spotify anthem in the tinder settings

        Args:
            track_id (str): spotify track_id, u can get a list of popular spotify songs from TinderApi.misc.popular_spotify()

        Returns:
            dict: Tinder json response
        """
        payload = {
            "id": track_id
        }
        res = self.api.s.put("/profile/spotify/theme", 2, params=f"?locale={self.api.locale}", data=payload)
        return res["data"]

    def update_profile(self, bio=None, interests=None, gender=None, show_gender_on_profile=None) -> dict:
        payload = {
            "user": {
            }
        }
        if bio:
            payload["user"]["bio"] = bio
        if interests:
            if len(interests) < 3:
                raise 'Interests list needs to contain at least 3 dicts of interests'
            payload["user"]["user_interests"]["selected_interests"] = interests
        if gender:
            payload["user"]["gender"] = gender
        if show_gender_on_profile:
            payload["user"]["show_gender_on_profile"] = show_gender_on_profile
        try:
            res = self.api.s.post("/profile", 2, data=payload)
            return res
        except:
            raise FailedToUpdateProfile
        
    def upload_image(self, photos: list):
        if type(photos) != list or len(photos) < 1:
            raise InvalidPhotoList
        placeholder_data = self.api.media.create_placeholder(count=len(photos))
        media_ids = placeholder_data["createPlaceholderResponseModel"]["mediaIds"]
        for i, photo in enumerate(photos):
            print(photo, i)
            self.api.media.photo_prepare(photo, media_ids[i])
            exit()

    def get_subscriptions(self):
        res = self.api.s.get("/purchase", params="?locale="+self.api.locale)
        return res["results"]

    def lifestyle_selections(self):
        res = self.api.s.get("/profile", 2, params=f"?locale={self.api.locale}&include=available_descriptors")
        return self.api.util.parseLifestyles(res["data"]["available_descriptors"])
    
    def available_interests(self):
        return self.get_me()["user_interests"]["available_interests"]
    
    def get_updates(self):
        last_active = str(datetime.now()).split(" ")
        last_active[0] += "T"
        last_active[1] += "Z"
        data = {
            "last_activity_date": "".join(last_active),
            "nudge": True
        }
        res = self.api.s.post("/updates", 1, data=data)
        return res