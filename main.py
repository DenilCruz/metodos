import sys
from PyQt6.QtWidgets import QApplication

from interfaz.ventana_principal import VentanaPrincipal
from interfaz.estilos import TEMA_OSCURO


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(TEMA_OSCURO)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
