from TinderApi import Tinder


tinder = Tinder(debug=True)
tinder.login(
    "your_phone_number",
    "your_email",
    store_auth_token=True
)