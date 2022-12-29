import requests
import json
import urllib.parse
import re

#basic auth token -> komoot-ios-3njbbl:ia6ui8gahxo1oowaegha5nua1
host = "https://api.komoot.de"
auth = "https://auth-api.main.komoot.net/oauth/token"

class komoot(object):

    def __init__(self) -> None:
        self.session = requests.session()

    def login(self,user,password):
        payload = f"grant_type=password&password={password}&scope=user.%2A&username={urllib.parse.quote(user)}"
        headers = {
          'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
          'authorization': 'Basic a29tb290LWlvcy0zbmpiYmw6aWE2dWk4Z2FoeG8xb293YWVnaGE1bnVhMQ==',
        }
        try:
            self.r = self.session.request("POST", auth, headers=headers, data=payload)
            if self.r.status_code==200:
                # Login successful
                self.login = self.r.json()
                self.r = True
            else:
                # Login failed
                self.r = False
        except:
            # Login failed
            self.r = False
        return(self.r)

    def get_all_tours_id(self):
        url = f"{host}v007/users/{self.login.get('username')}/tours/"
        headers = {
        'host': 'api.komoot.de',
        'authorization': f"Bearer {self.login.get('access_token')}"
        }
        self.tours = requests.request("GET", url, headers=headers).json()
        self.tours_id_recorded = [e.get('id') for e in self.tours.get('_embedded').get('tours') if e.get('type')=='tour_recorded']
        return(self.tours_id_recorded)

    def download_tour_gpx(self,tour_id):
        url = f"{host}v007/tours/{tour_id}.gpx"
        headers = {
        'host': 'api.komoot.de',
        'authorization': f"Bearer {self.login.get('access_token')}"
        }
        return(requests.request("GET", url, headers=headers).text)
    
    def get_combined_gpx(self,tour_ids):
        r = [re.findall(r"((?=<trkseg>).*(?<=</trkseg>))",self.download_tour_gpx(e), re.MULTILINE | re.DOTALL) for e in tour_ids]
        trkseg = ''.join([e[0] for e in r])
        str = """<?xml version='1.0' encoding='UTF-8'?><gpx version="1.1" creator="https://www.komoot.de" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">  <metadata>    <name>name</name>    <author>      <link href="https://www.komoot.de">        <text>komoot</text>        <type>text/html</type>      </link>    </author>  </metadata>  <trk>"""+trkseg+"""</trk></gpx>"""
        with open("all_maps_done.gpx", "w") as f:
            f.write(str)


# just used as an example
# delete this if you want to use the komoot class externally
if __name__ == '__main__':
    komoot = komoot()
    komoot.login('your@ma.il','password')
    komoot.get_combined_gpx(komoot.get_all_tours_id())