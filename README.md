# Unofficial Tinder-API in Python

An unofficial api wrapper for tinder.
To see more examples, check the tests folder.
For any problems you may have, open an issue in this repo.

|Api Type | Info
|--- | ---
|✔️ Authentication| `Supports authentication both login & providing already existing auth`
|✔️ Registering|`Supports registering a new account if you do not have one`
|✔️ Messaging|`Supports sending & getting messages from/to matches`
|✔️ Swiping|`Supports fetching users to swipe on & liking/passing on them`
|✔️ Matches|`Supports fetching matches & messages with matches`
|✔️ Users|`Supports getting user data by id/username`
|✔️ Account|`Supports getting account data and editing account`
|✔️ Spotify|`Supports getting popular playlists/songs on tinder today`
|✔️ Captcha Solver|`Supports captcha solving with 2captcha, currently this is not used`
|✔️ Tinder+ Support|`Supports tinder gold/premium/platinum features if you have it`
|❌ Media| `Currently i do not have a solution to uploading photos/media to profile, But protobufs & endpoints are implemented.`

### Installation
`pip install MTinderApi`

**Getting users to swipe and swiping**
```py
from TinderApi import Tinder

tinder = Tinder(debug=True, x_auth_token="your_auth_token")
users_to_swipe = tinder.swipe.get_users()

for user in users_to_swipe:
    liked = tinder.swipe.like_user(user["user_id"]) # LIKE USER
    print(liked) # -> {'status': 200, 'match': False, 'user_id': 'some_user_id', 'likes_left': 100}
```


**Logging in to tinder**
```py
from TinderApi import Tinder

tinder = Tinder(debug=True)
tinder.login(
    "your_phone_number",
    "your_email",
    store_auth_token=True
)
```

**Registering a new account**
```py
from TinderApi import Tinder

tinder = Tinder(debug=True)
fields = [
        {
            "data": "1995-10-10",
            "name": "birth_date"
        }, 
        {
            "data": 0,
            "name": "gender"
        }, 
        {
            "data": False,
            "name": "show_gender_on_profile"
        }, 
        {
            "data": [1],
            "name": "interested_in_gender"
        }, 
        {
            "data": {"checked": False, "should_show_option": False},
            "name": "show_same_orientation_first"
        }, 
        {
            "data": "David",
            "name": "name"
        },
        {
            "data": False,
            "name": "show_orientation_on_profile"
        }
]
tinder.register(
    phone_number="", # ONLY USA NUMS
    email="",
    fields=fields,
    photo_path="photo1.jpg",
    store_account_data=True
)
```
