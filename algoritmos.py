import random
import time
import multiprocessing
from collections import deque
from typing import List, Tuple, Dict, Optional, Any

# --- BUSQUEDA Y ORDENAMIENTO ---

def busqueda_binaria(lista_productos, id_buscado):
    # Clasico algoritmo de busqueda binaria para encontrar un ID rapido
    inicio = 0
    fin = len(lista_productos) - 1
    
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista_productos[medio]['id'] == id_buscado:
            return medio
        elif lista_productos[medio]['id'] < id_buscado:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1

def quick_sort(lista, clave='id'):
    # Ordenamiento rapido usando recursion y pivote central
    if len(lista) <= 1:
        return lista
    
    pivote = lista[len(lista) // 2][clave]
    menores = [x for x in lista if x[clave] < pivote]
    iguales = [x for x in lista if x[clave] == pivote]
    mayores = [x for x in lista if x[clave] > pivote]
    
    return quick_sort(menores, clave) + iguales + quick_sort(mayores, clave)

def merge_sort(lista, clave='ventas_totales'):
    # Algoritmo de Divide y Venceras: util para rankings estables
    if len(lista) <= 1:
        return lista
    
    mitad = len(lista) // 2
    izquierda = merge_sort(lista[:mitad], clave)
    derecha = merge_sort(lista[mitad:], clave)
    
    return mezclar_listas(izquierda, derecha, clave)

def mezclar_listas(izq, der, clave):
    # Funcion para unir las dos mitades ordenadas
    resultado = []
    i = 0
    j = 0
    
    while i < len(izq) and j < len(der):
        # Ordenamos de mayor a menor para que el ranking sea mas facil de leer
        if izq[i][clave] > der[j][clave]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
            
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

# --- PROGRAMACION DINAMICA ---

def mochila_01(capacidad_maxima, productos_disponibles):
    # Resolvemos el problema de la mochila y devolvemos que productos se eligieron
    cantidad_items = len(productos_disponibles)
    # Creamos la matriz llena de ceros
    matriz_dp = [[0 for _ in range(capacidad_maxima + 1)] for _ in range(cantidad_items + 1)]
    
    for i in range(cantidad_items + 1):
        for peso_actual in range(capacidad_maxima + 1):
            if i == 0 or peso_actual == 0:
                matriz_dp[i][peso_actual] = 0
            else:
                costo_item = int(productos_disponibles[i-1]['costo'])
                prioridad_item = productos_disponibles[i-1]['prioridad']
                
                if costo_item <= peso_actual:
                    # Decidimos si nos conviene mas llevarlo o no
                    matriz_dp[i][peso_actual] = max(
                        prioridad_item + matriz_dp[i-1][peso_actual - costo_item], 
                        matriz_dp[i-1][peso_actual]
                    )
                else:
                    matriz_dp[i][peso_actual] = matriz_dp[i-1][peso_actual]
    
    # Ahora retrocedemos en la matriz para saber cuales fueron los elegidos
    elegidos = []
    puntos_totales = matriz_dp[cantidad_items][capacidad_maxima]
    peso_temp = capacidad_maxima
    
    for i in range(cantidad_items, 0, -1):
        if puntos_totales <= 0:
            break
        if puntos_totales != matriz_dp[i-1][peso_temp]:
            # Este item si fue elegido
            elegidos.append(productos_disponibles[i-1])
            puntos_totales -= productos_disponibles[i-1]['prioridad']
            peso_temp -= int(productos_disponibles[i-1]['costo'])
            
    return matriz_dp[cantidad_items][capacidad_maxima], elegidos

def fibonacci_tab(periodo_años):
    # Genera la secuencia completa usando tabulacion
    if periodo_años <= 0: return [0]
    if periodo_años == 1: return [0, 1]
    
    tabla = [0] * (periodo_años + 1)
    tabla[1] = 1
    for i in range(2, periodo_años + 1):
        tabla[i] = tabla[i-1] + tabla[i-2]
    return tabla

# --- ALGORITMOS VORACES ---

def cambio_monedas(paga, costo):
    # Algoritmo voraz para dar el vuelto mas eficiente
    vuelto_pendiente = round(paga - costo, 2)
    billetes_monedas = [200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1]
    resultado_desglose = {}
    
    for valor in billetes_monedas:
        if vuelto_pendiente >= valor:
            cantidad = int(vuelto_pendiente // valor)
            if cantidad > 0:
                resultado_desglose[valor] = cantidad
                vuelto_pendiente = round(vuelto_pendiente % valor, 2)
    return resultado_desglose

# --- GRAFOS Y BACKTRACKING ---

def recorrer_bfs(grafo_red, punto_inicio, punto_final):
    # Busqueda en anchura para encontrar la ruta mas corta
    nodos_visitados = {punto_inicio: None}
    cola_proceso = deque([punto_inicio])
    
    while cola_proceso:
        nodo_actual = cola_proceso.popleft()
        if nodo_actual == punto_final:
            # Si llegamos, reconstruimos el camino hacia atras
            camino_final = []
            while nodo_actual is not None:
                camino_final.append(nodo_actual)
                nodo_actual = nodos_visitados[nodo_actual]
            return camino_final[::-1]
        
        for vecino in grafo_red.get(nodo_actual, []):
            if vecino not in nodos_visitados:
                nodos_visitados[vecino] = nodo_actual
                cola_proceso.append(vecino)
    return None

def resolver_n_reinas(cuadricula, columna_actual):
    # Algoritmo de Backtracking para poner las fichas sin ataques
    if columna_actual >= len(cuadricula):
        return True
    
    for fila in range(len(cuadricula)):
        if es_posicion_segura(cuadricula, fila, columna_actual):
            cuadricula[fila][columna_actual] = 1
            if resolver_n_reinas(cuadricula, columna_actual + 1):
                return True
            # Si no funciono, limpiamos (Retroceso)
            cuadricula[fila][columna_actual] = 0
    return False

def es_posicion_segura(tab, f, c):
    # Verifica ataques en horizontal y diagonales
    for i in range(c):
        if tab[f][i] == 1: return False
    for i, j in zip(range(f, -1, -1), range(c, -1, -1)):
        if tab[i][j] == 1: return False
    for i, j in zip(range(f, len(tab)), range(c, -1, -1)):
        if tab[i][j] == 1: return False
    return True

# --- PROBABILISTICOS ---

def simular_riesgo_stock(unidades_actuales, venta_promedio, dias_totales):
    # Metodo de Montecarlo para calcular riesgo de quiebre de stock
    simulaciones_totales = 5000
    casos_con_exito = 0 # Dias donde el stock NO se acabo
    
    for _ in range(simulaciones_totales):
        stock_temporal = unidades_actuales
        se_agoto = False
        for _ in range(dias_totales):
            # Simulamos demanda aleatoria alrededor del promedio
            demanda_del_dia = random.randint(0, venta_promedio * 2)
            stock_temporal -= demanda_del_dia
            if stock_temporal < 0:
                se_agoto = True
                break
        if not se_agoto:
            casos_con_exito += 1
            
    # Calculamos el porcentaje de riesgo (lo opuesto a la tasa de exito)
    tasa_exito = casos_con_exito / simulaciones_totales
    porcentaje_riesgo = (1 - tasa_exito) * 100
    return porcentaje_riesgo
