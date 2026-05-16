# INFORME TÉCNICO: PROYECTO FARMASYS ERP (VERSIÓN BETA)

## II. ANÁLISIS DE LA SOLUCIÓN

### 2.1. Elección de la solución
Para resolver la problemática de alta demanda y optimización de inventarios, se han seleccionado estrategias algorítmicas basadas en principios de ciencias de la computación y matemáticas:

*   **Ordenamiento y Búsqueda**: Se eligió **Quick Sort** ($O(n \log n)$) por su eficiencia en la organización de datos masivos y **Búsqueda Binaria** ($O(\log n)$) para garantizar que el despacho en caja sea instantáneo, reduciendo los tiempos de espera del cliente.
*   **Optimización de Recursos**: Se implementó el **Problema de la Mochila 0/1** mediante Programación Dinámica. Este principio de ingeniería permite maximizar la utilidad del presupuesto de reposición, asegurando que los medicamentos críticos siempre estén en stock.
*   **Logística y Redes**: Se utilizó la **Teoría de Grafos (BFS)** para encontrar rutas óptimas de distribución, fundamentado en la búsqueda de caminos mínimos en estructuras no pesadas.
*   **Análisis Probabilístico**: El método de **Montecarlo** permite cuantificar el riesgo de agotamiento de stock mediante simulaciones estadísticas, reemplazando las estimaciones manuales por datos científicos.

### 2.2. Herramientas de ingeniería
*   **Lenguaje**: Python 3.x por su versatilidad en estructuras de datos.
*   **Librerías**: `multiprocessing` para demostrar el speedup en cálculos pesados y `collections.deque` para la gestión eficiente de colas en grafos.

---

## III. DESARROLLO DE LA SOLUCIÓN

### 3.1. Formulación del pseudocódigo
A continuación, se presenta la lógica del algoritmo de reposición (Mochila 0/1):

```text
ALGORITMO ReposicionMochila(presupuesto, productos):
    Crear matriz K[n+1][presupuesto+1] llena de ceros
    PARA cada producto i desde 1 hasta n:
        PARA cada p_actual desde 1 hasta presupuesto:
            SI costo[i] <= p_actual:
                K[i][p_actual] = MAX(prioridad[i] + K[i-1][p_actual - costo[i]], K[i-1][p_actual])
            SINO:
                K[i][p_actual] = K[i-1][p_actual]
    RETORNAR K[n][presupuesto] y lista de productos recuperados
```

### 3.2. Implementación del algoritmo
La implementación se encuentra en el módulo `algoritmos.py`, utilizando matrices de Programación Dinámica para evitar la redundancia de cálculos (principio de optimalidad de Bellman) y retroceso (backtracking) para recuperar los nombres de los productos sugeridos.

---

## IV. RESULTADOS

### 4.1. Análisis empírico (Complejidad Temporal)

| Categoría | Algoritmo | Complejidad (Big O) | Aplicación en FarmaSys |
| :--- | :--- | :--- | :--- |
| Ordenamiento | Quick Sort | $O(n \log n)$ | Organización del inventario por ID. |
| Búsqueda | Binaria | $O(\log n)$ | Localización de productos en Caja. |
| Dinámica | Mochila 0/1 | $O(n \times W)$ | Sugerencia inteligente de compras. |
| Grafos | BFS | $O(V + E)$ | Cálculo de rutas de delivery. |
| Paralelismo | Multiprocessing | $O(T / P)$ | Reporte de ganancias acelerado. |

### 4.2. Evaluación
El sistema demuestra un alto desempeño. Por ejemplo, el reporte de ganancias en paralelo permite distribuir la carga de transacciones históricas en múltiples núcleos, logrando una reducción del tiempo de procesamiento proporcional al número de CPUs disponibles (Speedup).

---

## V. CONCLUSIONES
1.  La aplicación de **Programación Dinámica** garantiza que la farmacia siempre invierta su presupuesto en los medicamentos con mayor impacto social (Críticos).
2.  El uso de **Búsqueda Binaria** elimina el error humano y la lentitud en el punto de venta, permitiendo una escalabilidad real ante miles de productos.
3.  La integración de **Montecarlo** proporciona una capa de inteligencia predictiva que transforma la farmacia de un modelo reactivo a uno proactivo.
