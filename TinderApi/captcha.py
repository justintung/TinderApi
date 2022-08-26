import requests
import time

class Captcha():
    def __init__(self, key) -> None:
        self.api_key = key
        self.api_url = "http://2captcha.com/res.php"
        self.solve_url = "http://2captcha.com/in.php"
        try:
            self.balance = float(self.getBalance())
        except:
            skip_captcha = True
            
    def checkForResponse(self, captcha_id) -> str:
        req = requests.get(self.api_url+f"?key={self.api_key}&action=get&id={captcha_id}").text
        if req == "CAPCHA_NOT_READY" or req == "ERROR_CAPTCHA_UNSOLVABLE":
            return False
        else:
            return req

    def report_captcha(self, captcha_id):
        requests.post(f"http://2captcha.com/res.php?key={self.api_key}&action=reportbad&id={captcha_id}")
    
    def getBalance(self):
        return requests.get(self.api_url+f"?key={self.api_key}&action=getbalance").text

    def solve(self, method, site, params=""):
        req = requests.post(self.solve_url+f"?key={self.api_key}&method={method}&pageurl={site}&json=1"+params).json()
        for i in range(15):
            gotResponse = self.checkForResponse(req["request"])
            if gotResponse:
                if gotResponse.startswith("OK"):
                    return gotResponse.split("OK|")[1]
                else:
                    self.report_captcha(req["request"])
                    return False
            time.sleep(10)
        self.report_captcha(req["request"])
        return False