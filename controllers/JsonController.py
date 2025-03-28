import os
import json
import datetime

class JsonController:
    def __init__(self, dirname, timestamp):
        self.dirname=dirname
        self.logs={}

    def printLogs(self, filename, dictionary):
        data = []
        path = os.path.join(self.dirname, filename)

        # existe and not null
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, "r") as f:
                try:
                    data = json.load(f)

                    # dic vers liste
                    if isinstance(data, dict):
                        data = [data]

                    # Sréinit
                    elif not isinstance(data, list):
                        print(f"Format inattendu dans {path}, remplacement...")
                        data = []

                except json.JSONDecodeError:
                    print(f"Fichier {path} invalide ou vide, réinitialisation...")
                    data = []

        # ajout log
        data.append(dictionary)

        # save
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def printTerminal(self, head):
        print(head)
        for cle, valeur in self.logs.items():
            print(f"{valeur}")

    def clean(self, timestamp, daynumber):
        # La limite (ici 7 jours)
        limite = datetime.datetime.now() - datetime.timedelta(days=daynumber)

        # itérations sur les fichiers du dossier
        for file in os.listdir(self.dirname):
            path = os.path.join(self.dirname, file)

            # on vérifie que ça soit bien json
            if os.path.isfile(path) and path.endswith(".json"):
                try:
                    # nom du fichier sans extension
                    filename = os.path.splitext(file)[0]
                    # transforme en date
                    datefile = datetime.datetime.fromisoformat(filename)

                    # condition pour nettoyage
                    if datefile < limite:
                        os.remove(path)
                        self.logs["file-change"] = {
                            "timestamp": timestamp,
                            "removed": path
                        }
                    else:
                        self.logs["state"] = "no changes"
                except Exception as e:
                    print("Erreur lors de la collecte :", e)
                    self.logs["error"] = {
                        "timestamp": timestamp,
                        "error": str(e)
                    }
    
    def exists(self, key, value):
        for file in os.listdir(self.dirname):
            path = os.path.join(self.dirname, file)

            if os.path.isfile(path) and file.endswith(".json"):
                try:
                    with open(path, "r") as f:
                        data = json.load(f)

                        if isinstance(data, dict):
                            if key in data:
                                if data[key] == value:
                                    return True
                                else: return False
                            else:
                                raise KeyError(f"Key {key} doesn't exist in {path}")
                        else:
                            raise TypeError(f"file {path} is not correctly formatted to json")
                except json.JSONDecodeError as e:
                    print(f"Invalide Json : " + e)