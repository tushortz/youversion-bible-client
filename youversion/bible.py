import requests

class Bible:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = self.get_session(username, password)

    def get_session(self, username, password):
        session = requests.Session()
        session.auth = (username, password)
        session.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "content-type": "application/json; charset=utf-8"
        }

        session.post(self.get_url("login"), params={"username": username, "password": password})

        return session

    def get_url(self, url):
        home = "https://my.bible.com"
        urls = {
            "login":   "sign-in",
            "moments": "moments/_cards.json"
        }

        return_url = "{}/{}".format(home, urls.get(url))
        return return_url

    def moments(self, page=1):
        params = {"page": page}

        response = self.session.get(self.get_url("moments"), params=params)
        
        return response.json()
