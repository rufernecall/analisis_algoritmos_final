# Informe del Proyecto: Sistema para Farmacia (FarmaSys)

## 1. Introduccion
Este proyecto es un sistema de gestion para una farmacia que atiende a muchas personas y necesita rapidez. La idea es usar los algoritmos que aprendimos en el curso para que las tareas como cobrar, ordenar el inventario o reponer productos sean mas eficientes.

## 2. Los Algoritmos que use
Para que el sistema funcione bien, aplique varias de las estrategias que vimos en las clases:

*   **Busqueda y Ordenamiento (Semanas 1 y 2)**: 
    Use **Quick Sort** para que la lista de medicamentos siempre este ordenada por su ID. Esto es importante porque asi puedo usar la **Busqueda Binaria**, que es muchisimo mas rapida que buscar uno por uno cuando hay miles de productos. Tambien puse una busqueda de **Fuerza Bruta** para cuando queremos buscar por nombre.

*   **Algoritmos Voraces (Semana 3)**: 
    En la parte de la caja, use un algoritmo voraz para dar el vuelto. Lo que hace es ir entregando siempre la moneda mas grande posible hasta completar el monto. Es simple pero efectivo para el dia a dia de la farmacia.

*   **Backtracking (Semana 4)**: 
    Como ejemplo de esta tecnica, puse el problema de las **8 Reinas**. En el sistema lo usamos como una forma de organizar la seguridad o disposicion de camaras en el deposito para que cubran todo sin estorbarse.

*   **Programacion Dinamica (Semana 5)**: 
    Aqui use el problema de la **Mochila 0/1** para ayudar al dueño a decidir que productos comprar cuando tiene poco presupuesto, eligiendo los que tienen mas prioridad. Tambien implemente **Fibonacci** con una tabla para que los calculos sean instantaneos.

*   **Temas Avanzados (Semanas 6 y 7)**: 
    Añadi una seccion de laboratorio donde probe cosas mas complejas como:
    - **Montecarlo**: para estimar probabilidades tirando "dardos" virtuales.
    - **Grafos**: usando busqueda en anchura (BFS) para ver como se conectan los locales.
    - **Arboles de Expresion**: para resolver formulas matematicas de forma organizada.
    - **Paralelismo**: usando varios nucleos del procesador al mismo tiempo para procesar datos pesados mas rapido.

## 3. Conclusiones
Al aplicar estas tecnicas, el programa deja de ser una simple lista y se convierte en una herramienta real. Lo que mas me sirvio fue ver como la programacion dinamica y el ordenamiento correcto pueden hacer que un programa que antes era lento ahora vuele. 

El codigo esta ordenado y comentado para que se entienda que hace cada parte, tratando de seguir siempre lo que vimos en las diapositivas y laboratorios del ciclo.
