from bs4 import BeautifulSoup
import requests

class ParserController:
    def __init__(self):
        self.certUrl = "http://www.cert.ssi.gouv.fr/"
        self.logs = {}
    
    def getLastAlert(self, timestamp):
        try:
            # recup du site
            headers = {"User-Agent": "Mozilla/5.0 (compatible; MyParser/1.0)"}
            response = requests.get(self.certUrl, headers=headers, timeout=5)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            # on get la première balise
            alert = soup.find("a", class_="c-li__link")

            if not alert:
                self.logs ["info"] = "null"

            title = alert.get_text(strip=True)
            href = alert.get("href")

            # sécurité si les urls sont non conformes
            if not href.startswith("http"):
                href = self.certUrl.rstrip("/") + href

            self.logs = {
                "date_parsed": timestamp,
                "title": title,
                "url": href
            }

        except requests.RequestException as e:
            print(f"[!] Network error : {e}")
            self.logs["info"] = f"error : {e}"

        return self.logs