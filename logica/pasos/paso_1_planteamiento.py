from dataclasses import dataclass
from logica.matriz import Matriz, Vector


@dataclass(frozen=True)
class ResultadoPlanteamiento:
    """Resultado de validación y planteamiento del sistema A · X = B."""
    matriz_a: Matriz
    vector_b: Vector
    dimension: int
    es_valido: bool
    mensaje_error: str = ""


def plantear_sistema(matriz_a: Matriz, vector_b: Vector) -> ResultadoPlanteamiento:
    """
    Valida que la matriz A sea cuadrada y compatible con la dimensión del vector b.
    """
    if not matriz_a.es_cuadrada:
        return ResultadoPlanteamiento(
            matriz_a=matriz_a,
            vector_b=vector_b,
            dimension=matriz_a.filas,
            es_valido=False,
            mensaje_error=f"La matriz A debe ser cuadrada. Dimensiones recibidas: {matriz_a.filas}×{matriz_a.columnas}."
        )

    if matriz_a.filas != vector_b.tamano:
        return ResultadoPlanteamiento(
            matriz_a=matriz_a,
            vector_b=vector_b,
            dimension=matriz_a.filas,
            es_valido=False,
            mensaje_error=f"La dimensión de la matriz A ({matriz_a.filas}) no coincide con la longitud del vector b ({vector_b.tamano})."
        )

    return ResultadoPlanteamiento(
        matriz_a=matriz_a,
        vector_b=vector_b,
        dimension=matriz_a.filas,
        es_valido=True
    )
