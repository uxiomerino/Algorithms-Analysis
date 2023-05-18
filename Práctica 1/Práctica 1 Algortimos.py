# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 20:11:40 2021

@author: uxiom
"""

#Práctica 1 DAA

#Se importa math, necesario para la funcion Binet (raices y potencias)
import math

#Se importa PrettyTable, para mostrar los resultados en una tabla
from prettytable import PrettyTable
table_recursive = PrettyTable()
table_iterative = PrettyTable()
table_binet = PrettyTable()

#Primera Función : la versión recursiva

def fib_recursive(n):
    if n < 2:
        return n
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)


#Segunda Función : la versión iterativa
        
def fib_iterative(n):
    if n == 0:
        return 0
    a = 0
    b = 1
    i = 2
    while i < n:
        aux = a
        a = b
        b = b+aux
        i = i+1
    return a+b


#Tercera Función : a través de la fórmula de Binet

def fib_binet(n):
    Phi = (1 + math.sqrt(5))/2
    Tau = (1 - math.sqrt(5))/2
    return (math.pow(Phi,n)-math.pow(Tau,n))/math.sqrt(5)


#Test (Funciones para comprovar que las funciones van correctamente)   
for n in range(10):
    print("Fibonacci recursive({}) = {} ".format(n,round(fib_recursive(n))))
print("")
for n in range(10):
    print('Fibonacci Iterative({}) = {} '.format(n,round(fib_iterative(n))))
print("")
for n in range(10):
    print('Fibonacci Binet({}) = {} '.format(n,round(fib_binet(n))))
print("")
#Importamos el módulo time, para poder medir los timepos de ejecución a partir de él
import time

#Función que se encarga de la conversión a nanosegundos
def perfcounter_ns():
    return time.perf_counter() * (10**9)

#Creación de listas y tablas necesarias

table_recursive.add_column('n', [2, 4, 8, 16, 32])
time_recursive = []
time_recursive1 = []
time_recursive2 = []
time_recursive3 = []


table_iterative.add_column('n', [2, 4, 8, 16, 32, 64, 128])
time_iterative = []
time_iterative1 = []
time_iterative2 = []
time_iterative3 = []

time_binet = []
time_binet1 = []
time_binet2 = []
table_binet.add_column('n', [2, 4, 8, 16, 32, 64, 128])

v = [2, 4, 8, 16, 32]
w = [2, 4, 8, 16, 32, 64, 128]

#Ejecucion de la versión recursiva:
n = 2
while n<33:
    t1 = perfcounter_ns() 
    for k in (1, 1000):
        fib_recursive(n) 
    t2 = perfcounter_ns() 
    t_recursive = (t2 - t1)/1000
    time_recursive.append(int(t_recursive))
    n = n*2
table_recursive.add_column('t(n)', time_recursive)

i = 0    
for x in time_recursive:
    tn=time_recursive[i]/ math.pow(v[i],2)
    time_recursive1.append(int(tn))
    i+=1
table_recursive.add_column('t(n) / math.pow(n,2)', time_recursive1)

i=0    
for x in time_recursive:
    tn=time_recursive[i]/ math.pow(1.6180,v[i])
    time_recursive2.append(tn)
    i+=1
table_recursive.add_column('t(n) / math.pow(1.6180,n)', time_recursive2)

i=0    
for x in time_recursive:
    tn=time_recursive[i]/ math.pow(2,v[i])
    time_recursive3.append(tn)
    i+=1
table_recursive.add_column('t(n) / math.pow(2,n)', time_recursive3)  

print(table_recursive)
    


#Ejecucion de la versión iterativa:
n = 2
while n<=128:
    t1 = perfcounter_ns() 
    for k in (1, 1000):
        fib_iterative(n) 
    t2 = perfcounter_ns()
    t_iterative = (t2 - t1)/1000
    time_iterative.append(t_iterative)
    n = n*2
table_iterative.add_column('t(n)', time_iterative)

i=0    
for x in time_iterative:
    tn=time_iterative[i]/ (math.log(w[i]))
    time_iterative1.append(tn)
    i+=1
table_iterative.add_column('t(n) / COTA LIG. INFERIOR', time_iterative1)

i=0
for x in time_iterative:
    tn=time_iterative[i]/ w[i]
    time_iterative2.append(tn)
    i+=1
table_iterative.add_column('t(n) / COTA ÓPTIMA', time_iterative2)
i = 0    
for x in time_iterative:
    tn=time_iterative[i]/ math.pow(w[i], 2)
    time_iterative3.append(tn)
    i+=1
table_iterative.add_column('t(n) / COTA LIG. SUPERIOR', time_iterative3)  
    
print(table_iterative) 
    
    
  
#Ejecucion a través de la fórmula de Binet:
n = 2
while n<=128:    
    t1 = perfcounter_ns()
    for k in (1, 1000):
        fib_binet(n)
    t2 = perfcounter_ns() 
    t_binet = (t2 - t1)/1000
    time_binet.append(t_binet)    
    n = n*2
table_binet.add_column('t(n)', time_binet)

i=0
for x in time_binet:
    tn=time_binet[i] / 1
    time_binet1.append(tn)
    i+=1
table_binet.add_column('t(n) / COTA AJUSTADA', time_binet1)

i=0
for x in time_binet:
    tn= time_binet[i]/ w[i] 
    time_binet2.append(tn)
    i+=1
table_binet.add_column('t(n) / COTA LIG. SUPERIOR', time_binet2)

print(table_binet)



