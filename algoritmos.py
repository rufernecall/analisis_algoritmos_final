from typing import List, Tuple, Dict, Optional, Final

# Tipado estricto para claridad arquitectonica
Producto = Dict[str, any]
DesgloseCambio = Dict[float, int]

# --- MODULO DE ALGORITMOS DE OPTIMIZACION ---

def busqueda_binaria(arreglo: List[Producto], id_objetivo: int) -> Optional[Producto]:
    """
    Busqueda Binaria para consulta rapida de stock.
    Complejidad: O(log n)
    Precondicion: El arreglo debe estar ordenado por 'id'.
    """
    bajo: int = 0
    alto: int = len(arreglo) - 1
    
    while bajo <= alto:
        medio: int = (bajo + alto) // 2
        id_actual: int = arreglo[medio]['id']
        
        if id_actual == id_objetivo:
            return arreglo[medio]
        elif id_actual < id_objetivo:
            bajo = medio + 1
        else:
            alto = medio - 1
    return None

def cambio_monedas_voraz(monto: float, denominaciones: List[float]) -> DesgloseCambio:
    """
    Algoritmo Voraz para la entrega optima de vuelto (Coin Change).
    Complejidad: O(D log D) por el sort, O(D) para la iteracion.
    Donde D es el numero de denominaciones.
    """
    # Se asegura el orden descendente para cumplir la propiedad voraz
    denominaciones_ordenadas: List[float] = sorted(denominaciones, reverse=True)
    cambio: DesgloseCambio = {}
    restante: float = round(monto, 2)
    
    for moneda in denominaciones_ordenadas:
        if restante >= moneda:
            cantidad: int = int(restante // moneda)
            if cantidad > 0:
                cambio[moneda] = cantidad
                restante = round(restante % moneda, 2)
    
    return cambio

def mochila_reabastecimiento(capacidad: float, items: List[Producto]) -> Tuple[float, List[Producto]]:
    """
    Problema de la Mochila 0/1 para reabastecimiento bajo presupuesto limite.
    Complejidad: O(n * W)
    Donde n es el numero de items y W la capacidad (presupuesto).
    """
    n: int = len(items)
    W: int = int(capacidad)
    
    # Matriz de programacion dinamica
    dp: List[List[int]] = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item: Producto = items[i-1]
        costo: int = int(item['costo'])
        prioridad: int = item['prioridad']
        
        for w in range(W + 1):
            if costo <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - costo] + prioridad)
            else:
                dp[i][w] = dp[i-1][w]
                
    # Reconstruccion de la solucion optima
    seleccionados: List[Producto] = []
    w_restante: int = W
    for i in range(n, 0, -1):
        if dp[i][w_restante] != dp[i-1][w_restante]:
            seleccionados.append(items[i-1])
            w_restante -= int(items[i-1]['costo'])
            
    return float(dp[n][W]), seleccionados

# Memoizacion para calculo de Fibonacci optimo
_memo_fib: Dict[int, int] = {0: 0, 1: 1}

def get_fib(n: int) -> int:
    """Calculo de Fibonacci con Programacion Dinamica (Memoizacion)."""
    if n in _memo_fib:
        return _memo_fib[n]
    _memo_fib[n] = get_fib(n - 1) + get_fib(n - 2)
    return _memo_fib[n]

def busqueda_fibonacci(arreglo: List[Producto], stock_objetivo: int) -> int:
    """
    Busqueda Fibonacci para optimizacion de consultas por stock.
    Complejidad: O(log n)
    Precondicion: El arreglo debe estar ordenado por 'stock'.
    """
    n: int = len(arreglo)
    k: int = 0
    while get_fib(k) < n:
        k += 1
    
    offset: int = -1
    
    while get_fib(k) > 1:
        i: int = min(offset + get_fib(k - 2), n - 1)
        
        if arreglo[i]['stock'] < stock_objetivo:
            k -= 1
            offset = i
        elif arreglo[i]['stock'] > stock_objetivo:
            k -= 2
        else:
            return i
            
    if n > 0 and (offset + 1) < n and arreglo[offset + 1]['stock'] == stock_objetivo:
        return offset + 1
        
    return -1
