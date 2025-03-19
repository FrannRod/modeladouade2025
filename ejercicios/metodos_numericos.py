def imprimir_tabla(resultados, encabezados):
    # Encontrar el ancho máximo para cada columna
    anchos = [len(h) for h in encabezados]
    for r in resultados:
        for i, valor in enumerate(r):
            anchos[i] = max(anchos[i], len(f"{valor:.10f}" if isinstance(valor, float) else str(valor)))
    
    # Imprimir encabezado
    print("\n" + " | ".join(h.ljust(anchos[i]) for i, h in enumerate(encabezados)))
    print("-" * (sum(anchos) + 3 * (len(anchos) - 1)))
    
    # Imprimir resultados
    for r in resultados:
        print(" | ".join(
            (f"{valor:.10f}" if isinstance(valor, float) else str(valor)).ljust(anchos[i])
            for i, valor in enumerate(r)
        ))

def binario(funcion, rangoA, rangoB, tolerancia):
    iteracion = 0
    resultados = []
    while True:
        iteracion += 1
        puntoMedio = (rangoA+rangoB)/2
        resultado = funcion(puntoMedio)
        if resultado <= tolerancia:
            break
        positivo = (resultado * funcion(rangoA)) > 0
        resultados.append((iteracion, rangoA, rangoB, puntoMedio, resultado))
        if positivo:
            rangoB = puntoMedio
        else:
            rangoA = puntoMedio
    encabezados = ["Iteración", "Rango A", "Rango B", "Punto Medio", "f(Punto Medio)"]
    imprimir_tabla(resultados, encabezados)
    
    return puntoMedio, iteracion

def puntoFijo(funcion, x, tolerancia):
    iteracion = 0
    resultados = []
    while abs(x - funcion(x)) > tolerancia:
        iteracion += 1
        fx = funcion(x)
        diferencia = abs(x - fx)
        resultados.append((iteracion, x, fx, diferencia))
        x = fx
        
    encabezados = ["Iteración", "x", "f(x)", "|x - f(x)|"]
    imprimir_tabla(resultados, encabezados)
    
    return x, iteracion 