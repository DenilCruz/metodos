"""
Módulo de Pasos de Lógica Matemática del Método de Cholesky.
Cada paso matemático del método está encapsulado en su propio archivo independiente,
garantizando el principio de responsabilidad única (SRP) y alta cohesión.
"""

from logica.pasos.paso_1_planteamiento import (
    ResultadoPlanteamiento,
    plantear_sistema,
)
from logica.pasos.paso_2_simetria import (
    ResultadoSimetria,
    DetalleDiferenciaSimetria,
    comprobar_simetria,
)
from logica.pasos.paso_3_definida_positiva import (
    PasoMenorPrincipal,
    ResultadoDefinidaPositiva,
    determinante_puro,
    calcular_menores_principales,
    comprobar_definida_positiva,
)
from logica.pasos.paso_4_descomposicion import (
    PasoCalculoElemento,
    EtapaKCholesky,
    ResultadoDescomposicionCholesky,
    DescomponedorCholesky,
    descomponer_cholesky,
)
from logica.pasos.paso_5_sustitucion_progresiva import (
    PasoSustitucion as PasoSustitucionProgresiva,
    ResultadoSustitucionProgresiva,
    resolver_sustitucion_progresiva,
)
from logica.pasos.paso_6_sustitucion_regresiva import (
    PasoSustitucion as PasoSustitucionRegresiva,
    ResultadoSustitucionRegresiva,
    resolver_sustitucion_regresiva,
)
from logica.pasos.paso_7_solucion_general import (
    ElementoSolucion,
    ResultadoSolucionGeneral,
    consolidar_solucion_general,
)

__all__ = [
    # Paso 1
    "ResultadoPlanteamiento",
    "plantear_sistema",
    # Paso 2
    "ResultadoSimetria",
    "DetalleDiferenciaSimetria",
    "comprobar_simetria",
    # Paso 3
    "PasoMenorPrincipal",
    "ResultadoDefinidaPositiva",
    "determinante_puro",
    "calcular_menores_principales",
    "comprobar_definida_positiva",
    # Paso 4
    "PasoCalculoElemento",
    "EtapaKCholesky",
    "ResultadoDescomposicionCholesky",
    "DescomponedorCholesky",
    "descomponer_cholesky",
    # Paso 5
    "PasoSustitucionProgresiva",
    "ResultadoSustitucionProgresiva",
    "resolver_sustitucion_progresiva",
    # Paso 6
    "PasoSustitucionRegresiva",
    "ResultadoSustitucionRegresiva",
    "resolver_sustitucion_regresiva",
    # Paso 7
    "ElementoSolucion",
    "ResultadoSolucionGeneral",
    "consolidar_solucion_general",
]
