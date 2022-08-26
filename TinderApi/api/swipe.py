import time
from ..exceptions import *



class Swipe:
    def __init__(self, api):
        self.api = api
        
    def get_users(self) -> list:
        res = self.api.s.get("/recs/core", 2)
        return self.api.util.parseSwipes(res["data"]["results"])

    def like_user(self, user_id, super_like=False) -> dict:
        ep = "/like/"+user_id
        if super_like:
            ep += "/super"
        payload = {
            "s_number": self.api.util.gen_s_number(),
            "user_traveling": 1
        }
        try:
            res = self.api.s.post(ep, 1, data=payload)
        except:
            raise TinderRatelimited
        if not 'likes_remaining' in res:
            print(res)
        response = {'status': res["status"], 'match': False if not res["match"] else True, "user_id": user_id }
        if "super_likes" in res:
            response["super_likes_left"] = res["super_likes"]["remaining"]
        if 'likes_remaining' in res:
            response['likes_left'] = res["likes_remaining"]
        return response
    
    def pass_user(self, user_id, fast_match=False):
        res = self.api.s.get(f"/pass/{user_id}", 1, params=f"?locale={self.api.locale}&s_number={self.api.util.gen_s_number()}&user=traveling=1{'&fast_match=1' if fast_match else ''}")
        if res["status"] == 200:
            return True
        else:
            return False