"""
Servicio orquestador del Método de Cholesky.
Cumple con el Principio de Inversión de Dependencias (DIP) y Responsabilidad Única (SRP).
Orquesta secuencialmente los 7 pasos matemáticos modulares definidos en `logica/pasos/`.
"""

from dataclasses import dataclass
from typing import List, Optional

from logica.matriz import Matriz, Vector
from logica.pasos import (
    # Paso 1
    ResultadoPlanteamiento,
    plantear_sistema,
    # Paso 2
    ResultadoSimetria,
    comprobar_simetria,
    # Paso 3
    PasoMenorPrincipal,
    ResultadoDefinidaPositiva,
    comprobar_definida_positiva,
    # Paso 4
    ResultadoDescomposicionCholesky,
    DescomponedorCholesky,
    # Paso 5
    ResultadoSustitucionProgresiva,
    resolver_sustitucion_progresiva,
    # Paso 6
    ResultadoSustitucionRegresiva,
    resolver_sustitucion_regresiva,
    # Paso 7
    ResultadoSolucionGeneral,
    consolidar_solucion_general,
)


@dataclass(frozen=True)
class ResultadoCompletoCholesky:
    """Contenedor de todos los pasos y resultados del método de Cholesky."""
    matriz_a: Matriz
    vector_b: Vector

    # 1. Simetría
    es_simetrica: bool
    matriz_at: Matriz

    # 2. Menores principales (Definida Positiva)
    pasos_menores: List[PasoMenorPrincipal]
    es_definida_positiva: bool

    # 3. Descomposición Cholesky A = L · Lᵀ
    descomposicion: Optional[ResultadoDescomposicionCholesky]

    # 4. Sustitución progresiva L · D = B
    progresiva: Optional[ResultadoSustitucionProgresiva]

    # 5. Sustitución regresiva Lᵀ · X = D
    regresiva: Optional[ResultadoSustitucionRegresiva]

    # Estado general
    exito: bool
    mensaje_error: str = ""

    # 7. Solución general consolidada
    solucion_general: Optional[ResultadoSolucionGeneral] = None


class ServicioCholesky:
    """
    Orquesta la ejecución secuencial completa de los 7 pasos del método de Cholesky.
    """

    def __init__(self, descomponedor: Optional[DescomponedorCholesky] = None):
        self._descomponedor = descomponedor or DescomponedorCholesky()

    def resolver(self, matriz_a: Matriz, vector_b: Vector) -> ResultadoCompletoCholesky:
        # Paso 1: Planteamiento y validación de dimensiones
        res_planteamiento = plantear_sistema(matriz_a, vector_b)
        if not res_planteamiento.es_valido:
            return ResultadoCompletoCholesky(
                matriz_a=matriz_a,
                vector_b=vector_b,
                es_simetrica=False,
                matriz_at=matriz_a.transponer(),
                pasos_menores=[],
                es_definida_positiva=False,
                descomposicion=None,
                progresiva=None,
                regresiva=None,
                exito=False,
                mensaje_error=res_planteamiento.mensaje_error
            )

        # Paso 2: Comprobación de Simetría (A = Aᵀ)
        res_simetria = comprobar_simetria(matriz_a)
        if not res_simetria.es_simetrica:
            return ResultadoCompletoCholesky(
                matriz_a=matriz_a,
                vector_b=vector_b,
                es_simetrica=False,
                matriz_at=res_simetria.matriz_at,
                pasos_menores=[],
                es_definida_positiva=False,
                descomposicion=None,
                progresiva=None,
                regresiva=None,
                exito=False,
                mensaje_error=res_simetria.mensaje_error
            )

        # Paso 3: Comprobación de Definida Positiva (Sylvester Δ_kk > 0)
        res_def_pos = comprobar_definida_positiva(matriz_a)
        if not res_def_pos.es_definida_positiva:
            return ResultadoCompletoCholesky(
                matriz_a=matriz_a,
                vector_b=vector_b,
                es_simetrica=True,
                matriz_at=res_simetria.matriz_at,
                pasos_menores=res_def_pos.pasos_menores,
                es_definida_positiva=False,
                descomposicion=None,
                progresiva=None,
                regresiva=None,
                exito=False,
                mensaje_error=res_def_pos.mensaje_error
            )

        # Paso 4: Descomposición de Cholesky (A = L · Lᵀ)
        res_decomp = self._descomponedor.descomponer(matriz_a)
        if not res_decomp.exito:
            return ResultadoCompletoCholesky(
                matriz_a=matriz_a,
                vector_b=vector_b,
                es_simetrica=True,
                matriz_at=res_simetria.matriz_at,
                pasos_menores=res_def_pos.pasos_menores,
                es_definida_positiva=False,
                descomposicion=res_decomp,
                progresiva=None,
                regresiva=None,
                exito=False,
                mensaje_error=res_decomp.mensaje_error
            )

        # Paso 5: Sustitución progresiva (L · D = B)
        res_prog = resolver_sustitucion_progresiva(res_decomp.matriz_l, vector_b)

        # Paso 6: Sustitución regresiva (Lᵀ · X = D)
        res_reg = resolver_sustitucion_regresiva(res_decomp.matriz_lt, res_prog.vector_d)

        # Paso 7: Solución general consolidada (X)
        res_sol = consolidar_solucion_general(res_reg.vector_x)

        return ResultadoCompletoCholesky(
            matriz_a=matriz_a,
            vector_b=vector_b,
            es_simetrica=True,
            matriz_at=res_simetria.matriz_at,
            pasos_menores=res_def_pos.pasos_menores,
            es_definida_positiva=True,
            descomposicion=res_decomp,
            progresiva=res_prog,
            regresiva=res_reg,
            solucion_general=res_sol,
            exito=True
        )
