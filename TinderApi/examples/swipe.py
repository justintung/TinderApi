from TinderApi import Tinder



tinder = Tinder(debug=True, x_auth_token="your_auth_token")



users_to_swipe = tinder.swipe.get_users()

for user in users_to_swipe:
    liked = tinder.swipe.like_user(user["user_id"]) # LIKE USER
    passed = tinder.swipe.pass_user(user["user_id"]) # PASS USER
    print(liked) # -> {'status': 200, 'match': False, 'user_id': 'some_user_id', 'likes_left': 100}
    