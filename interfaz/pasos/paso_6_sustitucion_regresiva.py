"""
Paso 6: Encontrar las incógnitas mediante sustitución regresiva (Lᵀ · X = D).
"""

from typing import Tuple, Optional
from logica.cholesky import ResultadoCompletoCholesky
from interfaz.pasos.comun import (
    _formatear_numero, _render_matriz_html, 
    _render_vector_html, _render_ecuacion_fraccion_html,
    _quitar_parentesis_externos
)


def generar_paso_6(res: ResultadoCompletoCholesky) -> Optional[Tuple[str, str]]:
    """Retorna (titulo, html) para el Paso 6, o None si no hay sustitución regresiva."""
    if not res.regresiva or not res.descomposicion or not res.progresiva:
        return None

    n = res.matriz_a.filas
    nombres_vars = [f"x{i+1}" for i in range(n)]

    pasos_reg_html = []
    for paso in res.regresiva.pasos:
        nombre = paso.nombre_variable
        partes = paso.sustitucion_numerica.split(" / ")
        if len(partes) == 2:
            num_str = _quitar_parentesis_externos(partes[0])
            den_str = partes[1]
            pasos_reg_html.append(_render_ecuacion_fraccion_html(nombre, paso.formula_simbolica, num_str, den_str, _formatear_numero(paso.valor)))
        else:
            pasos_reg_html.append(f"""
            <div style="margin: 5px 0 5px 16px; padding: 2px 0; font-family: Consolas, monospace; font-size: 14px; color: #000000;">
                <span style="font-weight: bold;">{nombre}</span> = {paso.sustitucion_numerica} = <b>{_formatear_numero(paso.valor)}</b>
            </div>
            """)

    html = f"""
    <div id="paso_5" style="margin-bottom: 24px;">
        <div style="font-weight: bold; font-size: 15px; border-bottom: 1.5px solid #DC2626; padding-bottom: 3px; margin-bottom: 12px; color: #DC2626;">
            6. ENCONTRAMOS LOS VALORES DE LAS INCÓGNITAS (SUSTITUCIÓN REGRESIVA: Lᵀ · X = D)
        </div>
        <table style="border-collapse: collapse; border: none; margin: 6px 0;">
            <tr>
                <td style="vertical-align: middle;">{_render_matriz_html(res.descomposicion.matriz_lt.a_lista())}</td>
                <td style="vertical-align: middle;">{_render_vector_html([0.0]*n, nombres_vars)}</td>
                <td style="vertical-align: middle; padding: 0 10px; font-weight: bold; font-size: 15px; color: #000000;">=</td>
                <td style="vertical-align: middle;">{_render_vector_html(res.progresiva.vector_d.a_lista())}</td>
            </tr>
        </table>
        <div style="margin-top: 12px;">
            {''.join(pasos_reg_html)}
        </div>
    </div>
    """
    return ("Sustitución Regresiva (Lᵀ · X = D)", html)
