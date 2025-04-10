import pygal, os, json
from datetime import datetime


class GraphController:
    def load_sonde_data(self, sonde_name: str):
        data = []

        for file in sorted(os.listdir(self.folder_path)):
            if file.endswith(".json"):
                full_path = os.path.join(self.folder_path, file)
                try:
                    with open(full_path, "r") as f:
                        records = json.load(f)
                        if isinstance(records, dict):
                            records = [records]
                        for record in records:
                            timestamp = record.get("timestamp")
                            value = record.get(sonde_name)
                            if timestamp and value:
                                try:
                                    value = float(value)
                                    dt = datetime.fromisoformat(timestamp)
                                    data.append((dt, value))
                                except ValueError:
                                    continue
                except Exception as e:
                    print(f"[!] Erreur lecture {file} : {e}")
        self.data = data
        return data

    def __init__(self, sonde_name: str):
        self.sonde_name = sonde_name
        self.folder_path = "/home/titiplex/ams/logs/sondesLogs"
        self.data = self.load_sonde_data(self.sonde_name)

    def generate_svg_graph(self, output_path: str):
        chart = pygal.Line(x_label_rotation=25)
        chart.title = f"Evolution de la sonde '{self.sonde_name}'"

        chart.x_labels = [dt.strftime("%d/%m %H:%M") for dt, _ in self.data]
        # label/jour
        chart.x_labels_major = [dt.strftime("%d/%m %H:%M") for i, (dt, _) in enumerate(self.data) if dt.hour == 0 and dt.minute == 0]
        chart.show_minor_x_labels = True

        chart.add(self.sonde_name, [value for _, value in self.data])
        chart.render_to_file(output_path)
        print(f"### Graph generated ###\r\n {output_path}")