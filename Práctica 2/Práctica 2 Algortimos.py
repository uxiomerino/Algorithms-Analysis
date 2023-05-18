# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:54:47 2021

@author: uxiom
"""
# Importamos o módulo Pretty Table para organizar os datos en táboas, e creamos esas táboas (unha para cada situación requerida: vectores aleatorios, crecentes ou decrecentes):
from prettytable import PrettyTable
taboa_bubble_aleatorio = PrettyTable()
taboa_bubble_crecente = PrettyTable()
taboa_bubble_decrecente = PrettyTable()
taboa_insertion_aleatorio = PrettyTable()
taboa_insertion_crecente = PrettyTable()
taboa_insertion_decrecente = PrettyTable()

# Importamos o módulo math para algunhas operacións matemáticas e o módulo numpy para utilizar o numpy.arange:
import math
import numpy as np

# Definimos os dous algoritmos, insertionSort(v) e bubbleSort(v):
def insertionSort(v):
    n = len(v)
    for i in range(1,n):
        x = v[i]
        j = i-1
        while j >= 0 and v[j] > x:
            v[j+1] = v[j]
            j = j-1
        v[j+1] = x

def bubbleSort(v):
    n = len(v)
    for i in range(2, n+1):
        for j in range(n-i+1):
            if v[j+1] < v[j]:
                aux = v[j+1]
                v[j+1] = v[j]
                v[j] = aux
                
# Funcións de tests para odear cos dous algoritmos
tests = [ [-9,4,13,-1,-5], [6,-3,-15,5,4,5,2], [13,4], [9], [7,6,6,5,4,3,2,1], [1,2,3,4,4,5,6,7] ]
print ("Algunhas probas para o algoritmo insertionSort : ")
for t in tests:
    print ("Input: {}".format(t))
    insertionSort(t) 
    print("Output: {} \n".format(t))
sorted1 = tests

print("Mesmas probas para o algoritmo bubbleSort : ")
tests = [ [-9,4,13,-1,-5], [6,-3,-15,5,4,5,2], [13,4], [9], [7,6,6,5,4,3,2,1], [1,2,3,4,4,5,6,7] ]
for t in tests:
    print ("Input: {}".format(t))
    bubbleSort(t)
    print("Output: {} \n".format(t))

#Engadimos a función assert para asegurarmos de que ambos algoritmos devolven os mesmos vectores ordenados: 
assert sorted1 == tests
print("As saídas dos algoritmos de ordenación é a mesma, continuamos. \n")

# Xeramos vectores aleatorios con números comprendidos entre -10 e 10 e os ordeamos cos algoritmos:
from numpy.random import seed
from numpy.random import randint

seed(1)
sizes = [5,10,15]
for size in sizes:
    array = randint(-10,10,size)
    print(("Input: {}".format(array)))
    bubbleSort(array)
    print("Output: {} \n".format(array))

seed(1)
for size in sizes:
    array = randint(-10,10,size)
    print(("Input: {}".format(array)))
    insertionSort(array)
    print("Output: {} \n".format(array))

# Importamos as funcións de medición de tempo: 
import time
from time import time_ns
def perfcounter_ns():
    return time.perf_counter() * (10**9)

# Función única e principal para medir os tempos de excución e cotas de todas as situacións pedidas: 

sizes = [2, 4, 8, 16, 32, 64, 128, 256] # Tamaño de 'n' seguindo unha progresión xeométrica

def taboas(algoritmo, tabla, tipo_vector):
    # Creamos unha serie de listas para engadir os tempos e os resultados das cotas tras cada iteración do bucle
    cota_subestimada = []
    cota_optima = []
    cota_sobreestimada = []
    tempos_algoritmo = [] 
    # Creamos a primeira columna da táboa cos valores de 'n' 
    tabla.add_column('n', sizes)
    # Comezamos a executar o bucle collendo os distintos valores de 'n'
    for size in sizes:
        # Realizamos un comando 'if' para dividir as posibles situacións e axustar o tipo de vector (aleat, crec ou decrec).
        if tipo_vector == 'Aleatorio':
            array = randint(-size, size, size)
        elif tipo_vector == 'Crecente':
            array = np.arange(0, size)
        elif tipo_vector == 'Decrecente':
            array = np.arange(size, 0, -1)
        else:
            print('Erro na chamada á función: a variable "tipo_vector" non é correcta')
        # Medimos o tempo inicial, executamos o algoritmo e obtemos o tempo total coa resta do tempo ifinal co inicial 
        t1 = perfcounter_ns()
        algoritmo(array)
        t2 = perfcounter_ns()
        tf = t2-t1
        tf = round(tf, 3)
        tempos_algoritmo.append(tf)    
        # Co comando 'if', separamos de novo as distintas situacións e axustamos as cotas ao algoritmo 
        if algoritmo == bubbleSort:
            cotaOp = size**2
            cotaSub = math.log(size)
            cotaSobr = math.log(size) * (size**2)
        elif algoritmo == insertionSort:
            if tipo_vector == 'Crecente':
                cotaOp = size 
                cotaSub = math.log(size) 
                cotaSobr = math.log(size) * (size**2) 
            else:
                cotaOp = size**2
                cotaSobr = math.log(size) * size**2
                cotaSub = math.log(size)
        else:
                print('Erro na chamada á función: a variable "algoritmo" non é correcta')    
        # Unha vez xa axustamos as cotas ao algoritmo correspondente, calculamos os resultados
        x = tf / cotaSub
        y = tf / cotaOp
        z = tf / cotaSobr
        x = round(x, 3)
        y = round(y, 3)
        z = round(z, 3) 
        cota_subestimada.append(x)
        cota_optima.append(y)
        cota_sobreestimada.append(z)
    # Engadimos os resultados das cotas á táboa: 
    tabla.add_column('t(n)', tempos_algoritmo)
    tabla.add_column('COTA SUB', cota_subestimada)
    tabla.add_column('COTA OP', cota_optima)
    tabla.add_column('COTA SOBR', cota_sobreestimada)
    print(tabla)

# Chamamos á función principal varias veces, tantas coma situacións distintas pedidas haxa
print('Táboa "bubble" vectores aleatorios: ') 
taboas(bubbleSort, taboa_bubble_aleatorio, 'Aleatorio')
print('\n Táboa "bubble" vectores crecentes: ')
taboas(bubbleSort, taboa_bubble_crecente, 'Crecente')
print('\n Táboa "bubble" vectores decrecentes: ')
taboas(bubbleSort, taboa_bubble_decrecente, 'Decrecente')
print('\n Táboa "insertion" vectores aleatorios: ')
taboas(insertionSort, taboa_insertion_aleatorio, 'Aleatorio')
print('\n Táboa "insertion" vectores crecentes: ')
taboas(insertionSort, taboa_insertion_crecente, 'Crecente')
print('\n Táboa "insertion" vectores decrecentes: ')
taboas(insertionSort, taboa_insertion_decrecente, 'Decrecente')