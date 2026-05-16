import os
import time
import multiprocessing
from typing import List, Dict
from algoritmos import (
    busqueda_binaria, 
    cambio_monedas, 
    mochila_01, 
    fibonacci_tab,
    quick_sort,
    merge_sort,
    resolver_n_reinas,
    recorrer_bfs,
    simular_riesgo_stock
)

# --- BASE DE DATOS EN MEMORIA ---

inventario = [
    {"id": 101, "nombre": "Paracetamol 500mg", "stock": 50, "precio": 5.0, "costo": 3.0, "prioridad": 7, "ventas_totales": 120},
    {"id": 105, "nombre": "Ibuprofeno 400mg", "stock": 120, "precio": 8.5, "costo": 4.0, "prioridad": 7, "ventas_totales": 85},
    {"id": 110, "nombre": "Amoxicilina 500mg", "stock": 30, "precio": 15.0, "costo": 10.0, "prioridad": 10, "ventas_totales": 40},
    {"id": 115, "nombre": "Loratadina 10mg", "stock": 200, "precio": 12.0, "costo": 6.0, "prioridad": 4, "ventas_totales": 150},
    {"id": 120, "nombre": "Omeprazol 20mg", "stock": 15, "precio": 20.0, "costo": 12.0, "prioridad": 10, "ventas_totales": 200},
]

# Historial para guardar las ventas y calcular ganancias
historial_ventas = [] 

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input("\nPresiona Enter para continuar...")

def animacion_espera(mensaje):
    print(mensaje, end="", flush=True)
    for _ in range(3):
        time.sleep(0.2)
        print(".", end="", flush=True)
    print()

# --- MODULO 1: GESTION DE PRODUCTOS ---

def gestionar_inventario():
    global inventario
    while True:
        limpiar_consola()
        # Ordenamos por ID usando Quick Sort
        inventario = quick_sort(inventario, 'id')
        
        print("=== GESTION DE INVENTARIO (Quick Sort) ===")
        print(f"{'ID':<5} | {'Nombre':<25} | {'Stock':<6} | {'Precio':<8} | {'Prioridad':<10}")
        print("-" * 65)
        
        # Mapa para que sea mas amigable leer la prioridad
        nombres_prioridad = {10: "CRITICO", 7: "ALTO", 4: "MEDIO", 2: "BAJO", 5: "NORMAL"}
        
        for p in inventario:
            prio_texto = nombres_prioridad.get(p['prioridad'], "NORMAL")
            print(f"{p['id']:<5} | {p['nombre']:<25} | {p['stock']:<6} | S/{p['precio']:<7.2f} | {prio_texto:<10}")
        
        print("\n1. Añadir nuevo producto")
        print("2. Buscar producto por ID (Busqueda Binaria)")
        print("0. Volver al menu principal")
        opcion = input("\nElige una opcion: ")
        
        if opcion == "0":
            break
        elif opcion == "1":
            try:
                nuevo_id = int(input("ID del producto: "))
                nombre = input("Nombre: ")
                stock_inicial = int(input("Stock inicial: "))
                precio_venta = float(input("Precio de venta: "))
                costo_compra = float(input("Costo de compra: "))
                
                print("\nNivel de Importancia:")
                print("1. Critico | 2. Alto | 3. Medio | 4. Bajo")
                p_op = input("Elige nivel: ")
                niveles = {"1": 10, "2": 7, "3": 4, "4": 2}
                prioridad = niveles.get(p_op, 5)
                
                inventario.append({
                    "id": nuevo_id, "nombre": nombre, "stock": stock_inicial, 
                    "precio": precio_venta, "costo": costo_compra, 
                    "prioridad": prioridad, "ventas_totales": 0
                })
                animacion_espera("Guardando en la base de datos")
            except:
                print("Hubo un error en los datos. Intentalo de nuevo.")
                pausa()
        elif opcion == "2":
            try:
                id_a_buscar = int(input("Ingresa el ID que buscas: "))
                indice = busqueda_binaria(inventario, id_a_buscar)
                if indice != -1:
                    prod = inventario[indice]
                    print(f"\nPRODUCTO ENCONTRADO: {prod['nombre']}")
                    print(f"Stock: {prod['stock']} | Precio: S/{prod['precio']}")
                else:
                    print("\nNo se encontro ningun producto con ese ID.")
                pausa()
            except:
                pass

# --- MODULO 2: CAJA Y VENTAS ---

def iniciar_venta():
    carrito_compras = []
    while True:
        limpiar_consola()
        
        # Agrupamos los items del carrito para mostrarlos ordenados
        items_agrupados = {}
        for item in carrito_compras:
            id_p = item['id']
            if id_p in items_agrupados:
                items_agrupados[id_p]['cantidad'] += item['cantidad']
            else:
                items_agrupados[id_p] = item.copy()
        
        monto_total = sum(i['precio'] * i['cantidad'] for i in items_agrupados.values())
        
        print("=== PUNTO DE VENTA (Caja) ===")
        print(f"Items: {len(items_agrupados)} | Total a pagar: S/{monto_total:.2f}")
        print("-" * 50)
        for i in items_agrupados.values():
            print(f"  - {i['nombre']:<20} x{i['cantidad']:>2} (S/{i['precio'] * i['cantidad']:>6.2f})")
        print("-" * 50)
        
        print("1. Agregar item por ID (Busqueda Binaria)")
        print("2. Cobrar y dar vuelto (Algoritmo Voraz)")
        print("3. Cancelar venta")
        print("0. Salir")
        
        opcion = input("\nElige una opcion: ")
        if opcion == "0":
            break
        elif opcion == "1":
            try:
                id_producto = int(input("Ingrese ID del producto: "))
                indice_inv = busqueda_binaria(inventario, id_producto)
                
                if indice_inv != -1:
                    producto_ref = inventario[indice_inv]
                    # Calculamos cuanto hay ya en el carrito para no pasarnos del stock
                    ya_en_carrito = sum(it['cantidad'] for it in carrito_compras if it['id'] == id_producto)
                    stock_real_disponible = producto_ref['stock'] - ya_en_carrito
                    
                    if stock_real_disponible > 0:
                        cantidad = int(input(f"¿Cuantos {producto_ref['nombre']}? (Max disponible: {stock_real_disponible}): "))
                        if 0 < cantidad <= stock_real_disponible:
                            carrito_compras.append({
                                "id": producto_ref['id'], 
                                "nombre": producto_ref['nombre'], 
                                "precio": producto_ref['precio'], 
                                "cantidad": cantidad
                            })
                            print("¡Agregado!")
                        else:
                            print(f"Cantidad no valida. El maximo es {stock_real_disponible}.")
                    else:
                        print("Ya no queda stock de este producto.")
                else:
                    print("Ese ID no existe en el inventario.")
            except:
                print("Error al ingresar los datos.")
            time.sleep(1)
            
        elif opcion == "2":
            if not carrito_compras:
                print("El carrito esta vacio.")
                time.sleep(1)
                continue
            
            try:
                total_venta = sum(i['precio'] * i['cantidad'] for i in carrito_compras)
                pago_cliente = float(input(f"Total: S/{total_venta:.2f} | Paga con: "))
                
                if pago_cliente >= total_venta:
                    vuelto_entregar = pago_cliente - total_venta
                    desglose_vuelto = cambio_monedas(paga=pago_cliente, costo=total_venta)
                    
                    animacion_espera("Procesando pago y calculando vuelto")
                    print(f"\nVuelto total: S/{vuelto_entregar:.2f}")
                    print("Desglose de monedas/billetes:")
                    for moneda, cant in desglose_vuelto.items():
                        print(f"  > S/{moneda}: {cant}")
                    
                    # Actualizamos el inventario y guardamos en el historial
                    costo_total_compra = 0
                    for item in carrito_compras:
                        idx = busqueda_binaria(inventario, item['id'])
                        inventario[idx]['stock'] -= item['cantidad']
                        inventario[idx]['ventas_totales'] += item['cantidad']
                        costo_total_compra += (inventario[idx]['costo'] * item['cantidad'])
                    
                    historial_ventas.append({
                        "monto_venta": total_venta, 
                        "monto_costo": costo_total_compra
                    })
                    
                    print("\nVenta terminada. ¡Gracias!")
                    carrito_compras = []
                    pausa()
                    break
                else:
                    print("El dinero no alcanza para cubrir el total.")
                    time.sleep(1)
            except:
                pass
        elif opcion == "3":
            carrito_compras = []
            print("Venta cancelada.")
            time.sleep(1)

# --- MODULO 3: REPOSICION Y ANALISIS ---

def sugerir_compras_stock():
    limpiar_consola()
    print("=== REPOSICION INTELIGENTE (Mochila 0/1) ===")
    try:
        presupuesto = int(input("¿De cuanto es el presupuesto para reponer?: "))
        # Filtramos solo los que estan bajos de stock (menos de 60)
        necesitados = [p for p in inventario if p['stock'] < 60]
        
        if necesitados:
            puntos_prio, lista_elegidos = mochila_01(presupuesto, necesitados)
            print(f"\nSugerencia para maximizar la prioridad (Total: {puntos_prio}):")
            print("-" * 65)
            
            costo_acumulado = 0
            mapa_nombres = {10: "CRITICO", 7: "ALTO", 4: "MEDIO", 2: "BAJO"}
            
            for prod in lista_elegidos:
                nom_prio = mapa_nombres.get(prod['prioridad'], "NORMAL")
                print(f"  [COMPRAR] {prod['nombre']:<25} | Costo: S/{prod['costo']:<5} | Prio: {nom_prio}")
                costo_acumulado += prod['costo']
            
            print("-" * 65)
            print(f"Inversion total: S/{costo_acumulado:.2f} | Saldo libre: S/{presupuesto - costo_acumulado:.2f}")
        else:
            print("\nTodos los productos tienen un stock saludable.")
    except:
        print("Error en el calculo.")
    pausa()

def analisis_riesgo_stock():
    limpiar_consola()
    print("=== ANALISIS DE RIESGO DE AGOTAMIENTO (Montecarlo) ===")
    try:
        id_analizar = int(input("ID del producto a analizar: "))
        idx = busqueda_binaria(inventario, id_analizar)
        if idx != -1:
            p = inventario[idx]
            ventas_promedio = int(input(f"¿Cuantas unidades se venden de {p['nombre']} al dia?: "))
            dias_proyeccion = int(input("¿Para cuantos dias quieres simular?: "))
            
            porcentaje_riesgo = simular_riesgo_stock(p['stock'], ventas_promedio, dias_proyeccion)
            
            print(f"\nRESULTADO DE LA SIMULACION:")
            print(f"Probabilidad de quedar sin stock: {porcentaje_riesgo:.2f}%")
            if porcentaje_riesgo > 50:
                print("¡ALERTA! El riesgo es muy alto. Deberias reponer pronto.")
            else:
                print("El nivel de stock parece seguro para este periodo.")
        else:
            print("No se encontro ese producto.")
    except:
        pass
    pausa()

# --- MODULO 4: LOGISTICA Y REPORTES ---

def plan_logistico_delivery():
    limpiar_consola()
    print("=== RUTAS DE ENTREGA (Grafos BFS) ===")
    # Grafo de ejemplo de la red de la farmacia
    red_locales = {
        'AlmacenCentral': ['Sucursal_Norte', 'Sucursal_Sur', 'Sucursal_Oeste'],
        'Sucursal_Norte': ['AlmacenCentral', 'Tienda_A', 'Tienda_B'],
        'Sucursal_Sur': ['AlmacenCentral', 'Tienda_C'],
        'Sucursal_Oeste': ['AlmacenCentral', 'Tienda_D'],
        'Tienda_A': ['Sucursal_Norte'], 
        'Tienda_B': ['Sucursal_Norte'], 
        'Tienda_C': ['Sucursal_Sur'], 
        'Tienda_D': ['Sucursal_Oeste']
    }
    print("Locales en la red:", ", ".join(red_locales.keys()))
    inicio = input("\n¿Donde esta el camion?: ")
    destino = input("¿Cual es el destino de entrega?: ")
    
    ruta = recorrer_bfs(red_locales, inicio, destino)
    if ruta:
        print(f"\nRUTA MAS CORTA ENCONTRADA: {' -> '.join(ruta)}")
    else:
        print("\nNo se pudo encontrar una ruta entre esos puntos.")
    pausa()

def reporte_productos_top():
    limpiar_consola()
    print("=== RANKING DE VENTAS (Merge Sort) ===")
    # Ordenamos por el campo 'ventas_totales' usando Divide y Venceras
    ranking = merge_sort(inventario, 'ventas_totales')
    
    print(f"{'Puesto':<8} | {'Nombre':<25} | {'Unidades Vendidas'}")
    print("-" * 55)
    for i, p in enumerate(ranking[:5]): # Mostramos el Top 5
        print(f"#{i+1:<7} | {p['nombre']:<25} | {p['ventas_totales']} unidades")
    pausa()

# --- MODULO 5: REPORTES DE GANANCIAS (Paralelo) ---

def calcular_ganancia_bloque(lista_sub_ventas):
    # Funcion para el procesamiento paralelo
    v_t = sum(v['monto_venta'] for v in lista_sub_ventas)
    c_t = sum(v['monto_costo'] for v in lista_sub_ventas)
    return v_t, c_t

def reporte_ganancia_neta():
    limpiar_consola()
    print("=== REPORTE DE GANANCIAS (Procesamiento Paralelo) ===")
    if not historial_ventas:
        print("\nNo hay ventas registradas para generar el reporte."); pausa(); return
    
    m = len(historial_ventas) // 2
    partes_historial = [historial_ventas[:m], historial_ventas[m:]]
    
    animacion_espera("Calculando balances con multiples nucleos")
    
    if __name__ == '__main__':
        with multiprocessing.Pool(processes=2) as pool:
            resultados = pool.map(calcular_ganancia_bloque, partes_historial)
            
            total_v = sum(r[0] for r in resultados)
            total_c = sum(r[1] for r in resultados)
            ganancia = total_v - total_c
            
            print(f"\nRESUMEN FINANCIERO:")
            print(f"  > Ventas Totales:    S/{total_v:>8.2f}")
            print(f"  > Costos Totales:    S/{total_c:>8.2f}")
            print("-" * 35)
            print(f"  > GANANCIA TOTAL:    S/{ganancia:>8.2f}")
    pausa()

# --- MODULO 6: EXPANSIÓN (Fibonacci) ---

def proyeccion_expansion():
    limpiar_consola()
    print("=== PLAN DE EXPANSION ESTRATEGICA (Fibonacci) ===")
    try:
        años = int(input("¿A cuantos años quieres proyectar la expansion?: "))
        secuencia = fibonacci_tab(años)
        
        print(f"\nProyeccion de nuevas sucursales por año:")
        for i, locales in enumerate(secuencia):
            print(f"  Año {i}: +{locales} locales nuevos")
        
        total_locales = sum(secuencia)
        print(f"\nTotal estimado al final del plan: {total_locales} sucursales.")
    except:
        pass
    pausa()

# --- MODULO 7: SEGURIDAD Y DISEÑO (Backtracking) ---

def generar_layout_seguridad():
    limpiar_consola()
    print("=== DISEÑO DE SEGURIDAD DEL ALMACEN (Backtracking) ===")
    print("Este modulo usa el algoritmo de las 8 Reinas para colocar sensores")
    print("de movimiento de forma que cubran todo el almacen sin interferencias.")
    
    # Simulamos el calculo
    animacion_espera("Calculando posiciones optimas")
    
    # Tablero de 8x8 para el almacen
    almacen_cuadricula = [[0]*8 for _ in range(8)]
    
    if resolver_n_reinas(almacen_cuadricula, 0):
        print("\nMapa optimo generado (Q = Sensor de Seguridad):")
        print("   " + " ".join(str(n) for n in range(8)))
        print("   " + "-" * 16)
        for i, fila in enumerate(almacen_cuadricula):
            print(f"{i} | " + " ".join("Q" if x == 1 else "." for x in fila))
        
        print("\nEsta configuracion garantiza cobertura total sin puntos ciegos.")
    else:
        print("\nNo se pudo encontrar una configuracion valida.")
    pausa()


# --- ACCESO Y MENU ---

def login():
    limpiar_consola()
    print("========================================")
    print("      SISTEMA FARMASYS - ACCESO         ")
    print("========================================")
    usuario = input("Usuario: ")
    clave = input("Password: ")
    return usuario == "admin" and clave == "1234"

def menu_principal():
    while True:
        limpiar_consola()
        print("========================================")
        print("             FARMASYS ERP               ")
        print("========================================")
        print("1. Inventario (Quick Sort)")
        print("2. Caja y Ventas (Voraz)")
        print("3. Reposicion (Mochila 0/1)")
        print("4. Riesgo de Stock (Montecarlo)")
        print("5. Logistica Entrega (Grafos BFS)")
        print("6. Ranking Ventas (Merge Sort)")
        print("7. Reporte Ganancias (Paralelo)")
        print("8. Plan de Expansion (Fibonacci)")
        print("9. Layout Almacen (Backtracking)")
        print("0. Salir")
        print("========================================")
        
        op = input("Elige una opcion: ")
        if op == "0": break
        elif op == "1": gestionar_inventario()
        elif op == "2": iniciar_venta()
        elif op == "3": sugerir_compras_stock()
        elif op == "4": analisis_riesgo_stock()
        elif op == "5": plan_logistico_delivery()
        elif op == "6": reporte_productos_top()
        elif op == "7": reporte_ganancia_neta()
        elif op == "8": proyeccion_expansion()
        elif op == "9": generar_layout_seguridad()

if __name__ == "__main__":
    if login():
        animacion_espera("Sincronizando modulos")
        menu_principal()
