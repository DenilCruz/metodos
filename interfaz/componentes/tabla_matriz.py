"""
Componente para la visualización, edición y extracción de los datos de la matriz A y el vector b.
Siempre incluye el vector de términos independientes b.
"""

from typing import List, Dict, Tuple
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QBrush

from logica.matriz import Matriz, Vector


class TablaMatriz(QWidget):
    """
    Tabla interactiva de edición matricial que soporta:
    - Redimensionamiento dinámico (conservando valores previos).
    - Columna de términos independientes b siempre presente y destacada.
    - Validación y conversión limpia a modelos de dominio Matriz y Vector.
    """

    def __init__(self, tamano: int = 3, parent=None):
        super().__init__(parent)
        self._tamano = tamano
        self._iniciar_interfaz()
        self.actualizar_dimensiones(self._tamano)

    def _iniciar_interfaz(self):
        diseno = QVBoxLayout(self)
        diseno.setContentsMargins(14, 0, 14, 10)
        diseno.setSpacing(6)

        self.tabla = QTableWidget()
        self.tabla.setObjectName("matrixTable")
        self.tabla.setAlternatingRowColors(False)
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        
        # Ajustes de encabezados
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.verticalHeader().setDefaultSectionSize(46)

        diseno.addWidget(self.tabla)

    def actualizar_dimensiones(self, nuevo_tamano: int):
        """
        Ajusta la cantidad de filas y columnas (n filas x (n + 1) columnas para A y b)
        manteniendo los datos ya ingresados.
        """
        datos_guardados = self._leer_celdas_texto()
        self._tamano = nuevo_tamano
        total_columnas = nuevo_tamano + 1  # Siempre n columnas de A + 1 columna de b

        self.tabla.setRowCount(nuevo_tamano)
        self.tabla.setColumnCount(total_columnas)

        # Encabezados de columnas (x1, x2, x3... y Vector b)
        encabezados_cols: List[str] = [f"x{j + 1}" for j in range(nuevo_tamano)]
        encabezados_cols.append("Vector b")

        self.tabla.setHorizontalHeaderLabels(encabezados_cols)

        # Encabezados de filas
        encabezados_filas = [f"Fila {i + 1}" for i in range(nuevo_tamano)]
        self.tabla.setVerticalHeaderLabels(encabezados_filas)

        fuente = QFont("Consolas, 'Courier New', monospace", 11)
        fuente.setBold(True)

        for i in range(nuevo_tamano):
            for j in range(total_columnas):
                es_columna_vector = (j == nuevo_tamano)
                texto_valor = datos_guardados.get((i, j), "")
                
                item = QTableWidgetItem(texto_valor)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFont(fuente)

                if es_columna_vector:
                    # Columna de términos independientes b en gris tenue limpio
                    item.setBackground(QBrush(QColor(243, 244, 246)))
                    item.setForeground(QBrush(QColor(0, 0, 0)))
                else:
                    item.setForeground(QBrush(QColor(0, 0, 0)))
                    if i == j:
                        item.setBackground(QBrush(QColor(250, 250, 250)))
                    else:
                        item.setBackground(QBrush(QColor(255, 255, 255)))

                self.tabla.setItem(i, j, item)

    def _leer_celdas_texto(self) -> Dict[Tuple[int, int], str]:
        """Lee el texto en crudo de todas las celdas actuales."""
        datos = {}
        for i in range(self.tabla.rowCount()):
            for j in range(self.tabla.columnCount()):
                item = self.tabla.item(i, j)
                if item and item.text().strip():
                    datos[(i, j)] = item.text().strip()
        return datos

    def obtener_matriz_a(self) -> Matriz:
        """
        Extrae y valida la matriz cuadrada A desde la tabla.
        Lanza ValueError si algún dato no es numérico o está vacío.
        """
        n = self._tamano
        filas_matriz: List[List[float]] = []

        for i in range(n):
            valores_fila: List[float] = []
            for j in range(n):
                item = self.tabla.item(i, j)
                texto = item.text().strip() if item else ""
                if not texto:
                    raise ValueError(f"La celda de la Matriz A en [Fila {i + 1}, Columna {j + 1}] está vacía.")
                try:
                    valor = float(texto.replace(",", "."))
                    valores_fila.append(valor)
                except ValueError:
                    raise ValueError(
                        f"Valor inválido '{texto}' en [Fila {i + 1}, Columna {j + 1}]. Ingrese un número válido."
                    )
            filas_matriz.append(valores_fila)

        return Matriz.desde_lista_2d(filas_matriz)

    def obtener_vector_b(self) -> Vector:
        """
        Extrae el vector de términos independientes b.
        Lanza ValueError si algún dato no es numérico o está vacío.
        """
        n = self._tamano
        col_b = n
        valores_b: List[float] = []

        for i in range(n):
            item = self.tabla.item(i, col_b)
            texto = item.text().strip() if item else ""
            if not texto:
                raise ValueError(f"La celda de Términos Independientes (b) en la Fila {i + 1} está vacía.")
            try:
                valor = float(texto.replace(",", "."))
                valores_b.append(valor)
            except ValueError:
                raise ValueError(
                    f"Valor inválido '{texto}' en Términos Independientes (b), Fila {i + 1}. Ingrese un número válido."
                )

        return Vector.desde_lista(valores_b)

    def asignar_matriz_a(self, matriz: Matriz):
        """Carga una matriz en las celdas de A."""
        if matriz.filas != self._tamano or matriz.columnas != self._tamano:
            self.actualizar_dimensiones(matriz.filas)
        for i in range(matriz.filas):
            for j in range(matriz.columnas):
                item = self.tabla.item(i, j)
                if item:
                    item.setText(f"{matriz.obtener(i, j):g}")

    def asignar_vector_b(self, vector: Vector):
        """Carga el vector b en la columna correspondiente."""
        col_b = self._tamano
        for i in range(min(self._tamano, vector.tamano)):
            item = self.tabla.item(i, col_b)
            if item:
                item.setText(f"{vector.obtener(i):g}")

    def limpiar_todo(self):
        """Limpia el texto de todas las celdas dejándolas vacías."""
        for i in range(self.tabla.rowCount()):
            for j in range(self.tabla.columnCount()):
                item = self.tabla.item(i, j)
                if item:
                    item.setText("")

    @property
    def tamano_matriz(self) -> int:
        return self._tamano
