import random
# Número de puntos aleatorios
num_puntos = 10000000
puntos_dentro = 0 # Contador de puntos dentro del círculo
# Generamos los puntos aleatorios
for _ in range(num_puntos):
    x = random.uniform(-1, 1) # Coordenada x aleatoria en [-1,1]
    y = random.uniform(-1, 1) # Coordenada y aleatoria en [-1,1]

 # Si el punto cae dentro del círculo unitario, sumamos al contador
    if x**2 + y**2 <= 1:
        puntos_dentro += 1
# Estimación de pi usando la relación entre área del círculo y cuadrado
pi_estimado = (puntos_dentro / num_puntos) * 4
print(f"Estimación de π usando Montecarlo: {pi_estimado}")