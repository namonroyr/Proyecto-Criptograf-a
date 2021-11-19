import numpy as np

abc = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8, "J" : 9, "K" : 10,
        "L" : 11, "M" : 12, "N" : 13, "O" : 14, "P" : 15, "Q" : 16, "R" : 17, "S" : 18, "T" : 19, "U" : 20,
        "V" : 21, "W" : 22, "X" : 23, "Y" : 24, "Z" : 25}
inv_abc = {value:key for key, value in abc.items()}


print("Ingrese el valor del entero positivo m:")
m = int(input().strip())
print("Ingrese los " + str(m) + " valores de la matriz clave de permutación separados por un espacio:")
values = list(map(int, input().split()))

if (len(set(values)) < m):
    print("Error: Ingresó valores repetidos o no ingreso {} valores".format(m))
    quit()

for a, b in zip(tuple(range(1, m+1)), tuple(sorted(values))):
    if a != b:
        print("Error: Debe ingresar los numeros del 1 al", m)
        quit()
    
mat_permutacion = np.array([range(1, m+1), values]).reshape(2, m)
mat_inv_permutacion = np.array( [ range(1, m+1), [x[0] for x in sorted( list(zip(tuple(range(1, m+1)), tuple(values))), key = lambda x: x[1] )] ] ).reshape(2, m)

# CIFRAMIENTO
print("Ingrese el texto en claro que desea cifrar:")
texto_en_claro = input()

texto_separado = [texto_en_claro[i:i+m] for i in range(0, len(texto_en_claro), m)]

print(texto_separado)
print(mat_permutacion)
print(mat_inv_permutacion)

texto_cifrado = ""
for subtexto in texto_separado:
    for indice in range(1, m+1):
        letra_cifrada = subtexto[ int(mat_permutacion[1][ int(np.where(mat_permutacion == indice)[1][0]) ]) - 1 ]
        texto_cifrado += letra_cifrada

print(texto_cifrado)


# DESCIFRAMIENTO
print("Ingrese el texto cifrado que desea descifrar:")
texto_a_descifrar = input()

texto_separado = [texto_a_descifrar[i:i+m] for i in range(0, len(texto_a_descifrar), m)]
print(texto_separado)

texto_en_claro = ""
for subtexto in texto_separado:
    for indice in range(1, m+1):
        letra_descifrada = subtexto[ int(mat_inv_permutacion[1][ int(np.where(mat_inv_permutacion == indice)[1][0]) ]) - 1 ]
        texto_en_claro += letra_descifrada

print(texto_en_claro)