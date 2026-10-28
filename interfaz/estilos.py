"""
Estilos y tema visual para la interfaz gráfica PyQt6.
Paleta: Minimalista Académico (Texto negro sobre fondo blanco puro, estilo hoja de papel).
Filosofía de diseño: Bordes completamente rectos (border-radius: 0px),
estética sobria, limpia y de máxima legibilidad técnica.
"""

from pathlib import Path

_DIR_ACTUAL = Path(__file__).resolve().parent
_ICONO_ARRIBA = (_DIR_ACTUAL / "iconos" / "flecha_arriba.svg").as_posix()
_ICONO_ABAJO = (_DIR_ACTUAL / "iconos" / "flecha_abajo.svg").as_posix()

TEMA_OSCURO = f"""
QMainWindow {{
    background-color: #F9FAFB; /* Fondo limpio claro */
}}

QWidget {{
    color: #111827;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    font-size: 13px;
}}

/* Tarjetas y Contenedores con bordes rectos */
QFrame[frameShape="1"], QFrame#cardFrame {{
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
}}

/* Etiquetas */
QLabel {{
    color: #111827;
}}

QLabel#titleLabel {{
    font-size: 21px;
    font-weight: 700;
    color: #111827;
    letter-spacing: 0.5px;
}}

QLabel#subtitleLabel {{
    font-size: 13px;
    color: #6B7280;
}}

/* Botones con bordes rectos */
QPushButton {{
    background-color: #F3F4F6;
    color: #111827;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
    padding: 7px 18px;
    font-weight: 600;
    min-height: 22px;
}}

QPushButton:hover {{
    background-color: #E5E7EB;
    border-color: #9CA3AF;
    color: #000000;
}}

QPushButton:pressed {{
    background-color: #D1D5DB;
}}

QPushButton:disabled {{
    background-color: #F9FAFB;
    color: #9CA3AF;
    border-color: #E5E7EB;
}}

/* Botón principal: Negro minimalista de alto contraste */
QPushButton#primaryButton {{
    background-color: #111827;
    color: #FFFFFF;
    border: 1px solid #000000;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 24px;
    border-radius: 0px;
}}

QPushButton#primaryButton:hover {{
    background-color: #000000;
    border-color: #000000;
}}

QPushButton#primaryButton:pressed {{
    background-color: #374151;
}}

/* Botones de navegación paso a paso */
QPushButton#btnNav {{
    background-color: #F3F4F6;
    color: #111827;
    border: 1.5px solid #111827;
    border-radius: 0px;
    padding: 7px 16px;
    font-weight: 700;
    font-size: 13px;
    min-height: 22px;
}}

QPushButton#btnNav:hover {{
    background-color: #111827;
    color: #FFFFFF;
    border-color: #111827;
}}

QPushButton#btnNav:pressed {{
    background-color: #374151;
    color: #FFFFFF;
}}

QPushButton#btnNav:disabled {{
    background-color: #F9FAFB;
    color: #9CA3AF;
    border: 1px solid #E5E7EB;
}}

/* Indicador del paso actual */
QLabel#stepLabel {{
    font-weight: 700;
    font-size: 13px;
    color: #111827;
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
    padding: 6px 12px;
}}

/* Botón Ver Todo / Paso a Paso */
QPushButton#btnVerTodo {{
    background-color: #FFFFFF;
    color: #4B5563;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 14px;
    min-height: 20px;
}}

QPushButton#btnVerTodo:hover {{
    background-color: #F3F4F6;
    color: #111827;
    border-color: #111827;
}}

QPushButton#btnVerTodo:pressed {{
    background-color: #E5E7EB;
}}

QPushButton#btnVerTodo:disabled {{
    background-color: #F9FAFB;
    color: #9CA3AF;
    border-color: #E5E7EB;
}}

/* SpinBox y Campos de Entrada con bordes rectos */
QSpinBox, QDoubleSpinBox, QLineEdit {{
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
    padding: 6px 10px;
    color: #111827;
    selection-background-color: #E5E7EB;
    selection-color: #000000;
}}

QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {{
    border: 1.5px solid #111827;
}}

/* Botones de flechas del SpinBox con bordes rectos */
QSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 24px;
    background-color: #F3F4F6;
    border-left: 1px solid #D1D5DB;
    border-bottom: 0.5px solid #D1D5DB;
    border-radius: 0px;
}}

QSpinBox::up-button:hover {{
    background-color: #E5E7EB;
}}

QSpinBox::up-button:pressed {{
    background-color: #D1D5DB;
}}

QSpinBox::up-arrow {{
    image: url('{_ICONO_ARRIBA}');
    width: 9px;
    height: 9px;
}}

QSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 24px;
    background-color: #F3F4F6;
    border-left: 1px solid #D1D5DB;
    border-top: 0.5px solid #D1D5DB;
    border-radius: 0px;
}}

QSpinBox::down-button:hover {{
    background-color: #E5E7EB;
}}

QSpinBox::down-button:pressed {{
    background-color: #D1D5DB;
}}

QSpinBox::down-arrow {{
    image: url('{_ICONO_ABAJO}');
    width: 9px;
    height: 9px;
}}

/* Tabla de la Matriz */
QTableWidget {{
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
    gridline-color: #E5E7EB;
    color: #111827;
    selection-background-color: #E5E7EB;
    selection-color: #000000;
}}

QTableWidget::item {{
    padding: 4px;
    border: 1px solid #E5E7EB;
}}

QTableWidget::item:focus {{
    background-color: #F3F4F6;
    border: 1.5px solid #111827;
}}

QHeaderView::section {{
    background-color: #F3F4F6;
    color: #111827;
    padding: 6px;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
    font-weight: 700;
    font-size: 12px;
}}

QHeaderView::section:horizontal {{
    border-top: none;
}}

QHeaderView::section:vertical {{
    border-left: none;
}}

QTableCornerButton::section {{
    background-color: #F3F4F6;
    border: 1px solid #D1D5DB;
    border-radius: 0px;
}}

/* Divisor (Splitter) limpio */
QSplitter::handle {{
    background-color: #E5E7EB;
    width: 4px;
}}

QSplitter::handle:hover {{
    background-color: #9CA3AF;
}}

/* Barra de estado */
QStatusBar {{
    background-color: #F9FAFB;
    color: #4B5563;
    border-top: 1px solid #E5E7EB;
    font-size: 12px;
}}

/* ScrollBar con bordes rectos */
QScrollBar:vertical {{
    border: none;
    background: #F9FAFB;
    width: 10px;
    margin: 0px;
    border-radius: 0px;
}}

QScrollBar::handle:vertical {{
    background: #D1D5DB;
    min-height: 20px;
    border-radius: 0px;
}}

QScrollBar::handle:vertical:hover {{
    background: #9CA3AF;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    border: none;
    background: #F9FAFB;
    height: 10px;
    margin: 0px;
    border-radius: 0px;
}}

QScrollBar::handle:horizontal {{
    background: #D1D5DB;
    min-width: 20px;
    border-radius: 0px;
}}

QScrollBar::handle:horizontal:hover {{
    background: #9CA3AF;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""
