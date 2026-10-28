"""
Lógica del Paso 6: Sustitución Regresiva (Lᵀ · X = D).
Resuelve el sistema triangular superior mediante sustitución hacia atrás (de n hacia 1),
encontrando el vector de incógnitas X y registrando las operaciones aritméticas paso a paso.
"""

from typing import List
from dataclasses import dataclass
from logica.matriz import Matriz, Vector


@dataclass(frozen=True)
class PasoSustitucion:
    """Detalle de cálculo para una variable en la sustitución."""
    indice: int             # 1-indexed (1..n)
    nombre_variable: str    # ej. 'x₁'
    formula_simbolica: str
    sustitucion_numerica: str
    valor: float


@dataclass(frozen=True)
class ResultadoSustitucionRegresiva:
    """Resultado de la resolución del sistema Lᵀ · X = D."""
    vector_x: Vector
    pasos: List[PasoSustitucion]


def resolver_sustitucion_regresiva(matriz_lt: Matriz, vector_d: Vector) -> ResultadoSustitucionRegresiva:
    """
    Resuelve el sistema Lᵀ · X = D (Sustitución hacia atrás de n hacia 1).
    """
    n = matriz_lt.filas
    x_vals = [0.0] * n
    nombres = [f"x{i + 1}" for i in range(n)]
    pasos: List[PasoSustitucion] = []

    # Recorrer de abajo hacia arriba (n-1 a 0)
    for i in range(n - 1, -1, -1):
        i_humano = i + 1
        nombre_var = nombres[i]

        lt_ii = matriz_lt.obtener(i, i)
        d_i = vector_d.obtener(i)

        terminos_simb = []
        terminos_num = []
        suma = 0.0

        for j in range(i + 1, n):
            j_humano = j + 1
            lt_ij = matriz_lt.obtener(i, j)
            x_j = x_vals[j]
            nombre_j = nombres[j]
            terminos_simb.append(f"l^T_{{{i_humano}{j_humano}}} · {nombre_j}")
            terminos_num.append(f"({lt_ij:g})({x_j:g})")
            suma += lt_ij * x_j

        if not terminos_simb:
            if abs(lt_ii - 1.0) < 1e-9:
                form_simb = f"{nombre_var} = D_{{{i_humano}}}"
                sust_num = f"{d_i:g}"
            else:
                form_simb = f"{nombre_var} = D_{{{i_humano}}} / l^T_{{{i_humano}{i_humano}}}"
                sust_num = f"{d_i:g} / {lt_ii:g}"
        else:
            suma_simb_str = " + ".join(terminos_simb)
            suma_num_str = " + ".join(terminos_num)
            form_simb = f"{nombre_var} = (D_{{{i_humano}}} - ({suma_simb_str})) / l^T_{{{i_humano}{i_humano}}}"
            sust_num = f"({d_i:g} - ({suma_num_str})) / {lt_ii:g}"

        val = (d_i - suma) / lt_ii
        x_vals[i] = val

        pasos.append(PasoSustitucion(
            indice=i_humano,
            nombre_variable=nombre_var,
            formula_simbolica=form_simb,
            sustitucion_numerica=sust_num,
            valor=val
        ))

    return ResultadoSustitucionRegresiva(
        vector_x=Vector.desde_lista(x_vals),
        pasos=pasos
    )
