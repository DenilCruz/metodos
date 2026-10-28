from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Matriz:
    """
    Representa una matriz y operaciones elementales de matriz.
    """
    datos: Tuple[Tuple[float, ...], ...]
    filas: int
    columnas: int

    @classmethod
    def desde_lista_2d(cls, valores: List[List[float]]) -> 'Matriz':
        if not valores or not valores[0]:
            raise ValueError("La matriz no puede estar vacía.")
        num_filas = len(valores)
        num_columnas = len(valores[0])
        for fila in valores:
            if len(fila) != num_columnas:
                raise ValueError("Todas las filas deben tener el mismo número de columnas.")
        datos_tupla = tuple(tuple(float(x) for x in fila) for fila in valores)
        return cls(datos=datos_tupla, filas=num_filas, columnas=num_columnas)

    @classmethod
    def ceros(cls, filas: int, columnas: int) -> 'Matriz':
        datos = tuple(tuple(0.0 for _ in range(columnas)) for _ in range(filas))
        return cls(datos=datos, filas=filas, columnas=columnas)

    @property
    def es_cuadrada(self) -> bool:
        return self.filas == self.columnas

    def obtener(self, i: int, j: int) -> float:
        return self.datos[i][j]

    def a_lista(self) -> List[List[float]]:
        return [list(fila) for fila in self.datos]

    def transponer(self) -> 'Matriz':
        datos_transpuestos = tuple(
            tuple(self.datos[r][c] for r in range(self.filas))
            for c in range(self.columnas)
        )
        return Matriz(datos=datos_transpuestos, filas=self.columnas, columnas=self.filas)

    def es_simetrica(self, tolerancia: float = 1e-9) -> bool:
        if not self.es_cuadrada:
            return False
        for i in range(self.filas):
            for j in range(i + 1, self.columnas):
                if abs(self.datos[i][j] - self.datos[j][i]) > tolerancia:
                    return False
        return True


@dataclass(frozen=True)
class Vector:
    """
    Representa un vector
    """
    datos: Tuple[float, ...]
    tamano: int

    @classmethod
    def desde_lista(cls, valores: List[float]) -> 'Vector':
        datos_tupla = tuple(float(x) for x in valores)
        return cls(datos=datos_tupla, tamano=len(datos_tupla))

    def obtener(self, i: int) -> float:
        return self.datos[i]

    def a_lista(self) -> List[float]:
        return list(self.datos)
