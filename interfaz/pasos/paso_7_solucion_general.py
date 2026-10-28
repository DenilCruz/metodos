"""
Paso 7: Solución General del Sistema (Vector X).
"""

from typing import Tuple, Optional
from logica.cholesky import ResultadoCompletoCholesky
from interfaz.pasos.comun import _formatear_numero, _render_vector_html


def generar_paso_7(res: ResultadoCompletoCholesky) -> Optional[Tuple[str, str]]:
    """Retorna (titulo, html) para el Paso 7, o None si no hay solución."""
    if not res.regresiva:
        return None

    n = res.matriz_a.filas
    nombres_vars = [f"x{i+1}" for i in range(n)]

    soluciones_txt = []
    for i, val in enumerate(res.regresiva.vector_x.a_lista()):
        var_nombre = nombres_vars[i]
        soluciones_txt.append(f"""
        <div style="margin: 6px 0; font-family: Consolas, monospace; font-size: 16px; color: #000000;">
            <span style="font-weight: bold;">{var_nombre}</span> = <b>{_formatear_numero(val)}</b>
        </div>
        """)

    html = f"""
    <div id="paso_6" style="margin-bottom: 16px;">
        <div style="font-weight: bold; font-size: 15px; border-bottom: 1.5px solid #DC2626; padding-bottom: 3px; margin-bottom: 12px; color: #DC2626;">
            7. SOLUCIÓN GENERAL
        </div>
        <table style="border-collapse: collapse; border: none; margin: 6px 0;">
            <tr>
                <td style="vertical-align: middle; padding-right: 8px; font-weight: bold; font-size: 15px; color: #000000;">X =</td>
                <td style="vertical-align: middle;">{_render_vector_html(res.regresiva.vector_x.a_lista())}</td>
                <td style="vertical-align: middle; padding-left: 28px;">
                    {''.join(soluciones_txt)}
                </td>
            </tr>
        </table>
    </div>
    """
    return ("Solución General", html)
