from ejercicios.metodos_numericos import binario, puntoFijo

def funcion(x):
    # Modifique esta función según necesite
    return (x+1)**(1/3)

def main():
    tolerancia = float(input("Ingrese la tolerancia (Enter para usar 6 decimales por defecto): ") or "1e-6")
    
    while True:
        metodo = input("Seleccione el método (b: binario, p: punto fijo): ").lower()
        if metodo in ['b', 'p']:
            break
        print("Opción inválida. Intente nuevamente.")
        
    if metodo == 'b':
        rangoA = float(input("Ingrese el inicio del rango: "))
        rangoB = float(input("Ingrese el fin del rango: "))
        print("\nMétodo Binario:")
        resultado, iteraciones = binario(funcion, rangoA, rangoB, tolerancia)
        print(f"Resultado: {resultado}")
        print(f"Iteraciones: {iteraciones}")
    else:
        x0 = float(input("Ingrese el valor inicial x0: "))
        print("\nMétodo Punto Fijo:")
        resultado, iteraciones = puntoFijo(funcion, x0, tolerancia)
        print(f"Resultado: {resultado}")
        print(f"Iteraciones: {iteraciones}")
        
if __name__ == "__main__":
    main() 
