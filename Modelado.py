# =================================================================
# INSTRUCCIONES DE USO:
# 1. Modifique la función 'funcion(x)' en el código con la función 
#    que desea analizar
# 2. Ejecute el programa y responda las preguntas
# 3. El programa mostrará los resultados en formato de tabla
# =================================================================


import math

def funcion(x):
    return (x+1)**(1/3)

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

def binario(rangoA, rangoB, tolerancia):
    iteracion = 0
    resultados = []
    while abs(rangoA - rangoB) > tolerancia:
        iteracion += 1
        puntoMedio = (rangoA+rangoB)/2
        resultado = funcion(puntoMedio)
        positivo = resultado > 0
        resultados.append((iteracion, rangoA, rangoB, puntoMedio, resultado))
        if positivo:
            rangoB = puntoMedio
        else:
            rangoA = puntoMedio
            
    encabezados = ["Iteración", "Rango A", "Rango B", "Punto Medio", "f(Punto Medio)"]
    imprimir_tabla(resultados, encabezados)
    
    return puntoMedio, iteracion

def puntoFijo(x, tolerancia):
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

if __name__ == "__main__":
    tolerancia = float(input("Ingrese la tolerancia (Enter para usar 6 decimales por defecto): ") or "1e-6")
    
    while True:
        metodo = input("Seleccione el método (b: binario, p: punto fijo): ").lower()
        if metodo in ['b', 'p']:
            break
        print("Opción inválida. Intente nuevamente.")
        
    if metodo == 'b':
        rangoA = float(input("Ingrese el inicio del rango: "))
        rangoB = float(input("Ingrese el fin del rango: "))
        resultado, iteraciones = binario(rangoA, rangoB, tolerancia)
        print(f"\nMétodo Binario:")
    else:
        x0 = float(input("Ingrese el valor inicial x0: "))
        resultado, iteraciones = puntoFijo(x0, tolerancia)
        print(f"\nMétodo Punto Fijo:")
        
    print(f"Resultado: {resultado}")
    print(f"Iteraciones: {iteraciones}")
