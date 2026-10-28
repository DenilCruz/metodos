import math
from typing import List
from dataclasses import dataclass
from logica.matriz import Matriz


@dataclass(frozen=True)
class PasoCalculoElemento:
    """Detalle de cálculo de un elemento L_ki."""
    k: int  # Fila (1-indexed)
    i: int  # Columna (1-indexed)
    es_diagonal: bool
    formula_simbolica: str
    sustitucion_numerica: str
    resultado_intermedio: str
    valor: float


@dataclass(frozen=True)
class EtapaKCholesky:
    """Agrupación de cálculos para una etapa K (fila k de L)."""
    k: int
    pasos: List[PasoCalculoElemento]


@dataclass(frozen=True)
class ResultadoDescomposicionCholesky:
    """Resultado completo de la descomposición Cholesky."""
    matriz_l: Matriz
    matriz_lt: Matriz
    etapas: List[EtapaKCholesky]
    exito: bool
    mensaje_error: str = ""


class DescomponedorCholesky:
    """
    Realiza la factorización A = L · Lᵀ de forma puramente nativa,
    registrando cada fórmula y sustitución aritmética.
    """

    def descomponer(self, matriz_a: Matriz) -> ResultadoDescomposicionCholesky:
        n = matriz_a.filas
        # Matriz L inicializada en ceros
        l_datos = [[0.0 for _ in range(n)] for _ in range(n)]
        etapas: List[EtapaKCholesky] = []

        for k in range(n):  # Índice 0 a n-1
            k_humano = k + 1
            pasos_etapa: List[PasoCalculoElemento] = []

            # 1. Elementos fuera de la diagonal: L[k][i] para i < k
            for i in range(k):
                i_humano = i + 1

                # Suma sum_j (L[k][j] * L[i][j]) para j = 0 .. i-1
                terminos_sum_simb = []
                terminos_sum_num = []
                suma_acumulada = 0.0

                for j in range(i):
                    j_humano = j + 1
                    terminos_sum_simb.append(f"l_{{{i_humano}{j_humano}}} · l_{{{k_humano}{j_humano}}}")
                    v_ij = l_datos[i][j]
                    v_kj = l_datos[k][j]
                    terminos_sum_num.append(f"({v_ij:g} · {v_kj:g})")
                    suma_acumulada += v_ij * v_kj

                a_ki = matriz_a.obtener(k, i)
                l_ii = l_datos[i][i]

                if abs(l_ii) < 1e-12:
                    return ResultadoDescomposicionCholesky(
                        matriz_l=Matriz.ceros(n, n),
                        matriz_lt=Matriz.ceros(n, n),
                        etapas=etapas,
                        exito=False,
                        mensaje_error=f"División por cero al calcular L_{{{k_humano}{i_humano}}}: L_{{{i_humano}{i_humano}}} es 0."
                    )

                # Construir fórmula simbólica y numérica
                if not terminos_sum_simb:
                    formula_simb = f"L_{{{k_humano}{i_humano}}} = a_{{{k_humano}{i_humano}}} / l_{{{i_humano}{i_humano}}}"
                    sust_num = f"{a_ki:g} / {l_ii:g}"
                else:
                    suma_str = " + ".join(terminos_sum_simb)
                    suma_num_str = " + ".join(terminos_sum_num)
                    formula_simb = f"L_{{{k_humano}{i_humano}}} = (a_{{{k_humano}{i_humano}}} - ({suma_str})) / l_{{{i_humano}{i_humano}}}"
                    sust_num = f"({a_ki:g} - ({suma_num_str})) / {l_ii:g}"

                numerador = a_ki - suma_acumulada
                val = numerador / l_ii
                l_datos[k][i] = val

                pasos_etapa.append(PasoCalculoElemento(
                    k=k_humano,
                    i=i_humano,
                    es_diagonal=False,
                    formula_simbolica=formula_simb,
                    sustitucion_numerica=sust_num,
                    resultado_intermedio=f"{numerador:g} / {l_ii:g}",
                    valor=val
                ))

            # 2. Elemento diagonal: L[k][k]
            terminos_cuad_simb = []
            terminos_cuad_num = []
            suma_cuadrados = 0.0

            for j in range(k):
                j_humano = j + 1
                terminos_cuad_simb.append(f"l_{{{k_humano}{j_humano}}}^2")
                v_kj = l_datos[k][j]
                terminos_cuad_num.append(f"({v_kj:g})^2")
                suma_cuadrados += v_kj * v_kj

            a_kk = matriz_a.obtener(k, k)
            radicando = a_kk - suma_cuadrados

            if not terminos_cuad_simb:
                formula_simb = f"L_{{{k_humano}{k_humano}}} = √(a_{{{k_humano}{k_humano}}})"
                sust_num = f"√({a_kk:g})"
            else:
                suma_str = " + ".join(terminos_cuad_simb)
                suma_num_str = " + ".join(terminos_cuad_num)
                formula_simb = f"L_{{{k_humano}{k_humano}}} = √(a_{{{k_humano}{k_humano}}} - ({suma_str}))"
                sust_num = f"√({a_kk:g} - ({suma_num_str}))"

            if radicando <= 1e-12:
                pasos_etapa.append(PasoCalculoElemento(
                    k=k_humano,
                    i=k_humano,
                    es_diagonal=True,
                    formula_simbolica=formula_simb,
                    sustitucion_numerica=sust_num,
                    resultado_intermedio=f"√({radicando:g})",
                    valor=0.0
                ))
                etapas.append(EtapaKCholesky(k=k_humano, pasos=pasos_etapa))
                return ResultadoDescomposicionCholesky(
                    matriz_l=Matriz.desde_lista_2d(l_datos),
                    matriz_lt=Matriz.desde_lista_2d(l_datos).transponer(),
                    etapas=etapas,
                    exito=False,
                    mensaje_error=(
                        f"La matriz no es definida positiva: En la etapa K={k_humano}, "
                        f"el radicando de L_{{{k_humano}{k_humano}}} es {radicando:g} ≤ 0. "
                        "No se puede calcular una raíz cuadrada real."
                    )
                )

            val_diag = math.sqrt(radicando)
            l_datos[k][k] = val_diag

            pasos_etapa.append(PasoCalculoElemento(
                k=k_humano,
                i=k_humano,
                es_diagonal=True,
                formula_simbolica=formula_simb,
                sustitucion_numerica=sust_num,
                resultado_intermedio=f"√({radicando:g})",
                valor=val_diag
            ))

            etapas.append(EtapaKCholesky(k=k_humano, pasos=pasos_etapa))

        matriz_l = Matriz.desde_lista_2d(l_datos)
        matriz_lt = matriz_l.transponer()

        return ResultadoDescomposicionCholesky(
            matriz_l=matriz_l,
            matriz_lt=matriz_lt,
            etapas=etapas,
            exito=True
        )


def descomponer_cholesky(matriz_a: Matriz) -> ResultadoDescomposicionCholesky:
    """Función de conveniencia para descomponer una matriz simétrica definida positiva."""
    descomponedor = DescomponedorCholesky()
    return descomponedor.descomponer(matriz_a)
