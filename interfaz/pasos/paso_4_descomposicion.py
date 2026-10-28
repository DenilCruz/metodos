"""
Paso 4: Descomposición de Cholesky A = L · Lᵀ (cálculo de cada L_ki paso a paso).
"""

from typing import Tuple, Optional
from logica.cholesky import ResultadoCompletoCholesky
from interfaz.pasos.comun import (
    _formatear_numero, _render_matriz_html, 
    _render_ecuacion_fraccion_html, _render_ecuacion_raiz_html,
    _quitar_parentesis_externos, _extraer_radicando
)


def generar_paso_4(res: ResultadoCompletoCholesky) -> Optional[Tuple[str, str]]:
    """Retorna (titulo, html) para el Paso 4, o None si no se pudo descomponer."""
    if not res.exito or not res.descomposicion:
        return None

    bloques_etapas = []
    for etapa in res.descomposicion.etapas:
        pasos_etapa_html = []
        pasos_etapa_html.append(f"""
        <div style="margin-top: 14px; margin-bottom: 6px; font-weight: bold; text-decoration: underline; color: #000000;">
            Etapa K = {etapa.k}:
        </div>
        """)
        for paso in etapa.pasos:
            nombre = f"L<sub>{paso.k}{paso.i}</sub>"
            if paso.es_diagonal:
                rad_str = _extraer_radicando(paso.sustitucion_numerica)
                pasos_etapa_html.append(_render_ecuacion_raiz_html(nombre, paso.formula_simbolica, rad_str, _formatear_numero(paso.valor)))
            else:
                partes = paso.sustitucion_numerica.split(" / ")
                if len(partes) == 2:
                    num_str = _quitar_parentesis_externos(partes[0])
                    den_str = partes[1]
                    pasos_etapa_html.append(_render_ecuacion_fraccion_html(nombre, paso.formula_simbolica, num_str, den_str, _formatear_numero(paso.valor)))
                else:
                    pasos_etapa_html.append(f"""
                    <div style="margin: 5px 0 5px 16px; padding: 2px 0; font-family: Consolas, monospace; font-size: 14px; color: #000000;">
                        <span style="font-weight: bold;">{nombre}</span> = {paso.sustitucion_numerica} = <b>{_formatear_numero(paso.valor)}</b>
                    </div>
                    """)
        bloques_etapas.append("".join(pasos_etapa_html))

    html = f"""
    <div id="paso_3" style="margin-bottom: 24px;">
        <div style="font-weight: bold; font-size: 15px; border-bottom: 1.5px solid #DC2626; padding-bottom: 3px; margin-bottom: 12px; color: #DC2626;">
            4. DESCOMPONER A = L · Lᵀ (ALGORITMO DE CHOLESKY)
        </div>
        {''.join(bloques_etapas)}
        <div style="margin-top: 16px;">
            <div style="font-weight: bold; margin-bottom: 8px; color: #000000;">Matriz factorizada A = L · Lᵀ:</div>
            <table style="border-collapse: collapse; border: none; margin: 6px 0;">
                <tr>
                    <td style="vertical-align: middle;">{_render_matriz_html(res.descomposicion.matriz_l.a_lista())}</td>
                    <td style="vertical-align: middle; padding: 0 8px; font-size: 16px; font-weight: bold; color: #000000;">·</td>
                    <td style="vertical-align: middle;">{_render_matriz_html(res.descomposicion.matriz_lt.a_lista())}</td>
                </tr>
            </table>
        </div>
    </div>
    """
    return ("Descomposición Cholesky", html)
