from typing import List
from dataclasses import dataclass
from logica.matriz import Matriz, Vector


@dataclass(frozen=True)
class PasoSustitucion:
    """Detalle de cálculo para una variable en la sustitución."""
    indice: int             # 1-indexed (1..n)
    nombre_variable: str    # ej. 'D₁'
    formula_simbolica: str
    sustitucion_numerica: str
    valor: float


@dataclass(frozen=True)
class ResultadoSustitucionProgresiva:
    """Resultado de la resolución del sistema L · D = B."""
    vector_d: Vector
    pasos: List[PasoSustitucion]


def resolver_sustitucion_progresiva(matriz_l: Matriz, vector_b: Vector) -> ResultadoSustitucionProgresiva:
    """
    Resuelve el sistema L · D = B (Sustitución hacia adelante de 1 a n).
    """
    n = matriz_l.filas
    d_vals = [0.0] * n
    pasos: List[PasoSustitucion] = []

    for i in range(n):
        i_humano = i + 1
        nombre_var = f"D_{{{i_humano}}}"

        l_ii = matriz_l.obtener(i, i)
        b_i = vector_b.obtener(i)

        terminos_simb = []
        terminos_num = []
        suma = 0.0

        for j in range(i):
            j_humano = j + 1
            l_ij = matriz_l.obtener(i, j)
            d_j = d_vals[j]
            terminos_simb.append(f"l_{{{i_humano}{j_humano}}} · D_{{{j_humano}}}")
            terminos_num.append(f"({l_ij:g})({d_j:g})")
            suma += l_ij * d_j

        if not terminos_simb:
            if abs(l_ii - 1.0) < 1e-9:
                form_simb = f"{nombre_var} = b_{{{i_humano}}}"
                sust_num = f"{b_i:g}"
            else:
                form_simb = f"{nombre_var} = b_{{{i_humano}}} / l_{{{i_humano}{i_humano}}}"
                sust_num = f"{b_i:g} / {l_ii:g}"
        else:
            suma_simb_str = " + ".join(terminos_simb)
            suma_num_str = " + ".join(terminos_num)
            form_simb = f"{nombre_var} = (b_{{{i_humano}}} - ({suma_simb_str})) / l_{{{i_humano}{i_humano}}}"
            sust_num = f"({b_i:g} - ({suma_num_str})) / {l_ii:g}"

        val = (b_i - suma) / l_ii
        d_vals[i] = val

        pasos.append(PasoSustitucion(
            indice=i_humano,
            nombre_variable=nombre_var,
            formula_simbolica=form_simb,
            sustitucion_numerica=sust_num,
            valor=val
        ))

    return ResultadoSustitucionProgresiva(
        vector_d=Vector.desde_lista(d_vals),
        pasos=pasos
    )
