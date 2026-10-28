"""
Paso 3: Comprobación de Definida Positiva mediante el Criterio de Sylvester.
"""

from typing import Tuple
from logica.cholesky import ResultadoCompletoCholesky


def generar_paso_3(res: ResultadoCompletoCholesky) -> Tuple[str, str]:
    """Retorna (titulo, html) para el Paso 3."""
    filas_menores = []
    for p in res.pasos_menores:
        icono = "✓" if p.es_positivo else "✗"
        simb_comparacion = "> 0" if p.es_positivo else "≤ 0"
        filas_menores.append(f"""
        <div style="margin-bottom: 6px; font-family: Consolas, monospace; font-size: 13px; color: #000000; padding-left: 10px;">
            • {p.explicacion} = <b>{p.valor:g} {simb_comparacion}</b> ({icono})
        </div>
        """)

    positiva_msg = """
    <div style="margin-top: 10px; font-weight: bold; color: #000000;">
        ✓ Es definida positiva (todos los menores principales líderes son mayores a cero).
    </div>
    """ if res.es_definida_positiva else """
    <div style="margin-top: 10px; font-weight: bold; color: #000000;">
        ✗ No es definida positiva (al menos un menor principal es menor o igual a cero).
    </div>
    """
    html = f"""
    <div id="paso_2" style="margin-bottom: 24px;">
        <div style="font-weight: bold; font-size: 15px; border-bottom: 1.5px solid #DC2626; padding-bottom: 3px; margin-bottom: 10px; color: #DC2626;">
            3. COMPROBAMOS SI ES DEFINIDA POSITIVA (CRITERIO DE SYLVESTER)
        </div>
        <p style="margin: 0 0 10px 0; color: #000000; font-size: 13px;">
            Evaluamos los determinantes de los menores principales líderes (Δ<sub>kk</sub> &gt; 0):
        </p>
        {''.join(filas_menores)}
        {positiva_msg}
    </div>
    """
    return ("Comprobación de Definida Positiva", html)
