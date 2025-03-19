def imprimir_tabla(resultados, encabezados):
    # Encontrar el ancho máximo para cada columna
    anchos = [len(h) for h in encabezados]
    for r in resultados:
        for i, valor in enumerate(r):
            anchos[i] = max(anchos[i], len(str(valor)))
    
    # Imprimir encabezado
    print("\n" + " | ".join(h.ljust(anchos[i]) for i, h in enumerate(encabezados)))
    print("-" * (sum(anchos) + 3 * (len(anchos) - 1)))
    
    # Imprimir resultados
    for r in resultados:
        print(" | ".join(
            str(valor).ljust(anchos[i])
            for i, valor in enumerate(r)
        ))

def binario(funcion, rangoA, rangoB, tolerancia):
    iteracion = 0
    resultados = []
    
    fa = funcion(rangoA)
    fb = funcion(rangoB)
    
    # Agregar iteración 0
    puntoMedio = (rangoA + rangoB)/2
    resultado = funcion(puntoMedio)
    resultados.append((iteracion, rangoA, rangoB, puntoMedio, resultado))
    
    if abs(fa) <= tolerancia:
        return rangoA, 0
    if abs(fb) <= tolerancia:
        return rangoB, 0
    
    while True:
        iteracion += 1
        puntoMedio = (rangoA+rangoB)/2
        resultado = funcion(puntoMedio)
        
        resultados.append((iteracion, rangoA, rangoB, puntoMedio, resultado))
        
        if abs(resultado) <= tolerancia:
            break
            
        positivo = (resultado * fa) > 0
        if positivo:
            rangoA = puntoMedio
            fa = resultado
        else:
            rangoB = puntoMedio
            fb = resultado
            
    encabezados = ["Iteración", "Rango A", "Rango B", "Punto Medio", "f(Punto Medio)"]
    imprimir_tabla(resultados, encabezados)
    
    return puntoMedio, iteracion

def puntoFijo(funcion, x, tolerancia):
    iteracion = 0
    resultados = []
    
    # Agregar iteración 0
    fx = funcion(x)
    diferencia = abs(x - fx)
    resultados.append((iteracion, x, fx, diferencia))
    
    while abs(x - funcion(x)) > tolerancia:
        iteracion += 1
        fx = funcion(x)
        diferencia = abs(x - fx)
        resultados.append((iteracion, x, fx, diferencia))
        x = fx
        
    encabezados = ["Iteración", "x", "f(x)", "|x - f(x)|"]
    imprimir_tabla(resultados, encabezados)
    
    return x, iteracion 

def newtonRaphson(funcion, derivada, x, tolerancia):
    iteracion = 0
    resultados = []
    
    # Agregar iteración 0
    fx = funcion(x)
    derivadaX = derivada(x)
    resultados.append((iteracion, x, fx, derivadaX, "-"))  # Error inicial es 0
    x_anterior = x
    
    while abs(fx) > tolerancia:
        iteracion += 1
        fx = funcion(x)
        derivadaX = derivada(x)
        x_nuevo = x - fx/derivadaX
        error = abs(x_nuevo - x)  # Calculamos el error
        resultados.append((iteracion, x_nuevo, fx, derivadaX, error))
        x = x_nuevo
        
    encabezados = ["Iteración", "x", "f(x)", "f'(x)", "Error"]
    imprimir_tabla(resultados, encabezados)
    return x, iteracion
