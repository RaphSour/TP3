#Importation des plugin nécessaires pour le plugin
from PyQt5.QtWidgets import QAction, QDockWidget
from qgis.PyQt.QtCore import Qt
from .LayerStatsWidget import LayerStatsWidgetPanel

#Création de la classe LayerStatsWidget
class LayerStatsWidget:
    def __init__(self, iface):
        """Initialisation du plugin."""
        self.iface = iface
        self.dock_widget = None

    def initGui(self):
        """Création de l’interface utilisateur du plugin."""
        self.action = QAction("Layer Stats Widget", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("LayerStatsWidget", self.action)

    def unload(self):
        """Suppression du plugin."""
        self.iface.removePluginMenu("LayerStatsWidget", self.action)

    def run(self):
        """Affichage du widget."""
        if not self.dock_widget:
            self.dock_widget = LayerStatsWidgetPanel(self.iface)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.show()
        