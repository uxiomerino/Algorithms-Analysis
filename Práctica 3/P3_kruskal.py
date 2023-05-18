# -*- coding: utf-8 -*-


"""
Práctica 3: Árboles expandidos mínimos

Autores: Iván Castro (ivan.castro1@udc.es)
         Uxío Merino (uxio.merino@udc.es)
         Mario Chan (mario.chan@udc.es)
"""


import numpy as np
from prettytable import PrettyTable
import time
import math


# Conversión del tiempo a microsegundos
def perfcounter_us():
    return time.perf_counter() * (10**6)

# Creación de grafos completos aleatorios
def create_graph(n, max_distance=50):        
    a = np.random.randint(low=1, high=max_distance, size=(n,n))
    m = np.tril(a,-1) + np.tril(a, -1).T
    rows, cols = m.shape
    E = set([])
    V = set([])
    
    for i in range(rows):
        V.add(i)
        for j in range(i+1, cols):
            E.add((i,j,m[i][j]))
    return (V,E)


####################
# IMPLEMENTACIONES #
####################

# Función "find"
def find(S, nodo):
    """Encuentra el conjunto de S en el que está ubicado el nodo"""
    
    # Recorre cada conjunto y comprueba si se encuentra el nodo
    for subconjunto in S:
        if nodo in subconjunto:
            return subconjunto
            break # Si se encuentra el nodo, deja de buscar

# Función "merge"
def merge(set1, set2, S):
    """Aplica la operación de unión sobre los conjuntos set1 y set2"""
    
    # Aplica la operación entre los conjuntos
    set3 = set1.union(set2)
    
    # Actualiza S con el conjunto nuevo 
    S.remove(set1)
    S.remove(set2)
    S.append(set3)
    

# Algoritmo de Kruskal
def kruskal(V, E):
    """Calcula el árbol expandido mínimo de un grafo no dirigido y ponderado"""
    
    # Número de vértices del grafo
    n = len(V)
    
    # Ordena las aristas en función de su peso
    E_sorted = sorted(E, key = lambda arista: arista[2])
    
    # Definición del conjunto de aristas solución T
    T = set([])
    
    # Lista inicial de n conjuntos, cada uno formado por un nodo del grafo
    S = [set() for vertice in V]
    for vertice in V:
        S[vertice].add(vertice)
    
    while len(T) < (n - 1): # Comprueba si T es un árbol
        
        a = E_sorted.pop(0) # Recupera y elimina la arista con menor peso
        
        u = a[0] # Nodo u
        # Encuentra el conjunto en el que se encuentra u
        Uset = find(S, u)
        
        v = a[1] # Nodo v
        # Encuentra el conjunto en el que se encuentra v
        Vset = find(S, v)
        
        # Si u y v se encuentran en conjuntos distintos, realiza un "merge"
        # e incorpora la arista a T
        if Uset != Vset:
            merge(Uset, Vset, S)
            T.add(a)
        
    return T # Devuelve el árbol expandido mínimo
    

##############
# VALIDACIÓN #
##############

# Grafo de prueba 1
V1 = {0, 1, 2, 3}
E1 = {(0, 2, 9), (2, 3, 2), (0, 3, 6), (1, 2, 4), (0, 1, 5), (1, 3, 3)}

# Solución
MST1_gold = {(2, 3, 2), (0, 1, 5), (1, 3, 3)}

# Comprobación con la función "assert" del algoritmo de Kruskal
assert kruskal(V1, E1) == MST1_gold
print("Prueba satisfactoria con el grafo de prueba 1")


# Grafo de prueba 2
V2 = {0, 1, 2, 3, 4}
E2 = {(3, 4, 6), (1, 2, 1), (0, 2, 9), (1, 4, 7), (0, 3, 4), (1, 3, 2), \
      (2, 3, 3), (2, 4, 9), (0, 4, 8), (0, 1, 5)}

# Solución
MST2_gold = {(3, 4, 6), (1, 2, 1), (0, 3, 4), (1, 3, 2)}

# Comprobación con la función "assert" del algoritmo de Kruskal
assert kruskal(V2, E2) == MST2_gold
print("Prueba satisfactoria con el grafo de prueba 2")

print("")


########################
# TIEMPOS DE EJECUCIÓN #
########################

# Valores del tamaño del problema "n"
n = [20, 40, 80, 160, 320, 640, 1280, 2560] 


def createPrettyTable():
    """Genera una tabla para el algoritmo de Kruskal"""
    
    # Creación de la tabla
    x = PrettyTable()
    
    # Se determinan los campos, que corresponderán a cada una de las cotas
    x.field_names = ["n", "t(n)", "t(n) / math.pow(n, 1.5)", \
                     "t(n) / math.pow(n, 2.5)", \
                     "t(n) / math.pow(n, 3.5)"]
        
    return x # Devuelve el objeto creado


def tiempos_ejecucion(sizes, umbral = 1000, K = 1000):
    """Calcula los tiempos de ejecución del algoritmo de Kruskal, con un
    umbral fijado por defecto en 1000 µs, y devuelve una tabla con 
    las cotas correspondientes"""
    
    # Llamada a la función que genera la tabla
    tabla = createPrettyTable()
    tabla.float_format = ".7" # 7 cifras significativas
    
    # Calcula los tiempos de ejecución para cada valor de n
    for n in sizes:
        
        V, E = create_graph(n)
        t1 = perfcounter_us()
        kruskal(V, E) # Ejecución del algoritmo
        t2 = perfcounter_us()
        t = t2 - t1 # Tiempo de ejecución
    
        if t < umbral: # Umbral de confianza (por defecto =1000)
            
            # Cálculo de tiempos pequeños con K (por defecto =1000)
            t1 = perfcounter_us()
            for iteracion in range(K): 
                kruskal(V, E) # Se ejecuta durante K iteraciones
            t2 = perfcounter_us()
            
            # Tiempo de ejecución de 1 iteración del algoritmo
            t = (t2 - t1)/K
        
        # Añade cada fila a la tabla
        tabla.add_row([n, t, t/math.pow(n, 1.5), \
                       t/math.pow(n, 2.5), \
                       t/math.pow(n, 3.5)])
    
    # Devuelve la tabla con los tiempos de ejecución y las cotas
    # ajustada, ligeramente subestimada y ligeramente sobre-estimada
    print(tabla)
   

# Impresión de los resultados
print("Algoritmo de Kruskal")
tiempos_ejecucion(n) # Se hace uso de los parámetros por defecto









