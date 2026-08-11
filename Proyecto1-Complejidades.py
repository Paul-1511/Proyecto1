"""
Proyecto 1 - Logica Matematica

"""

import random
import sys
import time
import math

sys.setrecursionlimit(100_000)


# ---------------------------------------------------------------------------
# 1) O(lg n): Busqueda binaria
#    Recurrencia: T(n) = T(n/2) + c   -> T(n) = Theta(log n)
# ---------------------------------------------------------------------------
def busqueda_binaria(arr, objetivo, contador):
    izq, der = 0, len(arr) - 1
    while izq <= der:
        contador[0] += 1  # comparacion principal del ciclo
        medio = (izq + der) // 2
        if arr[medio] == objetivo:
            return medio
        elif arr[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1


# ---------------------------------------------------------------------------
# 2) O(n): Busqueda del maximo (version recursiva, para reflejar T(n)=T(n-1)+c)
#    Recurrencia: T(n) = T(n-1) + c   -> T(n) = Theta(n)
# ---------------------------------------------------------------------------
def encontrar_maximo(arr, contador, i=0):
    contador[0] += 1  # cada llamada hace 1 comparacion
    if i == len(arr) - 1:
        return arr[i]
    max_resto = encontrar_maximo(arr, contador, i + 1)
    return arr[i] if arr[i] > max_resto else max_resto


# ---------------------------------------------------------------------------
# 3) O(n lg n): Merge Sort
#    Recurrencia: T(n) = 2T(n/2) + c*n   -> T(n) = Theta(n log n)
# ---------------------------------------------------------------------------
def merge_sort(arr, contador):
    if len(arr) <= 1:
        return arr[:]
    medio = len(arr) // 2
    izq = merge_sort(arr[:medio], contador)
    der = merge_sort(arr[medio:], contador)
    return _merge(izq, der, contador)


def _merge(izq, der, contador):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        contador[0] += 1  # comparacion durante el merge
        if izq[i] <= der[j]:
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


# ---------------------------------------------------------------------------
# 4) O(n^2): Insertion Sort (peor caso: arreglo en orden descendente)
#    Recurrencia: T(n) = T(n-1) + c*n   -> T(n) = Theta(n^2)
# ---------------------------------------------------------------------------
def insertion_sort(arr, contador):
    a = arr[:]
    for i in range(1, len(a)):
        clave = a[i]
        j = i - 1
        while j >= 0:
            contador[0] += 1  # comparacion clave vs a[j]
            if a[j] > clave:
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = clave
    return a


# ---------------------------------------------------------------------------
# Verificacion empirica: para cada algoritmo se corre con varios tamanos de n
# y se compara el conteo de operaciones contra f(n) teorica.
# ---------------------------------------------------------------------------
def verificar_binaria(tamanos):
    print("\n=== O(lg n): Busqueda binaria ===")
    print(f"{'n':>10} {'ops':>10} {'log2(n)':>10} {'ops/log2(n)':>14} {'tiempo(s)':>12}")
    for n in tamanos:
        arr = sorted(random.sample(range(n * 10), n))
        objetivo = -1  # peor caso: no esta en el arreglo -> recorre todos los niveles
        contador = [0]
        t0 = time.perf_counter()
        busqueda_binaria(arr, objetivo, contador)
        t1 = time.perf_counter()
        f_n = math.log2(n)
        print(f"{n:>10} {contador[0]:>10} {f_n:>10.2f} {contador[0]/f_n:>14.3f} {t1 - t0:>12.8f}")


def verificar_maximo(tamanos):
    print("\n=== O(n): Busqueda del maximo (recursiva) ===")
    print(f"{'n':>10} {'ops':>10} {'n':>10} {'ops/n':>14} {'tiempo(s)':>12}")
    for n in tamanos:
        arr = random.sample(range(n * 10), n)
        contador = [0]
        t0 = time.perf_counter()
        encontrar_maximo(arr, contador)
        t1 = time.perf_counter()
        print(f"{n:>10} {contador[0]:>10} {n:>10} {contador[0]/n:>14.3f} {t1 - t0:>12.8f}")


def verificar_merge_sort(tamanos):
    print("\n=== O(n lg n): Merge Sort ===")
    print(f"{'n':>10} {'ops':>10} {'n*log2(n)':>12} {'ops/(n*log2n)':>16} {'tiempo(s)':>12}")
    for n in tamanos:
        arr = random.sample(range(n * 10), n)
        contador = [0]
        t0 = time.perf_counter()
        merge_sort(arr, contador)
        t1 = time.perf_counter()
        f_n = n * math.log2(n)
        print(f"{n:>10} {contador[0]:>10} {f_n:>12.1f} {contador[0]/f_n:>16.3f} {t1 - t0:>12.8f}")


def verificar_insertion_sort(tamanos):
    print("\n=== O(n^2): Insertion Sort (peor caso) ===")
    print(f"{'n':>10} {'ops':>10} {'n^2':>12} {'ops/n^2':>14} {'tiempo(s)':>12}")
    for n in tamanos:
        arr = list(range(n, 0, -1))  # peor caso: orden descendente
        contador = [0]
        t0 = time.perf_counter()
        insertion_sort(arr, contador)
        t1 = time.perf_counter()
        f_n = n ** 2
        print(f"{n:>10} {contador[0]:>10} {f_n:>12} {contador[0]/f_n:>14.4f} {t1 - t0:>12.8f}")


if __name__ == "__main__":
    random.seed(42)

    verificar_binaria([100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000])
    verificar_maximo([[100, 500, 1_000, 2_000, 4_000, 8_000]])
    verificar_merge_sort([1_000, 2_000, 4_000, 8_000, 16_000, 32_000])
    verificar_insertion_sort([100, 200, 400, 800, 1_600])

    print("\nNota: la columna 'ops/f(n)' deberia mantenerse aproximadamente")
    print("constante (o converger a una constante) si el algoritmo en efecto")
    print("tiene esa complejidad, confirmando la relacion de recurrencia resuelta.")