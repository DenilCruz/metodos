"""
Funciones auxiliares y formateadores comunes para la representación matemática.
Estilo: Minimalista académico (texto negro, fondo blanco puro estilo papel).
"""

from typing import List, Optional


def _formatear_numero(val: float) -> str:
    """Formatea números reales evitando decimales innecesarios (ej. 3.0 -> 3)."""
    if abs(val - round(val)) < 1e-9:
        return f"{int(round(val))}"
    return f"{val:.4f}".rstrip('0').rstrip('.')


def _quitar_parentesis_externos(s: str) -> str:
    """Quita únicamente el par de paréntesis más externo si envuelve toda la expresión."""
    s = s.strip()
    if s.startswith("(") and s.endswith(")"):
        balance = 0
        for i, char in enumerate(s):
            if char == "(":
                balance += 1
            elif char == ")":
                balance -= 1
                if balance == 0 and i < len(s) - 1:
                    return s
        if balance == 0:
            return s[1:-1].strip()
    return s


def _extraer_radicando(s: str) -> str:
    """Extrae el contenido de una raíz √( ... ) sin eliminar paréntesis internos."""
    s = s.strip()
    if s.startswith("√(") and s.endswith(")"):
        return s[2:-1].strip()
    if s.startswith("√"):
        return s[1:].strip()
    return s


def _render_matriz_html(datos: List[List[float]]) -> str:
    """Genera una tabla HTML con corchetes negros estilo notación matricial sobre papel."""
    num_filas = len(datos)
    filas_html = []
    
    for i, fila in enumerate(datos):
        celdas = []
        estilo_izq = "border-left: 2px solid #000000; width: 4px;"
        estilo_der = "border-right: 2px solid #000000; width: 4px;"

        if i == 0:
            estilo_izq += " border-top: 2px solid #000000;"
            estilo_der += " border-top: 2px solid #000000;"
        if i == num_filas - 1:
            estilo_izq += " border-bottom: 2px solid #000000;"
            estilo_der += " border-bottom: 2px solid #000000;"

        celdas.append(f"<td style='{estilo_izq}'></td>")

        for val in fila:
            txt = _formatear_numero(val)
            if not txt.startswith("-"):
                txt = f"&nbsp;{txt}&nbsp;"
            celdas.append(
                f"<td style='padding: 3px 8px; text-align: center; color: #000000; font-weight: 600; font-family: Consolas, monospace; font-size: 14px; white-space: nowrap;'>"
                f"{txt}</td>"
            )

        celdas.append(f"<td style='{estilo_der}'></td>")
        filas_html.append(f"<tr>{''.join(celdas)}</tr>")

    return (
        f"<table style='display: inline-table; vertical-align: middle; border-collapse: collapse; margin: 2px 4px;'>"
        f"{''.join(filas_html)}"
        f"</table>"
    )


def _render_vector_html(datos: List[float], nombres: Optional[List[str]] = None) -> str:
    """Genera un vector columna HTML con corchetes negros sobre papel."""
    num_filas = len(datos)
    filas_html = []
    
    for i, val in enumerate(datos):
        texto = nombres[i] if nombres else _formatear_numero(val)
        estilo_izq = "border-left: 2px solid #000000; width: 4px;"
        estilo_der = "border-right: 2px solid #000000; width: 4px;"

        if i == 0:
            estilo_izq += " border-top: 2px solid #000000;"
            estilo_der += " border-top: 2px solid #000000;"
        if i == num_filas - 1:
            estilo_izq += " border-bottom: 2px solid #000000;"
            estilo_der += " border-bottom: 2px solid #000000;"

        filas_html.append(
            f"<tr>"
            f"<td style='{estilo_izq}'></td>"
            f"<td style='padding: 3px 8px; text-align: center; color: #000000; font-weight: 600; font-family: Consolas, monospace; font-size: 14px; white-space: nowrap;'>{texto}</td>"
            f"<td style='{estilo_der}'></td>"
            f"</tr>"
        )

    return (
        f"<table style='display: inline-table; vertical-align: middle; border-collapse: collapse; margin: 2px 4px;'>"
        f"{''.join(filas_html)}"
        f"</table>"
    )


def _render_ecuacion_fraccion_html(nombre: str, formula_simb: str, numerador: str, denominador: str, resultado: str) -> str:
    """Renderiza una ecuación matemática con fracción limpia en blanco y negro."""
    return f"""
    <table style="border-collapse: collapse; margin: 5px 0 5px 16px;">
        <tr>
            <td style="color: #000000; font-weight: bold; font-family: Consolas, monospace; font-size: 14px; padding-right: 6px; vertical-align: middle; white-space: nowrap;">{nombre} =</td>
            <td style="vertical-align: middle;">
                <table style="border-collapse: collapse; text-align: center;">
                    <tr><td style="border-bottom: 1.5px solid #000000; padding: 0 4px; text-align: center; color: #000000; font-family: Consolas, monospace; font-size: 13px; white-space: nowrap;">{numerador}</td></tr>
                    <tr><td style="padding: 0 4px; text-align: center; color: #000000; font-family: Consolas, monospace; font-size: 13px; white-space: nowrap;">{denominador}</td></tr>
                </table>
            </td>
            <td style="vertical-align: middle; padding: 0 8px; font-weight: bold; font-family: Consolas, monospace; font-size: 14px; color: #000000;">=</td>
            <td style="color: #000000; font-weight: bold; font-family: Consolas, monospace; font-size: 15px; vertical-align: middle; white-space: nowrap;">{resultado}</td>
        </tr>
    </table>
    """


def _render_ecuacion_raiz_html(nombre: str, formula_simb: str, radicando_str: str, resultado: str) -> str:
    """Renderiza una ecuación con raíz cuadrada en blanco y negro."""
    return f"""
    <div style="margin: 5px 0 5px 16px; padding: 2px 0; font-family: Consolas, monospace; font-size: 14px; color: #000000;">
        <span style="font-weight: bold;">{nombre}</span> = √({radicando_str}) = <b>{resultado}</b>
    </div>
    """


def envolver_html_paso(contenido_html: str) -> str:
    """Envuelve un bloque de contenido en el contenedor con estilo de hoja de papel blanca."""
    return f"""
    <div style="font-family: 'Segoe UI', Arial, 'Times New Roman', sans-serif; color: #000000; background-color: #FFFFFF; padding: 20px 24px; line-height: 1.6;">
        {contenido_html}
    </div>
    """
