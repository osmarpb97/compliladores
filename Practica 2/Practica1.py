"""
Objetivo:

Utilizar los conocimientos sobre el paradigma orientado a objetos y los
autómatas finitos, para diseñar e implementar las clases AFN y AFD.

"""
alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'E']

"""Base de los dos automatas"""


class Automata:
    estado_actual = None
    funcion_transicion = dict()
    salida = ''
    visitado = []

    def __init__(self, alfabeto, funcion_transicion, estado_inicial, estados_finales):
        self.alfabeto = alfabeto
        self.funcion_transicion = funcion_transicion
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.estado_actual = estado_inicial

    def reiniciar(self):
        """Reinicia el estado actual del automata asi como tambien su ultima salida"""
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
        """Retorna un arreglo con los estados finales"""
        return self.estados_finales

    def establecer_inicial(self, estado: int):
        """Establece un estado como estado inicial"""
        self.estado_inicial = estado

    def establecer_final(self, estado: int):
        """Agrega un estado final al arreglo de estados finales"""
        self.estados_finales.append(estado)

    def agregar_transicion(self, inicio: int, fin: int, simbolo: str):
        """Agrega una transicion al automata"""
        if(simbolo in alfabeto):
            if((inicio, simbolo) in self.funcion_transicion.keys() and fin not in self.funcion_transicion[(inicio, simbolo)]):
                self.funcion_transicion[(inicio, simbolo)].append(fin)
            else:
                self.funcion_transicion[(inicio, simbolo)] = [fin]

    def eliminar_transicion(self, inicio: int, fin: int, simbolo: str):
        """Elimina una transicion del automata"""
        if((inicio, simbolo) in self.funcion_transicion.keys()):
            transicion = self.funcion_transicion[(inicio, simbolo)]
            if(len(transicion) > 1):
                self.funcion_transicion[(inicio, simbolo)].remove(fin)
            else:
                del self.funcion_transicion[(inicio, simbolo)]

    def es_AFN(self):
        """Evalua si el automata es AFN"""
        return not self.es_AFD()

    def es_AFD(self):
        """Evalua si el automata es AFD"""
        for element in self.funcion_transicion:
            if(len(self.funcion_transicion[element]) > 1):
                return False
        return True

    def guardar_en(self, ruta: str):
        """Guarda en un archivo la salida del ultimo automata registrado"""
        try:
            archivo = open(ruta, "w")
            archivo.write(self.salida)
            archivo.close()
        except:
            pass


class AFD(Automata):
    camino = []
    generar = None

    def transicion_estado(self, simbolo: str):
        """Dado un simbolo realiza la trancicion y guarda el estado acutal y retorna el estado anterior"""
        if((self.estado_actual, simbolo) in self.funcion_transicion.keys()):
            t_estado = self.funcion_transicion[(self.estado_actual, simbolo)]
            if(simbolo in alfabeto):
                estado_anterior = self.estado_actual
                self.estado_actual = t_estado[0]
                return estado_anterior
        else:
            self.estado_actual = None

    def acepta(self, cadena: str):
        """Retorna True si la cadena es aceptada en el automata"""
        if self.es_AFD():
            self.reiniciar()
            trans = list(cadena)
            for t in trans:
                estado_anterior = self.transicion_estado(t)
                self.salida = self.salida + \
                    '{0}->{1}:{2} \n'.format(estado_anterior,
                                             self.estado_actual, t)
            return self.estado_aceptado()

    def nodos_desde(self, nodo: int):
        """Dado un nodo n retorna un arreglo con las transiciones de ese nodo"""
        return [element for element in self.funcion_transicion.keys() if int(element[0]) == nodo]

    def depthfirst(self, nodo: int):
        """Dado un nodo inicial recorre el grafo hasta encontrar un estado aceptado"""
        aceptado = self.acepta(self.camino)
        if nodo not in self.visitado and not aceptado:
            self.visitado.append(nodo)
            for vertice in self.nodos_desde(nodo):
                self.camino.append(vertice[1])
                return self.depthfirst(self.funcion_transicion[vertice][0])
        return self.camino

    def genera(self):
        """Genera una cadena valida para el automata"""
        self.visitado = []
        return str(self.depthfirst(self.estado_inicial))


class AFN(Automata):
    pass
    # def acepta(self, cadena: str):
    #     """Retorna True si la cadena es aceptada en el automata"""
    #     if self.es_AFN:
    #         print(self.funcion_transicion)
    #         self.reiniciar()
    #         trans = list(cadena)
    #         for t in trans:
    #             estado_anterior = self.transicion_estado(t)
    #             self.salida = self.salida + \
    #                 '{0}->{1}:{2} \n'.format(estado_anterior,
    #                                          self.estado_actual, t)
    #         return self.estado_aceptado()

    # def transicion_estado(self, simbolo: str, index=0):
    #     """Dado un simbolo realiza la trancicion y guarda el estado acutal y retorna el estado anterior"""
    #     if((self.estado_actual, simbolo) in self.funcion_transicion.keys()):
    #         t_estado = self.funcion_transicion[(self.estado_actual, simbolo)]
    #         if(len(t_estado) == 1 and (t_estado, index) not in self.visitado):
    #             self.visitado.append((t_estado, index))
    #             if(simbolo in alfabeto):
    #                 estado_anterior = self.estado_actual
    #                 self.estado_actual = t_estado[0]
    #                 return estado_anterior
    #             else:
    #                 self.estado_actual = None
    #         else:


def cargar_desde(ruta):
    """Dado un archivo genera un objeto AUTOMATA"""
    try:
        archivo = open(ruta, "r")
        estado_inicial = int(archivo.readline().rstrip("\n").split(":")[1])
        estados_finales = list(map(int, archivo.readline().rstrip(
            "\n").split(":")[1].split(',')))
        transiciones = archivo.readlines()
        funcion_transicion = dict()
        for element in transiciones:
            strip_trans = element.rstrip("\n").replace(',', '->').split('->')
            i = strip_trans[0]
            f = strip_trans[1]
            s = strip_trans[2]

            if(s in alfabeto):
                if ((int(i), s) in funcion_transicion.keys() and int(f) not in funcion_transicion[(int(i), s)]):
                    funcion_transicion[(int(i), s)].append(int(f))
                else:
                    funcion_transicion[(int(i), s)] = [int(f)]
        auto = {"alfabeto": alfabeto, "funcion_transicion": funcion_transicion,
                "estado_inicial": estado_inicial, "estados_finales": estados_finales}
        archivo.close()
        return auto
    except:
        raise


cargar_desde("./automata.fn")
