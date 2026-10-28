"""
Orquestador de representación visual para el Método de Cholesky.
Delega la construcción de cada paso a su propio archivo modular en `interfaz/pasos/`.
"""

from typing import List
from logica.cholesky import ResultadoCompletoCholesky
from interfaz.pasos import (
    envolver_html_paso,
    generar_paso_1,
    generar_paso_2,
    generar_paso_3,
    generar_paso_4,
    generar_paso_5,
    generar_paso_6,
    generar_paso_7,
)


def obtener_pasos_html(res: ResultadoCompletoCholesky) -> List[tuple[str, str]]:
    """
    Obtiene la lista de los 7 pasos en tuplas (titulo, html)
    llamando al archivo generador de cada paso.
    """
    pasos: List[tuple[str, str]] = [
        generar_paso_1(res),
        generar_paso_2(res),
        generar_paso_3(res),
    ]

    # Si la matriz no es simétrica o no es definida positiva, el procedimiento se detiene
    if not res.exito:
        return pasos

    p4 = generar_paso_4(res)
    if p4:
        pasos.append(p4)

    p5 = generar_paso_5(res)
    if p5:
        pasos.append(p5)

    p6 = generar_paso_6(res)
    if p6:
        pasos.append(p6)

    p7 = generar_paso_7(res)
    if p7:
        pasos.append(p7)

    return pasos


def generar_html_un_paso(res: ResultadoCompletoCholesky, indice_paso: int) -> str:
    """Genera el HTML exclusivamente para un paso específico (0-indexed)."""
    pasos = obtener_pasos_html(res)
    if not pasos or indice_paso < 0 or indice_paso >= len(pasos):
        return ""
    return envolver_html_paso(pasos[indice_paso][1])


def generar_html_solucion(res: ResultadoCompletoCholesky) -> str:
    """Construye el documento HTML completo con todos los pasos continuos."""
    pasos = obtener_pasos_html(res)
    contenido = "".join([p[1] for p in pasos])
    return envolver_html_paso(contenido)
