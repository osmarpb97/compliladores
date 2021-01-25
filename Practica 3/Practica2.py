from Practica1 import AFN, cargar_desde, alfabeto
from itertools import chain
from collections import defaultdict

operadores = ['*', '|', '+', '.']
operadores_binarios = ['|', '.']
operadores_unarios = ['*', '+']
precedencias_dict = {'(', '|', '.', '*', '+'}
precedencias = {'(': 1, '|': 2, '.': 3, '*': 4, '+': 5}


class ArbolBinario():

    def __init__(self, valor=None, operador=None, left=None, right=None):
        self.valor = valor
        self.operador = operador
        self.left = left
        self.right = right

    def __str__(self):
        return self.valor if self.valor else self.operador


def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        valor = node.valor if node.valor else node.operador
        print(' ' * 5 * level + str(node), '')
        printTree(node.right, level + 1)


class ArbolSintactico():
    regex = []
    posfix = ''
    arbol = None

    def __init__(self, regex):
        """Cambia el concatenacion de "ab" = "a.b"""
        index = 0
        res = ''
        regexlen = len(regex)
        while index < regexlen:
            left = regex[index]
            if(index+1 < regexlen):
                right = regex[index+1]
                res += left
                if(left != '(' and right != ')' and (right not in operadores) and left not in operadores_binarios):
                    res += '.'
            index += 1
        res += regex[regexlen-1]
        self.regex = res
        self.infixToPosfix()

    def infixToPosfix(self):
        posfix = ''
        pila_operadores = []
        for element in self.regex:
            if(element == '('):
                pila_operadores.append(element)
            elif(element == ')'):
                while(self.ultimo(pila_operadores) != '('):
                    posfix += pila_operadores.pop()
                pila_operadores.pop()
            else:
                while(len(pila_operadores) > 0):
                    ultimo = self.ultimo(pila_operadores)
                    if(self.precedencia(ultimo) >= self.precedencia(element)):
                        posfix += pila_operadores.pop()
                    else:
                        break
                pila_operadores.append(element)
        while(len(pila_operadores) > 0):
            posfix += pila_operadores.pop()
        self.posfix = posfix

    def generar_arbol(self):
        pila_operadores = []
        print(self.posfix)
        for element in self.posfix:
            if(element in alfabeto):
                pila_operadores.append(ArbolBinario(valor=element))
            elif element in operadores_binarios:
                izquierda = pila_operadores.pop()
                derecha = pila_operadores.pop()
                pila_operadores.append(
                    ArbolBinario(operador=element, left=izquierda, right=derecha))
            elif element in operadores_unarios:
                izquierda = pila_operadores.pop()
                pila_operadores.append(ArbolBinario(
                    operador=element, left=izquierda))
        printTree(pila_operadores[0])

    def precedencia(self, operador):
        if(operador in precedencias_dict):
            return precedencias[operador]
        return 6

    def ultimo(self, pila):
        return pila[-1] if pila else None


class RegextoAFN():
    regex = ''
    automata = ''
    posfix = None

    def __init__(self, regex):
        self.regex = regex
        self.arbol = ArbolSintactico(self.regex)
        self.posfix = self.arbol.posfix
    
    def concatenacion(self,izquierda,derecha):
        """Concatena dos AFN; el de lz izquierda absorbe a la derecha"""
        aux = izquierda.estados_finales[0]
        for element in derecha.funcion_transicion:
            for estado in derecha.funcion_transicion[element]:
                izquierda.agregar_transicion(element[0]+aux, estado+aux, element[1])
            izquierda.estados_finales[0] +=1
                

    def generar_afn(self):
        """Crea un AFN a partir de postfix"""
        estado_final = 1
        estado_inicial = 0
        pila_afns = []
        for element in self.posfix:
            if(element in alfabeto):
                afn = AFN(alfabeto, {}, 0, 0)
                afn.agregar_transicion(estado_inicial, estado_final, element)
                afn.establecer_inicial(estado_inicial)
                afn.establecer_final(estado_final)
                pila_afns.append(afn)
            elif element == '.':
                derecha = pila_afns.pop()
                izquierda = pila_afns.pop()
                self.concatenacion(izquierda,derecha)
                pila_afns.append(izquierda)
            elif element == '|':
                afn = AFN(alfabeto, {}, 0, [1])
                derecha = pila_afns.pop()
                izquierda = pila_afns.pop()
                afn.agregar_transicion(afn.estado_inicial,derecha.estado_inicial+1,'E')
                self.concatenacion(afn,izquierda)
                final_izquierda = afn.estados_finales[0]
                afn.agregar_transicion(afn.estado_inicial,afn.estados_finales[0]+1,'E')
                afn.estados_finales[0]+=1
                self.concatenacion(afn,derecha)
                afn.agregar_transicion(afn.estados_finales[0],afn.estados_finales[0]+1,'E')
                afn.estados_finales[0]+=1
                afn.agregar_transicion(final_izquierda,afn.estados_finales[0],'E')
                pila_afns.append(afn)
            elif element == '*':
                afn = AFN(alfabeto, {}, 0, [1])
                izquierda = pila_afns.pop()
                afn.agregar_transicion(afn.estado_inicial,izquierda.estado_inicial+1,'E')
                self.concatenacion(afn,izquierda)
                afn.agregar_transicion(afn.estados_finales[0],afn.estados_finales[0]+1,'E')
                afn.agregar_transicion(afn.estados_finales[0],izquierda.estado_inicial+1,'E')
                afn.estados_finales[0]+=1
                afn.agregar_transicion(afn.estado_inicial,afn.estados_finales[0],'E')
                pila_afns.append(afn)
            elif element == '+':
                afn = AFN(alfabeto, {}, 0, [1])
                izquierda = pila_afns.pop()
                afn.agregar_transicion(afn.estado_inicial,izquierda.estado_inicial+1,'E')
                self.concatenacion(afn,izquierda)
                afn.agregar_transicion(afn.estados_finales[0],afn.estados_finales[0]+1,'E')
                afn.agregar_transicion(afn.estados_finales[0],izquierda.estado_inicial+1,'E')
                afn.estados_finales[0]+=1
                afn.agregar_transicion(afn.estado_inicial,afn.estados_finales[0],'E')
                self.concatenacion(izquierda,afn)
                pila_afns.append(izquierda)
        print(pila_afns[0].funcion_transicion)

# reg = RegextoAFN('(a|b)*ab|b')
# reg.generar_afn()
