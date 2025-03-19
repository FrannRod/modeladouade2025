def imprimir_tabla(resultados, encabezados):
    # Ancho fijo para cada tipo de columna
    ANCHO_ITERACION = 9
    ANCHO_NUMERICO = 20
    
    # Asignar anchos según el tipo de columna
    anchos = []
    for h in encabezados:
        if h == "Iteración":
            anchos.append(ANCHO_ITERACION)
        else:
            anchos.append(ANCHO_NUMERICO)
    
    # Imprimir encabezado
    print("\n" + " | ".join(h.ljust(anchos[i]) for i, h in enumerate(encabezados)))
    print("-" * (sum(anchos) + 3 * (len(anchos) - 1)))
    
    # Imprimir resultados
    for r in resultados:
        fila = []
        for i, valor in enumerate(r):
            if i == 0:  # Iteración
                fila.append(str(valor).ljust(anchos[i]))
            elif valor == "-":
                fila.append(str(valor).center(anchos[i]))
            else:  # Valores numéricos
                fila.append(format(valor, '.16f').ljust(anchos[i]))
        print(" | ".join(fila))

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
    resultados.append((iteracion, x, fx, derivadaX, "-", "-"))  # Error inicial es 0
    x_anterior = x
    
    while abs(fx) > tolerancia:
        iteracion += 1
        x_nuevo = x - fx/derivadaX
        fx = funcion(x_nuevo)
        derivadaX = derivada(x_nuevo)
        error_absoluto = abs(x_nuevo - x)  # Calculamos el error absoluto
        error_relativo = abs(error_absoluto / x_nuevo) if x_nuevo != 0 else "-"  # Error relativo
        resultados.append((iteracion, x_nuevo, fx, derivadaX, error_absoluto, error_relativo))
        x = x_nuevo
        
    encabezados = ["Iteración", "x", "f(x)", "f'(x)", "Error Absoluto", "Error Relativo"]
    imprimir_tabla(resultados, encabezados)
    return x, iteracion
