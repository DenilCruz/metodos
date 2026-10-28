"""
Paso 2: Comprobación de Simetría de la Matriz (A = Aᵀ).
"""

from typing import Tuple
from logica.cholesky import ResultadoCompletoCholesky
from interfaz.pasos.comun import _render_matriz_html


def generar_paso_2(res: ResultadoCompletoCholesky) -> Tuple[str, str]:
    """Retorna (titulo, html) para el Paso 2."""
    simetria_msg = """
    <div style="margin-top: 10px; font-weight: bold; color: #000000;">
        ✓ Sí es simétrica (A = Aᵀ).
    </div>
    """ if res.es_simetrica else """
    <div style="margin-top: 10px; font-weight: bold; color: #000000;">
        ✗ No es simétrica. Cholesky requiere que la matriz sea simétrica.
    </div>
    """
    html = f"""
    <div id="paso_1" style="margin-bottom: 24px;">
        <div style="font-weight: bold; font-size: 15px; border-bottom: 1.5px solid #DC2626; padding-bottom: 3px; margin-bottom: 12px; color: #DC2626;">
            2. COMPROBAMOS SI ES SIMÉTRICA (A = Aᵀ)
        </div>
        <table style="border-collapse: collapse; border: none; margin: 8px 0;">
            <tr>
                <td style="vertical-align: middle; padding-right: 6px; font-weight: bold; font-size: 15px; color: #000000;">A =</td>
                <td style="vertical-align: middle;">{_render_matriz_html(res.matriz_a.a_lista())}</td>
                <td style="vertical-align: middle; padding: 0 14px; font-weight: bold; font-size: 15px; color: #000000;">Aᵀ =</td>
                <td style="vertical-align: middle;">{_render_matriz_html(res.matriz_at.a_lista())}</td>
            </tr>
        </table>
        {simetria_msg}
    </div>
    """
    return ("Comprobación de Simetría", html)
