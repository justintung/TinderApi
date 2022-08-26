from ..protos.authgateway import *
from ..protos.media_responses import *
from ..protos.create_placeholder_request import *

class Media:
    def __init__(self, api):
        self.api = api
    
    def create_placeholder(self, count):
        """UNFINISHED DONT USE"""
        body = CreatePlaceholderRequest(num_pending_media=count)
        res = self.api.s.post("/mediaservice/placeholders", 1, params="?locale="+self.api.locale, headers={"content-type": "application/x-google-protobuf", "x-supported-image-formats": "webp,jpeg"}, data=bytes(body), json=False)
        response = ClientDataProto().parse(res.content).to_dict()
        return response
    
    def photo_prepare(self, file_path, media_id):
        """UNFINISHED DONT USE"""
        files = {'file': open(file_path, "rb")}
        res = self.api.s.post("/mediaservice/photo", 1, params="?locale="+self.api.locale, files=files, headers={"x-media-id": media_id})
        print(res)
        
        