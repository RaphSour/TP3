from PyQt5.QtWidgets import (
    QDockWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QComboBox,
    QCheckBox, QPushButton, QFileDialog
)
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeatureRequest, QgsGeometry
)
from qgis.utils import iface
import csv

class LayerStatsComparatorDockWidget(QDockWidget):
    def __init__(self, iface):
        super().__init__("Layer Stats Comparator", iface.mainWindow())
        self.iface = iface

        # Interface principale
        self.main_widget = QWidget()
        self.setWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Sélecteurs de couches
        self.layer1_combo = QComboBox()
        self.layer2_combo = QComboBox()
        self.extent_checkbox = QCheckBox("Limiter à la zone visible de la carte")

        self.layout.addWidget(QLabel("Couche A :"))
        self.layout.addWidget(self.layer1_combo)
        self.layout.addWidget(QLabel("Couche B :"))
        self.layout.addWidget(self.layer2_combo)
        self.layout.addWidget(self.extent_checkbox)

        # Stats affichées
        self.stats_label = QLabel("Statistiques comparées ici")
        self.layout.addWidget(self.stats_label)

        # Bouton export CSV
        self.export_button = QPushButton("Exporter les statistiques en CSV")
        self.layout.addWidget(self.export_button)

        # Connexions
        self.layer1_combo.currentIndexChanged.connect(self.update_stats)
        self.layer2_combo.currentIndexChanged.connect(self.update_stats)
        self.extent_checkbox.stateChanged.connect(self.update_stats)
        self.export_button.clicked.connect(self.export_stats_to_csv)
        self.iface.mapCanvas().extentsChanged.connect(self.update_stats)

        self.populate_layer_combos()
        self.update_stats()

    def populate_layer_combos(self):
        self.layer1_combo.clear()
        self.layer2_combo.clear()
        self.vector_layers = [layer for layer in QgsProject.instance().mapLayers().values() if isinstance(layer, QgsVectorLayer)]
        for layer in self.vector_layers:
            self.layer1_combo.addItem(layer.name(), layer)
            self.layer2_combo.addItem(layer.name(), layer)

    def get_features(self, layer):
        if self.extent_checkbox.isChecked():
            extent = self.iface.mapCanvas().extent()
            request = QgsFeatureRequest().setFilterRect(extent)
            return list(layer.getFeatures(request))
        else:
            return list(layer.getFeatures())

    def compute_stats(self, layer, features):
        geom_type = layer.geometryType()
        count = len(features)
        total_area = sum(f.geometry().area() for f in features) if geom_type == 2 else None
        total_length = sum(f.geometry().length() for f in features) if geom_type == 1 else None
        return count, total_area, total_length

    def update_stats(self):
        try:
            layer1 = self.layer1_combo.currentData()
            layer2 = self.layer2_combo.currentData()
            if not layer1 or not layer2:
                self.stats_label.setText("Veuillez sélectionner deux couches.")
                return

            features1 = self.get_features(layer1)
            features2 = self.get_features(layer2)

            stats1 = self.compute_stats(layer1, features1)
            stats2 = self.compute_stats(layer2, features2)

            text = f"<b>{layer1.name()}</b> vs <b>{layer2.name()}</b><br>"
            text += f"Nombre d'entités : {stats1[0]} vs {stats2[0]}<br>"

            if layer1.geometryType() == 2 and stats1[1] is not None:
                text += f"Surface totale : {stats1[1]:.2f} vs {stats2[1]:.2f}<br>"
            elif layer1.geometryType() == 1 and stats1[2] is not None:
                text += f"Longueur totale : {stats1[2]:.2f} vs {stats2[2]:.2f}<br>"

            self.stats_label.setText(text)
        except Exception as e:
            self.stats_label.setText(f"Erreur : {str(e)}")

    def export_stats_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer les statistiques", "", "CSV Files (*.csv)")
        if not file_path:
            return

        layer1 = self.layer1_combo.currentData()
        layer2 = self.layer2_combo.currentData()
        features1 = self.get_features(layer1)
        features2 = self.get_features(layer2)
        stats1 = self.compute_stats(layer1, features1)
        stats2 = self.compute_stats(layer2, features2)
        extent = self.iface.mapCanvas().extent()

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Statistique", layer1.name(), layer2.name()])
            writer.writerow(["Nombre d'entités", stats1[0], stats2[0]])
            if layer1.geometryType() == 2:
                writer.writerow(["Surface totale", stats1[1], stats2[1]])
            elif layer1.geometryType() == 1:
                writer.writerow(["Longueur totale", stats1[2], stats2[2]])
            writer.writerow([])
            writer.writerow(["Étendue visible (xmin, ymin, xmax, ymax)"])
            writer.writerow([extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()])


# Écriture dans le fichier widget.py
widget_file_path = os.path.join("/mnt/data/LayerStatsComparator", "widget.py")
with open(widget_file_path, "w", encoding="utf-8") as f:
    f.write(widget_code)

widget_file_path  # Affiche le chemin du fichier mis à jour