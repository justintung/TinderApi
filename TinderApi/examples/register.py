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