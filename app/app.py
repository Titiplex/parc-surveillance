# app/app.py
import os, sys, json, glob
sys.path.insert(0, os.path.abspath(os.path.join(__file__,"..","..")))

from flask import Flask, Response, abort, render_template, jsonify
from controllers.GraphController import GraphController

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Dossier des sondes pour récupérer leur nom
SONDES_DIR = "/home/titiplex/ams/sondes/"
# Dossier des logs pour extraire la liste de machines
LOGS_DIR   = "/home/titiplex/ams/logs/sondesLogs/"

@app.route("/api/sondes")
def api_sondes():
    sondes = sorted([
        os.path.splitext(f)[0]
        for f in os.listdir(SONDES_DIR)
        if f.endswith((".py", ".sh")) and not f.startswith("machineName")
    ])
    return jsonify(sondes)

@app.route("/api/machines")
def api_machines():
    machines = set()
    for fname in os.listdir(LOGS_DIR):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(LOGS_DIR, fname)
        try:
            with open(path) as f:
                data = json.load(f)
                if isinstance(data, dict):
                    L = [data]
                else:
                    L = data
            for rec in L:
                m = rec.get("machineName")
                if m:
                    machines.add(m)
        except:
            pass
    return jsonify(sorted(machines))

@app.route("/api/svg/<sonde>/<machine>")
def api_svg(sonde, machine):
    # Vérifier qu'on a bien les deux choix
    gc = GraphController(sonde, machine)
    svg = gc.render_svg_string()
    if not svg:
        abort(404)
    return Response(svg, mimetype="image/svg+xml")

def fix_double_encoding(s: str) -> str:
    try:
        # On prend la chaîne Python (où chaque caractère <256 est en fait un octet Latin-1)
        # on l'encode en bytes Latin-1, puis on la décode en UTF-8
        return s.encode("latin-1").decode("utf-8")
    except Exception:
        return s  # si ça plante, on renvoie la chaîne brute

CERT_DIR = "/home/titiplex/ams/logs/certLogs"

@app.route("/api/cert_logs")
def api_cert_logs():
    """Renvoie toutes les alertes CERT triées par date_parsed croissante."""
    all_alerts = []
    # on parcours tous les .json de CERT, par ex 2025.json
    for path in sorted(glob.glob(os.path.join(CERT_DIR, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # chaque fichier contient soit un dict, soit une liste
                if isinstance(data, dict):
                    all_alerts.append(data)
                elif isinstance(data, list):
                    all_alerts.extend(data)
        except Exception as e:
            print(f"[!] Erreur lecture CERT {path}: {e}")
    # trier par date_parsed
    try:
        all_alerts.sort(key=lambda x: x.get("date_parsed", ""))
    except Exception:
        pass
    
    for alert in all_alerts:
        if "title" in alert:
            alert["title"] = fix_double_encoding(alert["title"])
    return jsonify(all_alerts)

@app.route("/")
def index():
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
