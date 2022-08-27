import random


class Utils:
    def __init__(self, api) -> None:
        self.api = api
        
    def parsePhotos(self, photos: list):
        photo_list = []
        for photo in (photos):
            photo_list.append(photo["url"])
        return photo_list

    def saveToFile(self, path, string):
        with open(path, "w+") as f:
            f.write(string)
            f.close()

    def set_image_tuples(self, image_paths):
        photos = []
        for image_path in image_paths:
            photos.append(
                ('images', ('photo', open(image_path, 'rb'), 'image/png')),
            )
        print(photos)
        return photos
            

    def parseSpotifyArtists(self, artists: list):
        spotify_artists = []

        for artist in artists:
            spotify_artists.append({
                "artist_id": artist["id"],
                "name": artist["name"],
                "top_track": {
                    "track_id": artist["top_track"]["id"],
                    "track_name": artist["top_track"]["name"],
                    "artists": artist["top_track"]["artists"],
                    "album": {
                        "id": artist["top_track"]["album"]["id"],
                        "name": artist["top_track"]["album"]["name"],
                    }
                }
            })
        return spotify_artists

    def parseLifestyles(self, descriptors: list):
        new_lifestyles = {}
        for d in descriptors:
            for descriptor in d["descriptors"]:
                key = descriptor["name"]
                new_lifestyles[key] = descriptor
                
        return new_lifestyles       
    
    def parseSwipes(self, swipes: list):
        """
        Makes a new dict out of the data that tinder returns from swipes, the data is not the same as a normal user.
        """
        new_swipes = []
        for swipe in swipes:
            user = swipe["user"]
            new_swipes.append({
                "user_id": user["_id"],
                "bio": user["bio"],
                "birth_date": user["birth_date"] if 'birth_date' in user else 'No birth date found...',
                "name": user["name"],
                "city": user["city"] if 'city' in user else {"name": "Unknown"},
                "schools": user["schools"],
                "jobs": user["jobs"],
                "photos": self.parsePhotos(user["photos"]),
                "gender": user["gender"],
                "recently_active": user["recently_active"],
                "distance": swipe["distance_mi"],
                "interests": swipe["experiment_info"]["user_interests"]["selected_interests"] if 'experiment_info' in swipe else []
            })
        return new_swipes

    def parseUsers(self, users: list):
        """
        Makes a new dict out of the data that tinder returns from a user, otherwise there's just too much to read
        """
        newUsers = []
        for user in users:
            newUsers.append({
                "match_id": user["_id"],
                "messages": user["messages"],
                "created_at": user["created_date"],
                "user_id": user["person"]["_id"],
                "bio": user["person"]["bio"] if "bio" in user["person"] else "No bio found...",
                "birth_date": user["person"]["birth_date"] if 'birth_date' in user["person"] else 'No birth date found...',
                "name": user["person"]["name"],
                "gender": user["person"]["gender"],
                "last_active": user["last_activity_date"],
                "images": self.parsePhotos(user["person"]["photos"])
            })
        return newUsers

    def gen_temp_messageid(self):
        return str(random.randint(1670880186952589, 9670880186952589))

    def gen_s_number(self):
        return random.randint(447198460, 1147198460)

    def random_cooldown(self):
        return random.randint(3, 10)