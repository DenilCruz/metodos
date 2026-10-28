# metodos

Calculadora interactiva del **Método de Cholesky** para la resolución de sistemas de ecuaciones lineales y descomposición matricial ($A = L \cdot L^T$).

## Características
- **Paso 1:** Planteamiento del sistema de ecuaciones ($A \cdot X = B$).
- **Paso 2:** Comprobación formal de simetría ($A = A^T$).
- **Paso 3:** Comprobación de matriz definida positiva mediante el Criterio de Sylvester ($\Delta_{kk} > 0$).
- **Paso 4:** Descomposición de Cholesky ($A = L \cdot L^T$) paso a paso con fórmulas.
- **Paso 5:** Sustitución progresiva hacia adelante ($L \cdot D = B$).
- **Paso 6:** Sustitución regresiva hacia atrás ($L^T \cdot X = D$).
- **Paso 7:** Solución general consolidada del vector incógnita $X$.
- Interfaz gráfica de usuario con PyQt6.

## Requisitos y Ejecución
```bash
pip install PyQt6
python main.py
```
