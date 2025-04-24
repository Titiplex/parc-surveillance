# controllers/GraphController.py
import pygal, os, json
from datetime import datetime

class GraphController:
    def __init__(self, sonde_name: str, machine_name: str,
                 folder_path: str = "/home/titiplex/ams/logs/sondesLogs"):
        self.sonde_name   = sonde_name
        self.machine_name = machine_name
        self.folder_path  = folder_path
        self.data = self.load_sonde_data()

    def load_sonde_data(self):
        data = []
        for fname in sorted(os.listdir(self.folder_path)):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(self.folder_path, fname)
            try:
                with open(path, "r") as f:
                    records = json.load(f)
                if isinstance(records, dict):
                    records = [records]
                for rec in records:
                    # Filtrer sur la machine
                    if rec.get("machineName") != self.machine_name:
                        continue
                    ts = rec.get("timestamp")
                    val = rec.get(self.sonde_name)
                    if ts and val is not None:
                        try:
                            dt = datetime.fromisoformat(ts)
                            nv = float(val)
                            data.append((dt, nv))
                        except Exception:
                            pass
            except Exception as e:
                print(f"[!] Erreur lecture {path}: {e}")
        return data

    def render_svg_string(self) -> str:
        if not self.data:
            return "<svg><!-- no data --></svg>"

        chart = pygal.Line(x_label_rotation=25, width=800, height=400)
        chart.title = (f"Machine {self.machine_name} – {self.sonde_name}")

        labels = [dt.strftime("%d/%m %H:%M") for dt, _ in self.data]
        step   = max(1, len(labels)//10)
        chart.x_labels       = labels
        chart.x_labels_major = labels[::step]
        chart.show_minor_x_labels = False

        series = [v for _, v in self.data]
        chart.add(self.sonde_name, series)
        return chart.render().decode("utf-8")
