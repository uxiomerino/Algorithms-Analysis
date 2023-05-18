# -*- coding: utf-8 -*-


"""
Práctica 4: Programación dinámica

Autores: Iván Castro (ivan.castro1@udc.es)
         Uxío Merino (uxio.merino@udc.es)
         Mario Chan (mario.chan@udc.es)
"""


import numpy as np
from prettytable import PrettyTable
from numpy.random import seed
import time
import math


# Conversión del tiempo a microsegundos
def perfcounter_us():
    return time.perf_counter() * (10**6)

# Creación de palabras aleatorias
def create_word(n, alphabet=(0, 1)):
    a = np.random.randint(low=0, high=len(alphabet), size=(n,))
    word = np.array(alphabet)[a].tolist()
    return word

# Creación de palabras fusionadas aleatorias válidas -> CREA SECUENCIAS VÁLIDAS
def mix_words(a, b, valid=True):
    new_word = []
    a_array = np.array(a)
    b_array = np.array(b)
    if not valid:
        np.random.shuffle(a_array)
        np.random.shuffle(b_array)
    a_index = 0
    b_index = 0
    while len(new_word) < len(a) + len(b):
        p = np.random.randint(2)
        if (p and a_index < len(a_array)) or b_index >= len(b_array):
            new_word.append(a_array[a_index])
            a_index += 1
        else:
            new_word.append(b_array[b_index])
            b_index += 1
    return new_word



####################
# IMPLEMENTACIONES #
####################

# Algoritmo 1
def isMixtureDP(A, B, C):
    """Dados dos strings (o listas de enteros) A y B, determina si un
    tercer string C es una mezcla válida o no de ambos"""
    
    # Tamaños de A, B y C
    n = len(A)    
    m = len(B)    
    s = len(C)
    
    if n + m != s:
        return False
        
    # Tabla de booleanos inicializada a False
    t = np.zeros((n + 1, m + 1))
    t[0, 0] = True
    
    for i in range(0, n + 1):
        for j in range(0, m + 1):
            t[i, j] = t[max(0, i - 1), j] or t[i, max(0, j - 1)]
            if t[i, j] and (i < n or j < m):
                k = i + j
                t[i, j] = False
                if i < n:
                    t[i, j] = (t[i, j] or A[i] == C[k])
                if j < m:
                    t[i, j] = (t[i, j] or B[j] == C[k])  
                    
    return t[n, m]
            
# Algoritmo 2
def isMixtureCX(A, B, C):
    """Dados dos strings (o listas de enteros) A y B, determina si un
    tercer string C es una mezcla válida o no de ambos"""
    
    # Tamaños de A, B y C
    n = len(A)
    m = len(B)
    s = len(C)
    
    if n + m != s:
        return False
    
    known = {(0, 0)} # set
    trial = [(0, 0)] # list
    
    while len(trial) > 0:
        (i, j) = trial.pop() # removing last element in trial
        k = i + j
        if k > (s - 1):
            return True
        if (i < n and A[i] == C[k] and (i + 1, j) not in known):
            trial.append((i + 1, j))
            known.add((i + 1, j))
        if (j < m and B[j] == C[k] and (i, j + 1) not in known):
            trial.append((i, j + 1))
            known.add((i, j + 1))
            
    return False


##############
# VALIDACIÓN #
##############
    
# Secuencia de combinaciones válidas para C
comb_validas = ["HelloWorld", "WorldHello", "HWorellldo", "WorHellold", \
                 "HWeolrllod"]

# Secuencia de combinaciones inválidas para C
comb_invalidas = ["dlroWolleH", "oHelloWrld", "HelloWorlds", "HeloWorld", \
                  "HelloWooorld"] 

# Función test para la validación de los algoritmos
def test(A, B, combs, alg):
    """Comprueba el funcionamiento del algoritmo con cada secuencia"""
    
    # Secuencias válidas
    if combs == comb_validas:
        for combinacion in combs:
            assert alg(A, B, combinacion) == True
        print("{}: Prueba satisfactoria para secuencias válidas" \
              .format(alg.__name__))
        
    # Secuencias inválidas
    else:
        for combinacion in combs:
            assert alg(A, B, combinacion) == False
        print("{}: Prueba satisfactoria para secuencias inválidas" \
              .format(alg.__name__))
        
# Caso básico: A = Hello y B = World
test("Hello", "World", comb_validas, isMixtureDP)
test("Hello", "World", comb_invalidas, isMixtureDP)
test("Hello", "World", comb_validas, isMixtureCX)
test("Hello", "World", comb_invalidas, isMixtureCX)


########################
# TIEMPOS DE EJECUCIÓN #
########################

# Valores del tamaño de las palabras "n"
n =  [20, 40, 80, 160, 320, 640, 1280, 2560]


def createPrettyTable(alg):
    """Genera una tabla en función del algoritmo considerado"""
    
    # Creación de la tabla
    x = PrettyTable()
    
    # En función del algoritmo que se considere se determinan los campos,
    # que corresponderán a cada una de las cotas
    
    if alg == isMixtureDP: # Algoritmo 1
        x.field_names = ["n", "t(n)", "t(n)/n", \
                         "t(n)/math.pow(n, 2)", "t(n)/(math.pow(n, 2.5))"]
        
    else: # Algoritmo 2
       x.field_names =  ["n", "t(n)", "t(n) / math.log(n)", \
                         "t(n) / n", "t(n) / math.pow(n, 1.5)"]
     
    return x # Devuelve el objeto creado

def caso_vocabulario(caso, n):
    """Determina el escenario con el que se va a trabajar"""
    
    # Crea una semilla para generar siempre las mismas palabras
    seed(1) 
    
    # En función del caso, determina la forma de crear las palabras
    if caso == 1: # Escenario 1 (vocabulario de dos únicos elementos)
        A = create_word(n)
        B = create_word(n)
        C = mix_words(A, B) # Secuencia válida
        
    elif caso == 2: # Escenario 2 (con todos los caracteres del código ASCII)
        alphabet = tuple(np.arange(0, 256))
        A = create_word(n, alphabet)
        B = create_word(n, alphabet)
        C = mix_words(A, B) # Secuencia válida
    
    else: # Escenario 3 (vocabulario de igual tamaño que la longitud de A y B)
        alphabet = tuple(np.arange(0, n))
        A = create_word(n, alphabet)
        B = create_word(n, alphabet)
        C = mix_words(A, B) # Secuencia válida
        
    return A, B, C
    
def tiempos_ejecucion(alg, sizes, caso, umbral = 1000, K = 1000):
    """Calcula los tiempos de ejecución del algoritmo pasado como
    argumento y devuelve una tabla con las cotas correspondientes"""
    
    # Llamada a la función que genera la tabla
    tabla = createPrettyTable(alg)
    tabla.float_format = ".5" # 7 cifras significativas
    
    # Calcula los tiempos de ejecución para cada valor de n
    for i in sizes:
        A, B, C = caso_vocabulario(caso, i) # Generación de las palabras
        # Calcula el tiempo de ejecución para dichas palabras
        t1 = perfcounter_us()
        alg(A, B, C) # Ejecución del algoritmo
        t2 = perfcounter_us()
        t = t2 - t1 # Tiempo de ejecución en microsegundos
    
        if t < umbral: # Umbral de confianza (por defecto =1000)   
            # Cálculo de tiempos pequeños con K (por defecto =1000)
            t1 = perfcounter_us()
            for iteracion in range(K):
                A, B, C = caso_vocabulario(caso, i)
                alg(A, B, C) # Se ejecuta durante K iteraciones
            t2 = perfcounter_us()
            t_1 = t2 - t1
            t3 = perfcounter_us()
            for iteracion in range(K):
                A, B, C = caso_vocabulario(caso, i) # Calcula el tiempo que 
            t4 = perfcounter_us()                   # tardan las palabras
            t_2 = t4 - t3                           # en inicializarse K veces
            t = (t_1 - t_2)/K # Tiempo ajustado
            
        # Añade cada fila a la tabla
        if alg == isMixtureDP:
            tabla.add_row([i, t, t/i, \
                       t/math.pow(i, 2), \
                       t/(math.pow(i, 2.5))])
        else: # Algoritmo 2
            tabla.add_row([i, t, t/math.log(i), \
                       t/(i* math.log(i)), \
                       t/math.pow(i, 1.5)])
    
    # Devuelve la tabla con los tiempos de ejecución y las cotas
    print(tabla)
   
# Impresión de los resultados

print("\n Algoritmo isMixtureDP, escenario 1: ")
tiempos_ejecucion(isMixtureDP, n, 1)
print("\n Algoritmo isMixtureDP, escenario 2: ")
tiempos_ejecucion(isMixtureDP, n, 2)
print("\n Algoritmo isMixtureDP, escenario 3: ")
tiempos_ejecucion(isMixtureDP, n, 3)
print("")
print("\n Algoritmo isMixtureCX, escenario 1: ")
tiempos_ejecucion(isMixtureCX, n, 1)
print("\n Algortimo isMixtureCX, escenario 2: ")
tiempos_ejecucion(isMixtureCX, n, 2)
print("\n Algortimo isMixtureCX, escenario 3: ")
tiempos_ejecucion(isMixtureCX, n, 3)   
