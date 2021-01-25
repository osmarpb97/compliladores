from Practica1 import AFN, AFD, alfabeto
from itertools import chain
estados_ocupados = {'a', 'b'}


class AFNDtoAFD():
    afnd = None
    conjuntos = []
    afd = None
    # A = espsilon cerradura del estado inicial
    # Por cada letra en el alfabeto y en nuestro automata vamos a calcular Dtran[A,alfabeto] ej. Dtran[A,a] Dtran[A,b]

    def __init__(self, afnd):
        self.afnd = afnd
        self.afd = AFD(alfabeto, dict(),0,[])
        self.dtrans([], [])

    def epsilon_cerradura(self, estados: list, visitados, pila):
        for estado in estados:
            if estado not in visitados:
                visitados.append(estado)
                alcanzados = self.afnd.movereps(estado)
                for element in alcanzados:
                    if(element not in pila):
                        pila.append(element)
                self.epsilon_cerradura(alcanzados, visitados, pila)
        return sorted(pila)

    def dtrans(self, conjunto=[], visitados=[]):
        if(conjunto == []):
            conjunto = self.epsilon_cerradura(
                [self.afnd.estado_inicial], [], [])
        if conjunto not in visitados:
            print("Conjunto", conjunto)
            self.conjuntos.append(conjunto)
            visitados.append(conjunto)
            for simbolo in estados_ocupados:
                pila = []
                for estado in conjunto:
                    if(estado, simbolo) in self.afnd.funcion_transicion.keys():
                        pila.append(
                            self.afnd.funcion_transicion[estado, simbolo])
                flatten = list(chain.from_iterable(pila))
                nuevo_estado = self.epsilon_cerradura(flatten, [], [])
                if(nuevo_estado not in visitados):
                    self.dtrans(nuevo_estado)
                    #Agregamos transicion
                self.afd.agregar_transicion(self.conjuntos.index(
                    conjunto), self.conjuntos.index(nuevo_estado), simbolo)
                    #Agregamos los estados finales
                if(self.afnd.estados_finales[0] in nuevo_estado):
                    print(self.afnd.estados_finales, nuevo_estado)
                    self.afd.estados_finales.append(self.conjuntos.index(nuevo_estado))

# afnd = AFN(alfabeto, {(0, 'E'): [1, 11], (1, 'E'): [2, 8], (2, 'E'): [3, 5], (3, 'a'): [4], (5, 'b'): [6], (6, 'E'): [7], (4, 'E'): [7], (7, 'E'): [8, 2], (8, 'a'): [9], (9, 'b'): [10], (11, 'b'): [12], (12, 'E'): [13], (10, 'E'): [13]}, 0, [13])
# afd = AFNDtoAFD(afnd).afd
# print(afd.estados_finales)
