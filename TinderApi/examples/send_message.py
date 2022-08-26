from TinderApi import Tinder



tinder = Tinder(debug=True, x_auth_token="your_auth_token")

matches = tinder.matches.get_matches()

for match in matches:
    data = tinder.matches.send_message(match["match_id"], "tja")
    print(data) # -> {'_id': '', 'from': '', 'to': '', 'match_id': '', 'sent_date': '2022-08-26T19:07:39.568Z', 'message': '', 'media': {'width': None, 'height': None}, 'created_date': '2022-08-26T19:07:39.568Z'}

