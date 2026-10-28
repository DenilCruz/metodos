"""
Ventana principal de la Calculadora de Cholesky.
Cumple con el Principio de Responsabilidad Única (SRP) coordinando las vistas y componentes.
Integra la entrada de la matriz y el desarrollo paso a paso en una sola ventana (sin ventanas emergentes).
"""

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parent.parent
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QMessageBox, QFrame, QStatusBar, QSplitter, QTextBrowser
)
from PyQt6.QtCore import Qt, QTimer

from logica.matriz import Matriz, Vector
from logica.cholesky import ServicioCholesky
from interfaz.componentes.selector_tamano import SelectorTamano
from interfaz.componentes.tabla_matriz import TablaMatriz
from interfaz.componentes.panel_acciones import PanelAcciones
from interfaz.generador_html_cholesky import (
    obtener_pasos_html,
    generar_html_solucion,
    envolver_html_paso
)


class VentanaPrincipal(QMainWindow):
    """
    Ventana principal con panel dividido (Splitter):
    - Panel izquierdo: Entrada de datos (selector de dimensión, tabla de coeficientes y botones).
    - Panel derecho: Visor integrado del desarrollo paso a paso (sin ventanas adicionales).
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora del Método de Cholesky • Métodos Numéricos")
        self.resize(1120, 720)
        self.setMinimumSize(850, 550)
        
        self._servicio = ServicioCholesky()
        self._resultado_actual = None
        self._pasos = []
        self._indice_paso_actual = 0
        self._modo_ver_todo = False

        self._iniciar_interfaz()
        self._conectar_senales()
        self._mostrar_mensaje_inicial_resultados()

    def _iniciar_interfaz(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        diseno_principal = QVBoxLayout(widget_central)
        diseno_principal.setContentsMargins(16, 14, 16, 14)
        diseno_principal.setSpacing(10)

        # Divisor horizontal para entrada y resultados lado a lado
        self.divisor = QSplitter(Qt.Orientation.Horizontal)
        self.divisor.setChildrenCollapsible(False)

        # -------------------------------------------------------------
        # PANEL IZQUIERDO: Controles y Entrada de Datos
        # -------------------------------------------------------------
        panel_izquierdo = QWidget()
        diseno_izquierdo = QVBoxLayout(panel_izquierdo)
        diseno_izquierdo.setContentsMargins(0, 0, 8, 0)
        diseno_izquierdo.setSpacing(10)

        # Título
        titulo = QLabel("Metodo de Cholesky")
        titulo.setObjectName("titleLabel")
        diseno_izquierdo.addWidget(titulo)

        # Selector de dimensión
        self.selector_tamano = SelectorTamano(tamano_inicial=3, tamano_min=2, tamano_max=20)
        diseno_izquierdo.addWidget(self.selector_tamano)

        # Contenedor de la tabla
        contenedor_tabla = QFrame()
        contenedor_tabla.setObjectName("cardFrame")
        diseno_tabla = QVBoxLayout(contenedor_tabla)
        diseno_tabla.setContentsMargins(12, 12, 12, 8)
        diseno_tabla.setSpacing(8)

        titulo_tabla = QLabel("Matriz de Coeficientes  A  y  Términos Independientes  b")
        titulo_tabla.setStyleSheet("font-weight: 700; font-size: 13px; color: #111827;")
        diseno_tabla.addWidget(titulo_tabla)

        self.tabla_matriz = TablaMatriz(tamano=3)
        diseno_tabla.addWidget(self.tabla_matriz)
        diseno_izquierdo.addWidget(contenedor_tabla, stretch=1)

        # Panel de acciones (Limpiar y Resolver)
        self.panel_acciones = PanelAcciones()
        diseno_izquierdo.addWidget(self.panel_acciones)

        self.divisor.addWidget(panel_izquierdo)

        # -------------------------------------------------------------
        # PANEL DERECHO: Visor Integrado de Resultados Paso a Paso
        # -------------------------------------------------------------
        panel_derecho = QFrame()
        panel_derecho.setObjectName("cardFrame")
        diseno_derecho = QVBoxLayout(panel_derecho)
        diseno_derecho.setContentsMargins(14, 14, 14, 14)
        diseno_derecho.setSpacing(10)

        # Fila superior de cabecera: Título y opción de Ver Todo
        fila_cabecera = QHBoxLayout()
        fila_cabecera.setContentsMargins(0, 0, 0, 0)

        titulo_resultados = QLabel("Desarrollo Paso a Paso")
        titulo_resultados.setStyleSheet("font-weight: 700; font-size: 15px; color: #111827;")
        fila_cabecera.addWidget(titulo_resultados)

        fila_cabecera.addStretch()

        self.boton_ver_todo = QPushButton("Ver Todo")
        self.boton_ver_todo.setObjectName("btnVerTodo")
        self.boton_ver_todo.setMinimumWidth(105)
        self.boton_ver_todo.setToolTip("Alternar entre visualización paso a paso o desarrollo continuo")
        fila_cabecera.addWidget(self.boton_ver_todo)

        diseno_derecho.addLayout(fila_cabecera)

        # Barra de control paso a paso (Botón Anterior, Indicador de Paso, Botón Siguiente)
        contenedor_nav = QFrame()
        diseno_nav = QHBoxLayout(contenedor_nav)
        diseno_nav.setContentsMargins(0, 0, 0, 0)
        diseno_nav.setSpacing(8)

        self.boton_paso_anterior = QPushButton("◀ Anterior")
        self.boton_paso_anterior.setObjectName("btnNav")
        self.boton_paso_anterior.setMinimumWidth(95)
        self.boton_paso_anterior.setToolTip("Ir al paso anterior")
        diseno_nav.addWidget(self.boton_paso_anterior)

        self.etiqueta_paso = QLabel("Paso 0 de 0")
        self.etiqueta_paso.setObjectName("stepLabel")
        self.etiqueta_paso.setAlignment(Qt.AlignmentFlag.AlignCenter)
        diseno_nav.addWidget(self.etiqueta_paso, stretch=1)

        self.boton_paso_siguiente = QPushButton("Siguiente ▶")
        self.boton_paso_siguiente.setObjectName("btnNav")
        self.boton_paso_siguiente.setMinimumWidth(95)
        self.boton_paso_siguiente.setToolTip("Avanzar al paso siguiente")
        diseno_nav.addWidget(self.boton_paso_siguiente)

        diseno_derecho.addWidget(contenedor_nav)

        # Visor de texto enriquecido HTML con fondo blanco puro tipo papel
        self.visor_resultados = QTextBrowser()
        self.visor_resultados.setOpenExternalLinks(False)
        self.visor_resultados.setStyleSheet("""
            QTextBrowser {
                background-color: #FFFFFF;
                border: 1px solid #D1D5DB;
                border-radius: 0px;
                color: #000000;
            }
        """)
        diseno_derecho.addWidget(self.visor_resultados, stretch=1)

        self.divisor.addWidget(panel_derecho)

        # Proporción inicial: 42% entrada, 58% desarrollo de pasos
        self.divisor.setSizes([460, 640])
        diseno_principal.addWidget(self.divisor, stretch=1)

        # Barra de estado
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        self.barra_estado.showMessage("Listo • Ingrese los coeficientes y términos independientes en las celdas.")

    def _conectar_senales(self):
        self.selector_tamano.tamano_cambiado.connect(self._al_cambiar_tamano_matriz)
        self.panel_acciones.limpiar_solicitado.connect(self._limpiar_matriz)
        self.panel_acciones.calcular_solicitado.connect(self._al_solicitar_calculo)

        self.boton_paso_anterior.clicked.connect(self._al_retroceder_paso)
        self.boton_paso_siguiente.clicked.connect(self._al_avanzar_paso)
        self.boton_ver_todo.clicked.connect(self._al_alternar_ver_todo)

    def _al_cambiar_tamano_matriz(self, nuevo_tamano: int):
        self.tabla_matriz.actualizar_dimensiones(nuevo_tamano)
        self._mostrar_mensaje_inicial_resultados()
        self.barra_estado.showMessage(f"Dimensión actualizada a {nuevo_tamano}×{nuevo_tamano}.")

    def _limpiar_matriz(self):
        self.tabla_matriz.limpiar_todo()
        self._mostrar_mensaje_inicial_resultados()
        self.barra_estado.showMessage("Todas las celdas fueron limpiadas.")

    def _mostrar_mensaje_inicial_resultados(self):
        """Limpia el visor de resultados y desactiva los controles de navegación."""
        self._resultado_actual = None
        self._pasos = []
        self._indice_paso_actual = 0
        self._modo_ver_todo = False

        self.boton_paso_anterior.setEnabled(False)
        self.boton_paso_siguiente.setEnabled(False)
        self.boton_ver_todo.setEnabled(False)
        self.boton_ver_todo.setText("Ver Todo")
        self.etiqueta_paso.setText("Paso 0 de 0")

        self.visor_resultados.setHtml("""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #6B7280; background-color: #FFFFFF; padding: 40px 20px; text-align: center;">
            <div style="font-size: 15px; font-weight: bold; color: #111827; margin-bottom: 8px;">
                Desarrollo Paso a Paso
            </div>
            <div style="font-size: 13px; line-height: 1.6; color: #4B5563;">
                Ingrese los coeficientes en la tabla y presione <b>Resolver Sistema</b>.<br>
                El procedimiento se mostrará paso a paso para facilitar su comprensión pedagógica.
            </div>
        </div>
        """)

    def _mostrar_paso_actual(self, desplazar_al_nuevo: bool = True):
        """
        Muestra de manera acumulativa las operaciones desde el Paso 1 hasta el paso actual,
        haciendo que cada nueva operación aparezca abajo de la anterior de forma secuencial
        (como en una hoja continua, sin borrar lo anterior como si fuera un cuaderno).
        """
        if not self._pasos:
            return

        total = len(self._pasos)
        idx = self._indice_paso_actual
        titulo_paso, _ = self._pasos[idx]

        self.etiqueta_paso.setText(f"<span style='color: #DC2626; font-weight: bold;'>Paso {idx + 1} de {total}:</span> {titulo_paso}")

        # Concatenar todas las operaciones hasta el paso actual
        # De este modo cada paso aparece ABAJO del anterior
        contenido_acumulado = "".join([self._pasos[i][1] for i in range(idx + 1)])
        self.visor_resultados.setHtml(envolver_html_paso(contenido_acumulado))

        # Actualizar estado de los botones según la posición del paso
        self.boton_paso_anterior.setEnabled(idx > 0)
        self.boton_paso_siguiente.setEnabled(idx < total - 1)
        self.boton_ver_todo.setEnabled(True)

        if idx == total - 1:
            self.boton_ver_todo.setText("Reiniciar Pasos")
        else:
            self.boton_ver_todo.setText("Ver Todo")

        # Desplazar la vista para que la última operación que apareció abajo sea visible
        if desplazar_al_nuevo and idx > 0:
            QTimer.singleShot(60, lambda: self._desplazar_al_ancla(idx))
        elif idx == 0:
            QTimer.singleShot(60, lambda: self.visor_resultados.verticalScrollBar().setValue(0))

    def _desplazar_al_ancla(self, idx: int):
        """Desplaza el scroll suavemente para enfocar la nueva operación agregada abajo."""
        self.visor_resultados.scrollToAnchor(f"paso_{idx}")

    def _al_avanzar_paso(self):
        """Avanza al siguiente paso del desarrollo (agregándolo abajo)."""
        if self._modo_ver_todo:
            self._modo_ver_todo = False
        if self._indice_paso_actual < len(self._pasos) - 1:
            self._indice_paso_actual += 1
            self._mostrar_paso_actual(desplazar_al_nuevo=True)

    def _al_retroceder_paso(self):
        """Retrocede al paso anterior (removiendo la última operación de abajo)."""
        if self._modo_ver_todo:
            self._modo_ver_todo = False
        if self._indice_paso_actual > 0:
            self._indice_paso_actual -= 1
            self._mostrar_paso_actual(desplazar_al_nuevo=True)

    def _al_alternar_ver_todo(self):
        """Alterna entre mostrar todas las operaciones o reiniciar al paso 1."""
        if not self._resultado_actual or not self._pasos:
            return

        total = len(self._pasos)
        # Si ya se muestran todos los pasos, reiniciar al paso 1
        if self._indice_paso_actual == total - 1 or self._modo_ver_todo:
            self._modo_ver_todo = False
            self._indice_paso_actual = 0
            self._mostrar_paso_actual(desplazar_al_nuevo=False)
        else:
            # Mostrar todas las operaciones directamente de corrido
            self._modo_ver_todo = True
            self._indice_paso_actual = total - 1
            self.etiqueta_paso.setText(f"<span style='color: #DC2626; font-weight: bold;'>Mostrando todos los pasos:</span> 1 al {total}")
            self.visor_resultados.setHtml(generar_html_solucion(self._resultado_actual))
            self.boton_paso_anterior.setEnabled(True)
            self.boton_paso_siguiente.setEnabled(False)
            self.boton_ver_todo.setText("Reiniciar Pasos")
            QTimer.singleShot(60, lambda: self.visor_resultados.verticalScrollBar().setValue(0))

    def _al_solicitar_calculo(self):
        """
        Extrae la matriz A y el vector b, ejecuta el método de Cholesky
        e inicia la visualización mostrando el Paso 1 (las siguientes aparecerán abajo).
        """
        try:
            matriz_a = self.tabla_matriz.obtener_matriz_a()
            vector_b = self.tabla_matriz.obtener_vector_b()

            resultado = self._servicio.resolver(matriz_a, vector_b)
            self._resultado_actual = resultado
            self._pasos = obtener_pasos_html(resultado)
            self._indice_paso_actual = 0
            self._modo_ver_todo = False

            # Mostrar inicialmente el Paso 1
            self._mostrar_paso_actual(desplazar_al_nuevo=False)

            if resultado.exito:
                self.barra_estado.showMessage(f"Cálculo completado exitosamente • {len(self._pasos)} pasos disponibles.")
            else:
                self.barra_estado.showMessage(f"Atención: {resultado.mensaje_error}")

        except ValueError as ex:
            QMessageBox.critical(
                self,
                "Dato Faltante o Inválido",
                f"Por favor revise los valores ingresados:\n\n{str(ex)}"
            )
            self.barra_estado.showMessage("Error en datos de entrada.")
