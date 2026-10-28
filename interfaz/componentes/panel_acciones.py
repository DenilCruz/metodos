"""
Barra de herramientas y acciones de control para la calculadora.
Cumple con el Principio de Responsabilidad Única (SRP).
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import pyqtSignal


class PanelAcciones(QWidget):
    """
    Widget con botones de acción:
    - Limpiar todas las celdas.
    - Botón principal para resolver.
    """
    limpiar_solicitado = pyqtSignal()
    calcular_solicitado = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._iniciar_interfaz()

    def _iniciar_interfaz(self):
        diseno = QHBoxLayout(self)
        diseno.setContentsMargins(14, 4, 14, 14)
        diseno.setSpacing(10)

        # Botón para limpiar celdas a la izquierda
        self.boton_limpiar = QPushButton("Limpiar Celdas")
        self.boton_limpiar.setToolTip("Limpia todas las celdas dejándolas vacías")
        self.boton_limpiar.clicked.connect(self.limpiar_solicitado.emit)
        diseno.addWidget(self.boton_limpiar)

        diseno.addStretch()

        # Botón principal de cálculo destacado a la derecha
        self.boton_calcular = QPushButton("Resolver")
        self.boton_calcular.setObjectName("primaryButton")
        self.boton_calcular.clicked.connect(self.calcular_solicitado.emit)
        diseno.addWidget(self.boton_calcular)
