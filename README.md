# TinderApi

An unofficial api wrapper for tinder. For more examples, check the example folder.

```py
from TinderApi import Tinder

tinder = Tinder(debug=True, x_auth_token="your_auth_token")
users_to_swipe = tinder.swipe.get_users()

for user in users_to_swipe:
    liked = tinder.swipe.like_user(user["user_id"]) # LIKE USER
    print(liked) # -> {'status': 200, 'match': False, 'user_id': 'some_user_id', 'likes_left': 100}
```


# Login to tinder
```py
from TinderApi import Tinder

tinder = Tinder(debug=True)
tinder.login(
    "your_phone_number",
    "your_email",
    store_auth_token=True
)
```

# Register a new account
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
