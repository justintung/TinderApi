from ..exceptions import *


class Matches:
    def __init__(self, api):
        self.api = api
    
    def get_matches(self, count=100, with_messages=False) -> list:
        matches = []
        res = self.api.s.get(f"/matches", 2, params=f"?locale={self.api.locale}&count={count}&message={'0' if not with_messages else '1'}&is_tinder_u=false")
        matches = self.api.util.parseUsers(res["data"]["matches"])
        return matches

    def get_all_matches(self, pageToken=None, with_messages=False):
        try:
            matches = []
            while True:
                res = self.api.s.get("/matches", 2, params=f"?locale={self.api.locale}&count=100&message={'0' if not with_messages else '1'}&is_tinder_u=false{'&page_token='+pageToken if pageToken else ''}")
                pageToken = res["data"]["next_page_token"] if "next_page_token" in res["data"] else None
                for match in res["data"]["matches"]:
                    matches.append({
                        "match_id": match["_id"],
                        "messages": match["messages"],
                        "created_at": match["created_date"],
                        "user_id": match["person"]["_id"],
                        "bio": match["person"]["bio"] if "bio" in match["person"] else "No bio found...",
                        "birth_date": match["person"]["birth_date"],
                        "name": match["person"]["name"],
                        "gender": "female" if match["person"]["gender"] == 1 else "male",
                        "last_active": match["last_activity_date"],
                        "images": self.api.util.parsePhotos(match["person"]["photos"])
                    })
                if "next_page_token" not in res["data"]:
                    break
            return matches
        except:
            raise Exception("Failed to parse json response")
    
    def delete_match(self, match_id):
        res = self.api.s.delete(f"/matches/{match_id}", 2)
        if res.status_code == 404:
            raise InvalidMatchId
        if res.status_code > 204:
            raise UserNotFound
        return True
    
    def get_match(self, match_id):
        res = self.api.s.get("/matches/"+match_id, 2)
        return res["data"]
    
    def get_all_messages(self) -> list:
        matches = self.get_all_matches(with_messages=True)
        messages = []
        for match in matches:
            messages.append({
                "match_id": match["_id"],
                "messages": match["messages"]
            })
        return messages

    
    def get_messages(self, match_id, count="100") -> list:
        res = self.api.s.get(f"/matches/{match_id}/messages", 2, params=f"?count={count}")
        if 'data' not in res:
            raise InvalidMatchId
        return res["data"]["messages"]


    def send_message(self, match_id, message, contact_type=None) -> dict:
        """
        Sends a message to a match, returns MessageDict on success

        Returns MessageError exception on fail
        """
        self.api.debugger.Log("Attempting to send message to "+match_id)
        user_id, other_id = match_id[:len(match_id)//2], match_id[len(match_id)//2:]
        payload = {
            "matchId": match_id,
            "message": message,
            "otherId": other_id,
            "sessionId": None,
            "tempMessageId": f"0.{self.api.util.gen_temp_messageid()}",
            "userId": user_id
        }
        if contact_type:
            if contact_type not in self.api.contact_types:
                raise InvalidContactType
            payload["contact_type"] = contact_type
            payload["type"] = "contact_card"
        try:
            res = self.api.s.post(f"/user/matches/{match_id}", 1, data=payload)
        except:
            self.api.debugger.Log("Failed to send message to "+match_id)
            raise TinderMatchNotFound
        if 'sent_date' in res:
            self.api.debugger.Log("Successfully sent a message to "+match_id)
            return res
        else:
            self.api.debugger.Log("Failed to send message to "+match_id)
            raise MessageError