"""
Paso 1: Planteamiento del Sistema de Ecuaciones en forma matricial (A · X = B).
"""

from typing import Tuple
from logica.cholesky import ResultadoCompletoCholesky
from interfaz.pasos.comun import _render_matriz_html, _render_vector_html


def generar_paso_1(res: ResultadoCompletoCholesky) -> Tuple[str, str]:
    """Retorna (titulo, html) para el Paso 1."""
    n = res.matriz_a.filas
    nombres_vars = [f"x{i+1}" for i in range(n)]

    html = f"""
    <div id="paso_0" style="margin-bottom: 24px;">
        <div style="font-weight: bold; font-size: 15px; border-bottom: 1.5px solid #DC2626; padding-bottom: 3px; margin-bottom: 12px; color: #DC2626;">
            1. PLANTEAMIENTO DEL SISTEMA (A · X = B)
        </div>
        <table style="border-collapse: collapse; border: none; margin: 8px 0;">
            <tr>
                <td style="vertical-align: middle; padding-right: 6px; font-weight: bold; font-size: 15px; color: #000000;">A =</td>
                <td style="vertical-align: middle;">{_render_matriz_html(res.matriz_a.a_lista())}</td>
                <td style="vertical-align: middle; padding: 0 8px; font-weight: bold; font-size: 15px; color: #000000;">·  X =</td>
                <td style="vertical-align: middle;">{_render_vector_html([0.0]*n, nombres_vars)}</td>
                <td style="vertical-align: middle; padding: 0 8px; font-weight: bold; font-size: 15px; color: #000000;">=  B =</td>
                <td style="vertical-align: middle;">{_render_vector_html(res.vector_b.a_lista())}</td>
            </tr>
        </table>
    </div>
    """
    return ("Planteamiento del Sistema", html)
