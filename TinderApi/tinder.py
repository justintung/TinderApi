import json
import sys

from TinderApi.api.account import Account
from TinderApi.api.swipe import Swipe
from TinderApi.browser import Browser
from TinderApi.protos.authgateway import *
from TinderApi.captcha import Captcha
from TinderApi.api.matches import Matches
from TinderApi.utils import Utils
from TinderApi.api.misc import Misc
from TinderApi.api.user import User
from TinderApi.api.media import Media
from TinderApi.exceptions import *
from TinderApi.debugger import Debugger
from TinderApi.session import Session

class Tinder:
    def __init__(self, debug=False, **args) -> None:
        """_Tinder class, for everything this package has to offer_

        Args:
            x_auth_token (str): Must be provided unless auth_file is provided.
            auth_file (str): Must be provided unless x_auth_token is provided.
            user_agent (str, optional): If you want to use a custom user-agent.
            debug (bool, optional): If you want to see everything that happens while you're using the package. Defaults to False.
            locale (str, optional): No idea what this actually does, but defaults to en.
        """
        self.debugger = Debugger(debug=True) if debug else Debugger()
        self.locale = args.get("locale") if args.get("locale") else "en"
        self.s = Session(self, **args)
        self.next_page_token = ""
        self.contact_types = ["snapchat", "instagram"]
        self.util = Utils(self)
        self.media = Media(self)
        self.misc = Misc(self)
        self.matches = Matches(self)
        self.user = User(self)
        self.account = Account(self)
        self.swipe = Swipe(self)
        self.browser = Browser(self)
        if args.get("captcha_key"):
            self.captcha = Captcha(args.get("captcha_key"))
            
    def login(self, phone_number, email, store_auth_token=False, registerFields=False, photo_path=False):
        """Login to a tinder account, requires phone and email.

        Args:
            phone_number (str): Phone number on the tinder account
            email (str): Email on the tinder account
            store_auth_token (bool, optional): If you want to store the auth token in a txt file after login is done. Defaults to False.

        Returns:
            dict: Account data
        """
        self.email = email
        self.phone_number = phone_number
        no_captcha_payload = {
            "device_id": self.s.session.headers["install-id"],
            "experiments": ["default_login_token", "tinder_u_verification_method", "tinder_rules", "user_interests_available"]
        }
        self.s.session.headers["content-type"] = "application/json; charset=UTF-8"
        self.s.post("/buckets", 2, json=no_captcha_payload) # Disables captcha
        #captcha_token = self.captcha.solve("funcaptcha", "https://tinder.com/", "&publickey=B5B07C8C-F93F-44A8-A353-4A47B8AD5238&surl=https://client-api.arkoselabs.com") (If they fix their shitty api so that captcha starts working again)
        self.s.session.headers["content-type"] = "application/x-protobuf"
        body = AuthGatewayRequest(phone=Phone(phone=phone_number))
        r = self.s.post("/auth/login", 3, data=bytes(body), json=False)
        response = AuthGatewayResponse().parse(r.content).to_dict()
        if 'validatePhoneOtpState' in response:
            if not response["validatePhoneOtpState"]["smsSent"]:
                self.debugger.Log("Could not send sms. "+json.dumps(response))
                exit()
            self.debugger.Log(f"Input the {str(response['validatePhoneOtpState']['otpLength'])} digit code sent to {response['validatePhoneOtpState']['phone']}")
            code = input("> ")
            body = AuthGatewayRequest(phone_otp=PhoneOtp(phone=phone_number, otp=code))
            r = self.s.post("/auth/login", 3, data=bytes(body), json=False)
            response = AuthGatewayResponse().parse(r.content).to_dict()
            self.debugger.Log(json.dumps(response))
            if 'validateEmailOtpState' in response:
                refresh_token = response['validateEmailOtpState']['refreshToken']
                self.debugger.Log(f"Input the 6 digit code sent to your email ({email}) (register)")
                code = input("> ")
                body = AuthGatewayRequest(email_otp=EmailOtp(otp=code, email=email, refresh_token=refresh_token))
                r = self.s.post("/auth/login", 3, data=bytes(body), json=False)
                response = AuthGatewayResponse().parse(r.content).to_dict()
                is_success = self.check_login(response, email, phone_number, store_auth_token=store_auth_token)
                if is_success:
                    return is_success
                else:
                    self.debugger.Log("Failed to login: "+json.dumps(response))
            elif 'getEmailState' in response:
                refresh_token = response["getEmailState"]["refreshToken"]
                body = AuthGatewayRequest(email=Email(email=email, refresh_token=refresh_token))
                r = self.s.post("/auth/login", 3, data=bytes(body), json=False)
                response = AuthGatewayResponse().parse(r.content).to_dict()
                if 'validateEmailOtpState' in response:
                    self.debugger.Log(f"Input the 6 digit code sent to your email ({email})")
                    code = input("> ")
                    body = AuthGatewayRequest(email_otp=EmailOtp(otp=code, email=email, refresh_token=refresh_token))
                    r = self.s.post("/auth/login", 3, data=bytes(body), json=False)
                    response = AuthGatewayResponse().parse(r.content).to_dict()
                    is_success = self.check_login(response, email, phone_number, store_auth_token=store_auth_token)
                    if is_success:
                        return is_success
                    else:
                        self.debugger.Log("Failed to login: "+json.dumps(response))
                elif 'onboardingState' in response:
                    self.debugger.Log("Boarding State Response: "+json.dumps(response))
                    refresh_token = response["onboardingState"]["refreshToken"]
                    boarding_token = response["onboardingState"]["onboardingToken"]
                    fields = {
                        "fields": registerFields
                    }
                    self.s.session.headers["content-type"] = "application/json"
                    self.s.session.headers["token"] = boarding_token
                    boarding_fields_request = self.s.post("/onboarding/fields", 2, data=fields, params="?requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=interested_in_gender&requested=name&requested=photos&requested=sexual_orientations&requested=show_gender_on_profile&requested=show_orientation_on_profile&requested=show_same_orientation_first&requested=tinder_rules&requested=user_interests")
                    field_res = boarding_fields_request
                    if field_res["meta"]["status"] == 200:
                        self.debugger.Log("Passed fields stage!")
                        # Send in photos
                        del self.s.session.headers["content-type"]
                        photo = {'photo': open(photo_path, "rb")}
                        boarding_photos_request = self.s.post("/onboarding/photo", 2, files=photo, params="?requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=interested_in_gender&requested=name&requested=photos&requested=sexual_orientations&requested=show_gender_on_profile&requested=show_orientation_on_profile&requested=show_same_orientation_first&requested=tinder_rules&requested=user_interests")
                        photos_res = boarding_photos_request
                        if photos_res["meta"]["status"] == 200:
                            self.s.session.headers["content-type"] = "text/plain;charset=UTF-8"
                            self.s.session.headers["x-refresh-token"] = refresh_token
                            complete_profile = self.s.post("/onboarding/complete", 2, data={}, params="?requested=allow_email_marketing&requested=birth_date&requested=consents&requested=email&requested=gender&requested=interested_in_gender&requested=name&requested=photos&requested=sexual_orientations&requested=show_gender_on_profile&requested=show_orientation_on_profile&requested=show_same_orientation_first&requested=tinder_rules&requested=user_interests")
                            complete_res = complete_profile
                            if complete_res["meta"]["status"] == 200:
                                self.debugger.Log("Successfully updated profile and profile photos.")
                                del self.s.session.headers["x-refresh-token"]
                                del self.s.session.headers["token"]
                                self.s.session.headers["content-type"] = "application/x-protobuf"
                                body = AuthGatewayRequest(refresh_auth=RefreshAuth(refresh_token=refresh_token))
                                r = self.s.post("/auth/login", 3, data=bytes(body), json=False)
                                response = AuthGatewayResponse().parse(r.content).to_dict()
                                self.debugger.Log("Last Login Request: "+json.dumps(response))
                                is_success = self.check_login(response, email, phone_number, store_auth_token=store_auth_token)
                                if is_success:
                                    return is_success
                                else:
                                    self.debugger.Log("Failed to login: "+json.dumps(response))
                            else:
                                self.debugger.Log("Failed to complete profile. "+json.dumps(complete_res))  
                        else:
                            self.debugger.Log("Failed to set photos: "+json.dumps(photos_res))
                            print(self.s.session.headers)
                    else:
                        self.debugger.Log("Failed to pass fields stage: "+json.dumps(field_res))
                else:
                    self.debugger.Log("Failed to send code to that email. exiting.")
                    sys.exit(0)
                
    def check_login(self, response, email, phone_number, store_auth_token):
        if 'loginResult' in response:
            self.refresh_token = response['loginResult']['refreshToken']
            self.userId = response['loginResult']['userId']
            self.authTokenExpires = response['loginResult']['authTokenTtl']
            self.s.session.headers["x-auth-token"] = response['loginResult']['authToken']
            self.s.session.headers["x-auth-token"] = response['loginResult']['authToken']
            logged_in_as = self.account.get_me()
            if store_auth_token:
                self.debugger.Log("Saved session data to file")
                self.util.saveToFile(f"{self.userId}.txt", f"userId: {self.userId}\nx-auth-token: {self.s.session.headers['x-auth-token']}\nrefreshToken: {self.refresh_token}\nEmail: {email}\nPhone: {phone_number}")
            return logged_in_as
        else:
            return False
    
    def browser_view(self):
        self.browser.start("https://tinder.com")
    
    def register(self, phone_number, email, fields, photo_path, store_account_data=True):
        """Registers a new account with a phone number & email provided

        Args:
            phone_number (str): The phone number to register the account with
            email (str): The email to register the account with
            fields (list): This is required to signup, it's basic information about the profile.
                  Example:
                        fields = [
                            {
                                "data": "1995-10-10",
                                "name": "birth_date"
                            },
                            {
                                "data": 0, MALE = 0 FEMALE = 1 (other gender shit i dont know find that out urself),
                                "name": "gender"
                            },
                            {
                                "data": False,
                                "name": "show_gender_on_profile"
                            },
                            {
                                "data": [0, 1] (male and female),
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
            profile_images (str): 1 image to upload, path to it.
            store_account_data (bool, optional): _description_. Defaults to True.
        """
        account_data = self.login(phone_number, email, False, registerFields=fields, photo_path=photo_path, store_auth_token=store_account_data)
        if store_account_data:
            with open("register_account_data", "w+") as f:
                f.write(json.dumps(account_data))
                f.close()
        
    def is_suspiscious(self):
        res = self.s.get("/healthcheck/auth", 1)
        if res["data"]["ok"]:
            return True
        else:
            return False
