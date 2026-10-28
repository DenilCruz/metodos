from typing import List, Tuple
from dataclasses import dataclass
from logica.matriz import Matriz


@dataclass(frozen=True)
class PasoMenorPrincipal:
    """Información detallada de un menor principal líder Delta_k."""
    orden: int
    submatriz: List[List[float]]
    valor: float
    explicacion: str
    es_positivo: bool


@dataclass(frozen=True)
class ResultadoDefinidaPositiva:
    """Resultado de la verificación de matriz definida positiva mediante Sylvester."""
    matriz: Matriz
    pasos_menores: List[PasoMenorPrincipal]
    es_definida_positiva: bool
    mensaje_error: str = ""


def determinante_puro(matriz: List[List[float]]) -> float:
    """
    Calcula el determinante de una matriz cuadrada mediante eliminación Gaussiana
    con pivoteo parcial desde cero (Python puro, sin librerías).
    """
    n = len(matriz)
    if n == 1:
        return float(matriz[0][0])
    if n == 2:
        return float(matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0])

    # Copia para no mutar los datos originales
    a = [row[:] for row in matriz]
    det = 1.0

    for i in range(n):
        # Encontrar pivote máximo
        pivote = i
        for r in range(i + 1, n):
            if abs(a[r][i]) > abs(a[pivote][i]):
                pivote = r

        if abs(a[pivote][i]) < 1e-12:
            return 0.0

        if pivote != i:
            a[i], a[pivote] = a[pivote], a[i]
            det = -det

        det *= a[i][i]
        piv_val = a[i][i]

        for r in range(i + 1, n):
            factor = a[r][i] / piv_val
            for c in range(i + 1, n):
                a[r][c] -= factor * a[i][c]

    return det


def calcular_menores_principales(matriz_datos: List[List[float]]) -> Tuple[List[PasoMenorPrincipal], bool]:
    """
    Calcula todos los menores principales líderes (Criterio de Sylvester)
    y genera la explicación matemática paso a paso.
    """
    n = len(matriz_datos)
    pasos: List[PasoMenorPrincipal] = []
    es_definida_positiva = True

    for k in range(1, n + 1):
        # Submatriz principal de orden k x k
        submatriz = [fila[:k] for fila in matriz_datos[:k]]
        val = determinante_puro(submatriz)

        # Generar texto de desglose aritmético según el orden
        if k == 1:
            exp = f"Δ₁₁ = a₁₁ = {submatriz[0][0]:g}"
        elif k == 2:
            a, b = submatriz[0][0], submatriz[0][1]
            c, d = submatriz[1][0], submatriz[1][1]
            prod1 = a * d
            prod2 = b * c
            exp = f"Δ₂₂ = ({a:g})({d:g}) - ({b:g})({c:g}) = {prod1:g} - ({prod2:g}) = {val:g}"
        elif k == 3:
            # Regla de Sarrus / cofactores detallada
            a, b, c = submatriz[0]
            d, e, f = submatriz[1]
            g, h, i = submatriz[2]
            p1 = a * e * i
            p2 = b * f * g
            p3 = c * d * h
            n1 = c * e * g
            n2 = a * f * h
            n3 = b * d * i
            exp = (
                f"Δ₃₃ = ({p1:g} + {p2:g} + {p3:g}) - ({n1:g} + {n2:g} + {n3:g}) = "
                f"{(p1+p2+p3):g} - {(n1+n2+n3):g} = {val:g}"
            )
        else:
            exp = f"Δ_{k}{k} = det(Submatriz {k}×{k}) = {val:g}"

        positivo = val > 1e-12
        if not positivo:
            es_definida_positiva = False

        pasos.append(PasoMenorPrincipal(
            orden=k,
            submatriz=submatriz,
            valor=val,
            explicacion=exp,
            es_positivo=positivo
        ))

    return pasos, es_definida_positiva


def comprobar_definida_positiva(matriz_a: Matriz) -> ResultadoDefinidaPositiva:
    """
    Comprueba formalmente si la matriz A es definida positiva aplicando Sylvester.
    """
    pasos, es_def_pos = calcular_menores_principales(matriz_a.a_lista())
    mensaje = ""
    if not es_def_pos:
        menores_no_pos = [p for p in pasos if not p.es_positivo]
        if menores_no_pos:
            primer_no_pos = menores_no_pos[0]
            mensaje = (
                f"La matriz A no es definida positiva: El menor principal Δ_{{{primer_no_pos.orden}{primer_no_pos.orden}}} "
                f"= {primer_no_pos.valor:g} ≤ 0. El método de Cholesky requiere que todos los menores principales sean positivos."
            )
        else:
            mensaje = "La matriz A no es definida positiva."

    return ResultadoDefinidaPositiva(
        matriz=matriz_a,
        pasos_menores=pasos,
        es_definida_positiva=es_def_pos,
        mensaje_error=mensaje
    )
