import subprocess
import os

class SondeControl :

    def __init__(self):
        self.logs = {}
        self.dir = "/home/titiplex/ams/sondes/"

    def collectSysInfo(self, timestamp):
        try:

            self.logs["timestamp"] = timestamp

            for file in os.listdir(self.dir):
                path = os.path.join(self.dir, file)
                result = ""
                if os.path.isfile(path):
                    if file.endswith(".sh"):
                        result = subprocess.run(["bash", path], capture_output=True, text=True).stdout.strip()
                    else:
                        result = subprocess.run(["python3", path], capture_output=True, text=True).stdout.strip()
                else:
                    raise FileNotFoundError(f"File doesn't exist : {path}")
                self.logs[os.path.splitext(file)[0]] = result


        except Exception as e:
            print("Erreur lors de la collecte :", e)
            self.logs = {
                "timestamp": timestamp,
                "error": str(e)
            }

        return self.logs

    def printTerminal(self):
        print("### SondeControl ###")
        for cle, valeur in self.logs.items():
            print(f"{valeur}")
