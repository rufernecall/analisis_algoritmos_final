import os
from typing import List, Optional
from algoritmos import (
    busqueda_binaria, 
    cambio_monedas_voraz, 
    mochila_reabastecimiento, 
    busqueda_fibonacci,
    Producto,
    DesgloseCambio
)

# --- CAPA DE DATOS (DATA LAYER) ---
# Simulacion de persistencia en memoria
inventario: List[Producto] = [
    {"id": 101, "nombre": "Paracetamol 500mg", "stock": 50, "precio": 5.0, "costo": 3.0, "prioridad": 8},
    {"id": 105, "nombre": "Ibuprofeno 400mg", "stock": 120, "precio": 8.5, "costo": 4.0, "prioridad": 9},
    {"id": 110, "nombre": "Amoxicilina 500mg", "stock": 30, "precio": 15.0, "costo": 10.0, "prioridad": 7},
    {"id": 115, "nombre": "Loratadina 10mg", "stock": 200, "precio": 12.0, "costo": 6.0, "prioridad": 5},
    {"id": 120, "nombre": "Omeprazol 20mg", "stock": 15, "precio": 20.0, "costo": 12.0, "prioridad": 10},
]

carrito: List[Producto] = []

# --- UTILITARIOS ---
def limpiar_consola() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

# --- LOGICA DE NEGOCIO (BUSINESS LOGIC) ---

def listar_inventario() -> None:
    print("\n[REPORTE DE INVENTARIO]")
    header = f"{'ID':<5} | {'Nombre':<20} | {'Stock':<6} | {'Precio':<8} | {'Costo':<8} | {'Pri':<4}"
    print(header)
    print("-" * len(header))
    for p in sorted(inventario, key=lambda x: x['id']):
        print(f"{p['id']:<5} | {p['nombre']:<20} | {p['stock']:<6} | S/{p['precio']:<7.2f} | S/{p['costo']:<7.2f} | {p['prioridad']:<4}")
    input("\nPresione Enter para continuar...")

def ejecutar_venta() -> None:
    global carrito
    total: float = sum(item['precio'] * item['cantidad'] for item in carrito)
    print(f"\nTOTAL A COBRAR: S/{total:.2f}")
    
    try:
        pago: float = float(input("Monto recibido: "))
        if pago < total:
            print("ERROR: Pago insuficiente.")
            return
        
        vuelto: float = pago - total
        denominaciones: List[float] = [200.0, 100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.0, 0.50, 0.20, 0.10]
        desglose: DesgloseCambio = cambio_monedas_voraz(vuelto, denominaciones)
        
        print(f"\nVUELTO TOTAL: S/{vuelto:.2f}")
        for valor, cant in desglose.items():
            print(f"  - S/{valor:6.2f} : {cant}")
            
        # Actualizacion de inventario (Commit)
        for item in carrito:
            p = next(x for x in inventario if x['id'] == item['id'])
            p['stock'] -= item['cantidad']
        
        carrito = []
        print("\nVENTA FINALIZADA EXITOSAMENTE.")
    except ValueError:
        print("ERROR: Entrada invalida.")
    input()

def optimizar_stock() -> None:
    print("\n[OPTIMIZACION DE REABASTECIMIENTO]")
    try:
        presupuesto: float = float(input("Presupuesto disponible: "))
        # Consideramos productos con stock critico (< 60)
        candidatos = [p for p in inventario if p['stock'] < 60]
        
        valor, seleccion = mochila_reabastecimiento(presupuesto, candidatos)
        
        print(f"\nRESULTADO DE OPTIMIZACION (KNAPSACK):")
        print(f"Prioridad Maximizada: {valor}")
        print("Productos sugeridos para compra:")
        for s in seleccion:
            print(f"  - {s['nombre']} (Costo: S/{s['costo']:.2f})")
    except ValueError:
        print("ERROR: Ingrese un valor numerico.")
    input()

def buscar_producto_binario() -> None:
    try:
        id_busqueda: int = int(input("\nIngrese ID del producto: "))
        inv_ordenado = sorted(inventario, key=lambda x: x['id'])
        resultado = busqueda_binaria(inv_ordenado, id_busqueda)
        
        if resultado:
            print(f"\nENCONTRADO: {resultado['nombre']} | Stock: {resultado['stock']}")
        else:
            print("\nPRODUCTO NO REGISTRADO.")
    except ValueError:
        print("ERROR: ID invalido.")
    input()

# --- INTERFAZ DE USUARIO (UI) ---

def main() -> None:
    while True:
        limpiar_consola()
        print("========================================")
        print("      SISTEMA DE GESTION FARMACEUTICA   ")
        print("========================================")
        print("1. Listar Inventario")
        print("2. Buscar Producto (ID - Binaria)")
        print("3. Buscar por Stock (Fibonacci)")
        print("4. Caja / Punto de Venta")
        print("5. Optimizar Compras (Mochila)")
        print("0. Salir")
        print("========================================")
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            listar_inventario()
        elif opcion == "2":
            buscar_producto_binario()
        elif opcion == "4":
            ejecutar_venta()
        elif opcion == "5":
            optimizar_stock()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")
            input()

if __name__ == "__main__":
    main()
