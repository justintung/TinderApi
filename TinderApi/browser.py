from playwright.sync_api import sync_playwright
import time

class Browser:
    def __init__(self, api):
        self.api = api
        
    def start(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            script = self.script()
            time.sleep(3)
            page.evaluate(script)
            time.sleep(10)
            page.pause()
    
    def script(self):
        return """
                let db = window.indexedDB.open("keyval-store", 1)
                db.onsuccess = (event) => {
                    setTimeout(() => {
                        let result = event.target.result;
                        console.log(result)
                        let transaction = result.transaction(["keyval"], "readwrite")
                        let obj_store = transaction.objectStore("keyval")
                        obj_store.put('{\"authToken\":\""""+self.api.s.session.headers['x-auth-token']+"""\",\"authTokenExpiration\":1991729274973,\"captchaType\":\"CAPTCHA_INVALID\",\"funnelSessionId\":\""""+self.api.s.session.headers["funnel-session-id"]+"""\",\"guestAuthToken\":\"\",\"loginType\":\"sms\",\"onboardingUserId\":null,\"refreshToken\":\""""+self.api.refresh_token+"""\",\"__PERSIST__\":{\"version\":0,\"timestamp\":1991729274973}}', "persist::mfa")
                        obj_store.put('{\"loggedIn\":true,\"__PERSIST__\":{\"version\":2,\"timestamp\":1991729274973}}', "persist::user")
                        localStorage.setItem("TinderWeb/APIToken", '"""+self.api.s.session.headers["x-auth-token"]+"""')
                        console.log(localStorage.getItem("TinderWeb/APIToken"))
                        location.reload()
                    }, 3000)
                }
        """