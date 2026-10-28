"""
Lógica del Paso 7: Solución General del Sistema Lineal.
Consolida el vector solución X y estructura los valores finales de cada incógnita (x₁, x₂, ..., xₙ).
"""

from typing import List
from dataclasses import dataclass
from logica.matriz import Vector


@dataclass(frozen=True)
class ElementoSolucion:
    """Representación individual de una incógnita resuelta."""
    indice: int
    nombre_variable: str
    valor: float


@dataclass(frozen=True)
class ResultadoSolucionGeneral:
    """Resultado final consolidado de la solución general del sistema."""
    vector_x: Vector
    elementos: List[ElementoSolucion]
    dimension: int


def consolidar_solucion_general(vector_x: Vector) -> ResultadoSolucionGeneral:
    """
    Consolida las soluciones del vector X asignando a cada elemento su nombre de incógnita correspondiente.
    """
    n = vector_x.tamano
    elementos: List[ElementoSolucion] = []

    for i in range(n):
        i_humano = i + 1
        elementos.append(
            ElementoSolucion(
                indice=i_humano,
                nombre_variable=f"x{i_humano}",
                valor=vector_x.obtener(i)
            )
        )

    return ResultadoSolucionGeneral(
        vector_x=vector_x,
        elementos=elementos,
        dimension=n
    )
