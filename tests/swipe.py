from TinderApi import Tinder
import json
import time
import random
tinder = Tinder(
    debug=True,
    x_auth_token="your_auth_token",
)

while True:
    users_to_swipe = tinder.swipe.get_users()
    for user in users_to_swipe:
        liked_user = tinder.swipe.like_user(user["user_id"])
        if liked_user["match"]:
            tinder.debugger.Log("Matched with "+json.dumps(liked_user))
        else:
            tinder.debugger.Log("Swiped yes on "+json.dumps(liked_user))
        time.sleep(random.randint(1, 3))