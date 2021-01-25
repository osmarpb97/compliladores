"""
Objetivo:

Utilizar los conocimientos sobre el paradigma orientado a objetos y los
autómatas finitos, para diseñar e implementar las clases AFN y AFD.

"""
import re

alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'E']

"""Base de los dos automatas"""
class Automata:
    estado_actual = None
    funcion_transicion = dict()
    salida = ''

    def __init__(self, estados, alfabeto, funcion_transicion, estado_inicial, estados_finales):
        self.estados = estados
        self.alfabeto = alfabeto
        self.funcion_transicion = funcion_transicion
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.estado_actual = estado_inicial

    def buscar_estado(self, inicio: int, simbolo: str):
        result = []
        if(inicio != None):
            for element in self.funcion_transicion:
                if (int(element[0]) == int(inicio) and element[1] == simbolo):
                    result.append(element)
        return result

    def reiniciar(self):
        self.estado_actual = self.estado_inicial
        self.salida = ''

    def estado_aceptado(self):
        if(self.estado_actual in self.estados_finales):
            self.salida = self.salida + 'Automata aceptado'
            return True
        else:
            return False

    def obtener_inicial(self):
        return self.estado_inicial

    def obtener_finales(self):
        return self.estados_finales

    def establecer_inicial(self, estado: int):
        self.estado_inicial = estado

    def establecer_final(self, estado: int):
        self.estados_finales.append(estado)

    def agregar_transicion(self, inicio: int, fin: int, simbolo: str):
        if(simbolo in alfabeto):
            self.funcion_transicion[(inicio, simbolo, fin)] = fin
            if(inicio not in self.estados):
                self.estados.append(inicio)
            elif(fin not in self.estados):
                self.estados.append(fin)

    def eliminar_transicion(self, inicio: int, fin: int, simbolo: str):
        del self.funcion_transicion[(inicio, simbolo, fin)]

    def es_AFN(self):
        return not self.es_AFD()

    def es_AFD(self):
        for element in self.funcion_transicion:
            for comp in self.funcion_transicion:
                if element[0] == comp[0] and element[1] == comp[1] and element[2] != comp[2]:
                    return False
        return True

    def guardar_en(self, ruta: str):
        try:
            archivo = open(ruta, "w")
            archivo.write(self.salida)
            archivo.close()
        except:
            pass


class AFD(Automata):
    def transicion_estado(self, simbolo: str):
        t_estado = self.buscar_estado(self.estado_actual, simbolo)
        if(t_estado != [] and simbolo in alfabeto):
            estado_anterior = self.estado_actual
            self.estado_actual = self.funcion_transicion[t_estado[0]]
            return estado_anterior
        else:
            self.estado_actual = None

    def acepta(self, cadena: str):
        if self.es_AFD:
            self.reiniciar()
            trans = list(cadena)
            for t in trans:
                estado_anterior = self.transicion_estado(t)
                self.salida = self.salida + \
                    '{0}->{1}:{2} \n'.format(estado_anterior,
                                             self.estado_actual, t)
            print(self.salida)
            return self.estado_aceptado()

    def genera(self):
        for element in self.funcion_transicion:
            pass
            """No pude hacerlo en 1:30 me falto mas tiempo aun asi lo hare."""



"""No pude hacerlo en 1:30 me falto mas tiempo aun asi lo hare."""

class AFN(Automata):
    def acepta(self):
        if self.es_AFN:
            print("Hello another bro")


"""Crea un automata desde un archivo"""

def cargar_desde(ruta):
    try:
        archivo = open(ruta, "r")
        estado_inicial = archivo.readline().rstrip("\n").split(":")[1]
        estados_finales = list(map(int, archivo.readline().rstrip(
            "\n").split(":")[1].split(',')))
        transiciones = archivo.readlines()
        funcion_transicion = dict()
        estados = []
        for element in transiciones:
            strip_trans = element.rstrip("\n").replace(',', '->').split('->')
            if(strip_trans[2] in alfabeto):
                funcion_transicion[(int(strip_trans[0]), strip_trans[2], int(strip_trans[1]))
                                   ] = int(strip_trans[1])
                if(strip_trans[0] not in estados):
                    estados.append(int(strip_trans[0]))
                elif(strip_trans[1] not in estados):
                    estados.append(int(strip_trans[1]))
        auto = AFD(estados, alfabeto, funcion_transicion,
                   estado_inicial, estados_finales)
        archivo.close()
        return auto
    except:
        raise
