from PyQt5.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QWidget
from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtCore import Qt

class LayerStatsWidgetPanel(QDockWidget):
    def __init__(self, iface):
        """Création du panneau dockable."""
        super().__init__("Layer Stats", iface.mainWindow())
        self.iface = iface
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Labels pour afficher les informations
        self.layer_name_label = QLabel("Nom de la couche : ")
        self.geometry_type_label = QLabel("Type de géométrie : ")
        self.feature_count_label = QLabel("Nombre d'entités : ")
        self.total_area_label = QLabel("Surface totale : ")
        self.total_length_label = QLabel("Longueur totale : ")
        self.crs_label = QLabel("Projection : ")

        # Ajout des labels au layout
        self.layout.addWidget(self.layer_name_label)
        self.layout.addWidget(self.geometry_type_label)
        self.layout.addWidget(self.feature_count_label)
        self.layout.addWidget(self.total_area_label)
        self.layout.addWidget(self.total_length_label)
        self.layout.addWidget(self.crs_label)

        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)

        # Connexion au changement de couche active
        self.iface.currentLayerChanged.connect(self.update_layer_stats)
        self.update_layer_stats()  # Mise à jour initiale

    # Fonction pour mettre à jour les statistiques de la couche active
    def update_layer_stats(self):
        """Mise à jour des statistiques de la couche active."""
        layer = self.iface.activeLayer()
        if not isinstance(layer, QgsVectorLayer):
            self.layer_name_label.setText("Nom de la couche : Aucune couche active")
            self.geometry_type_label.setText("Type de géométrie : -")
            self.feature_count_label.setText("Nombre d'entités : -")
            self.total_area_label.setText("Surface totale : -")
            self.total_length_label.setText("Longueur totale : -")
            self.crs_label.setText("Projection : -")
            return

        # Mise à jour des informations de la couche
        self.layer_name_label.setText(f"Nom de la couche : {layer.name()}")
        self.geometry_type_label.setText(f"Type de géométrie : {layer.geometryType()}")
        if layer.geometryType() == 0:
            self.geometry_type_label.setText("Type de géométrie : Point")
        elif layer.geometryType() == 1:
            self.geometry_type_label.setText("Type de géométrie : Ligne")
        elif layer.geometryType() == 2:
            self.geometry_type_label.setText("Type de géométrie : Polygone")
        else:
            self.geometry_type_label.setText("Type de géométrie : Autre")

        # Calcul des statistiques
        features = list(layer.getFeatures())
        self.feature_count_label.setText(f"Nombre d'entités : {len(features)}")

        if layer.geometryType() == 2:  # Polygones
            total_area = sum(f.geometry().area() for f in features)
            self.total_area_label.setText(f"Surface totale : {total_area:.2f}")
            self.total_length_label.setText("Longueur totale : N/A")
        elif layer.geometryType() == 1:  # Lignes
            total_length = sum(f.geometry().length() for f in features)
            self.total_length_label.setText(f"Longueur totale : {total_length:.2f}")
            self.total_area_label.setText("Surface totale : N/A")
        else:
            self.total_area_label.setText("Surface totale : N/A")
            self.total_length_label.setText("Longueur totale : N/A")
        if layer.crs().isValid():
            self.crs_label.setText(f"Projection : {layer.crs().authid()} ({layer.crs().description()})")
        else:
            self.crs_label.setText("Projection : Non définie")