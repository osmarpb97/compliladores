from Practica1 import AFN, cargar_desde, alfabeto
import re

operadores_unarios = ['*', '+']


class ArbolSintactico():
    operadores = []
    regex = []
    estado = []

    def __init__(self, regex):
        arr_len = len(regex)
        operadores = re.findall("[+*().|]|[a-z]|E", regex)
        for index, i in enumerate(operadores):
            if operadores[index] in alfabeto and index+1 < arr_len and operadores[index+1] in alfabeto or operadores[index] in operadores_unarios and operadores[index+1] in alfabeto:
                regex = regex[:index+1]+'.'+regex[index+1:]
                operadores = re.findall("[+*().|]|[a-z]|E", regex)
        # print("REGEX:", regex)
        self.regex = regex

    def hoja(self, pila):
        return pila[-1] if pila else None

    def aplicar_operador(self):
        operator = self.operadores.pop()
        right = self.estado.pop()
        left = self.estado.pop()
        self.estado.append(eval("{0}{1}{2}".format(left, operator, right)))

    def presedencia(self, op1, op2):
        precedencias = {'*': 2, '.': 1, '+': 0}
        return precedencias[op1] > precedencias[op2]

    def operacion_binaria(self, operador, estado1, estado2):
        pass

    def operacion_unaria(self, operador, estado, estado2):
        pass
    
    def construccuion(self):
        for token in self.regex:
            # print("Operadores:{0} Estados:{1}".format(
                self.operadores, self.estado))
            if token in alfabeto:
                self.estado.append(token)
            elif token == '(':
                self.operadores.append(token)
            elif token == ')':
                # print("hoja")
                top = self.hoja(self.operadores)
                while top is not None and top != '(':
                    # print("hi",self.operadores, self.estado)
                    top = self.hoja(self.operadores)
                self.operadores.pop()
            elif token == '*':
                # print("Hacer *", self.estado.pop())
        #     else:
        #         # Operador
        #         top = self.hoja(self.operadores)
        #         while top is not None and top not in "()" and self.presedencia(top, token):
        #             self.aplicar_operador()
        #             top = self.hoja(self.operadores)
        #         self.operadores.append(token)
        # while self.hoja(self.operadores) is not None:
        #     self.aplicar_operador()

        return self.estado


class RegextoAFN():
    regex = ''
    automata = ''
    pilaAFN = []

    def __init__(self, automata, regex):
        self.automata = automata
        self.regex = regex

    def arbol_sintactico(self):
        arbol = ArbolSintactico(self.regex)
        return arbol.construccuion()


# reg = RegextoAFN('', '(a+b)*E')
# print(reg.arbol_sintactico())
