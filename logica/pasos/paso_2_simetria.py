from dataclasses import dataclass
from typing import List, Tuple
from logica.matriz import Matriz


@dataclass(frozen=True)
class DetalleDiferenciaSimetria:
    """Detalle de discrepancia en caso de que A[i][j] != A[j][i]."""
    fila: int
    columna: int
    valor_original: float
    valor_traspuesta: float


@dataclass(frozen=True)
class ResultadoSimetria:
    """Resultado de la verificación de simetría."""
    matriz_a: Matriz
    matriz_at: Matriz
    es_simetrica: bool
    diferencias: List[DetalleDiferenciaSimetria]
    mensaje_error: str = ""


def comprobar_simetria(matriz_a: Matriz, tolerancia: float = 1e-9) -> ResultadoSimetria:
    """
    Comprueba si la matriz A es idéntica a su transpuesta (A = Aᵀ).
    Registra cualquier discrepancia numérica encontrada.
    """
    matriz_at = matriz_a.transponer()
    diferencias: List[DetalleDiferenciaSimetria] = []

    for i in range(matriz_a.filas):
        for j in range(i + 1, matriz_a.columnas):
            v_orig = matriz_a.obtener(i, j)
            v_trasp = matriz_a.obtener(j, i)
            if abs(v_orig - v_trasp) > tolerancia:
                diferencias.append(
                    DetalleDiferenciaSimetria(
                        fila=i + 1,
                        columna=j + 1,
                        valor_original=v_orig,
                        valor_traspuesta=v_trasp
                    )
                )

    es_sim = len(diferencias) == 0
    mensaje = ""
    if not es_sim:
        primera = diferencias[0]
        mensaje = (
            f"La matriz A no es simétrica: a_{{{primera.fila}{primera.columna}}} = {primera.valor_original:g} ≠ "
            f"a_{{{primera.columna}{primera.fila}}} = {primera.valor_traspuesta:g}. "
            "El método de Cholesky exige que A = Aᵀ."
        )

    return ResultadoSimetria(
        matriz_a=matriz_a,
        matriz_at=matriz_at,
        es_simetrica=es_sim,
        diferencias=diferencias,
        mensaje_error=mensaje
    )
