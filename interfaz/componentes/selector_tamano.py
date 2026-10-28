"""
Componente para la selección de dimensiones de la matriz.
Cumple con el Principio de Responsabilidad Única (SRP).
Permite ingresar directamente un único número n para definir la matriz cuadrada n x n.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSpinBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal


class SelectorTamano(QWidget):
    """
    Widget especializado en permitir al usuario ingresar directamente
    el número n para la dimensión de la matriz cuadrada (n x n).
    """
    tamano_cambiado = pyqtSignal(int)

    def __init__(self, tamano_inicial: int = 3, tamano_min: int = 2, tamano_max: int = 20, parent=None):
        super().__init__(parent)
        self._tamano_min = tamano_min
        self._tamano_max = tamano_max
        self._tamano_actual = tamano_inicial
        self._iniciar_interfaz()

    def _iniciar_interfaz(self):
        diseno = QHBoxLayout(self)
        diseno.setContentsMargins(14, 6, 14, 6)
        diseno.setSpacing(12)

        tarjeta = QFrame()
        tarjeta.setObjectName("cardFrame")
        diseno_tarjeta = QHBoxLayout(tarjeta)
        diseno_tarjeta.setContentsMargins(16, 10, 16, 10)
        diseno_tarjeta.setSpacing(12)

        etiqueta_titulo = QLabel("Dimensión de la matriz:")
        etiqueta_titulo.setStyleSheet("font-weight: 600; font-size: 13px; color: #111827;")
        diseno_tarjeta.addWidget(etiqueta_titulo)

        # Entrada numérica directa sin sufijos molestos
        self.selector_spin = QSpinBox()
        self.selector_spin.setRange(self._tamano_min, self._tamano_max)
        self.selector_spin.setValue(self._tamano_actual)
        self.selector_spin.setFixedWidth(80)
        self.selector_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selector_spin.valueChanged.connect(self._al_cambiar_spin)
        diseno_tarjeta.addWidget(self.selector_spin)

        diseno_tarjeta.addStretch()
        diseno.addWidget(tarjeta)

    def _al_cambiar_spin(self, valor: int):
        self._tamano_actual = valor
        self.tamano_cambiado.emit(valor)

    def asignar_tamano(self, tamano: int):
        if self._tamano_min <= tamano <= self._tamano_max:
            self.selector_spin.setValue(tamano)

    @property
    def tamano_actual(self) -> int:
        return self._tamano_actual
