###############################################################
# Etapa 1
# 	- Archivo: lexer.py
#   - Lenguaje: Python
#   - Version: 3
# 	- Enero-Marzo 2020
# 	- CI-3725
# 	- Funcion: Analizador lexicografico del lenguaje Willy*
# 	
#	 - Autores:
#		-Fabio Suarez  12-10578
#       -Luis  Marval  12-10620
#  
################################################################

import ply.lex as lex
import re
import codecs
import os
import sys

arrToks = [] #Lista que contiene todos los tokens(contiene los tokens de comentarios de linea y bloque)
errToks = [] # Lista que contiene todos los errores (Solo se imprime el primero)
tokenList = [] # Lista que contiene los tokens del lenguaje willy* con los que se van a trabajar (ignora comentario de linea y bloque)
row = 0
col = 0

reservadas = {
            # Palabras simples que son tokens del lenguaje
            'World': 'TkWorld',
            'Wall': 'TkWall',
            'from': 'TkFrom',
            'to': 'TkTo',
            'north': 'TkNorth',
            'east': 'TkEast',
            'south': 'TkSouth',
            'west': 'TkWest',
            'of': 'TkOf',
            'color': 'TkColor',
            'red': 'TkRed',
            'blue': 'TkBlue',
            'magenta': 'TkMagenta',
            'cyan': 'TkCyan',
            'green': 'TkGreen',
            'yellow': 'TkYellow',
            'Place': 'TkPlace',
            'at': 'TkAt',
            'in': 'TkIn',
            'basket': 'TkBasket',
            'Start': 'TkStart',
            'heading': 'TkHeading',
            'Basket': 'TkBasketUppercase',
            'capacity': 'TkCapacity',
            'with': 'TkWith',
            'initial': 'TkInitial',
            'value': 'TkValue',
            'Goal': 'TkGoalUppercase',
            'is': 'TkIs',
            'Final': 'TkFinal',
            'goal': 'TkGoal',
            'willy': 'TkWilly',
            'objects': 'TkObjects',
            'and': 'TkAnd',
            'or': 'TkOr',
            'not': 'TkNot',
            'on': 'TkOn',
            'terminate': 'TkTerminate',
            'if':'TkIf',        
            'then': 'TkThen',
            'else': 'TkElse',
            'repeat': 'TkRepeat',
            'times': 'TkTimes',
            'while': 'TkWhile',
            'do':'TkDo',
            'begin': 'TkBegin',
            'end': 'TkEnd',
            'define': 'TkDefine',
            'as': 'TkAs',
            'move': 'TkMove',
            'pick': 'TkPick',
            'drop': 'TkDrop',
            'set': 'TkSet',
            'clear': 'TkClear',
            'flip': 'TkFlip',
            'found': 'TkFound',
            'carrying': 'TkCarrying',
            'true':'TkTrue', 
            'false':'TkFalse',
            'Boolean':'TkBoolean'
}

tokens = list(reservadas.values()) + ['TkId', 'TkObjectType', 'TkBeginWorld', 'TkEndWorld', 'TkBeginTask',
'TkEndTask', 'TkTurnLeft','TkTurnRight','TkFrontClear','TkLeftClear', 'TkRightClear', 'TkLookingNorth',
'TkLookingEast', 'TkLookingSouth', 'TkLookingWest', 'TkLineComment','TkOpenPar', 'TkClosePar', 'TkSemicolon', 'TkBlockComment','TkNum']

# Expresiones regulares para reconocer los siguientes simbolos del lenguaje
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkSemicolon = r'\;'
t_TkLineComment = r'\-\-.*'

# Se definen funciones con regex asociadas para reconocer los tokens restantes
def t_TkObjectType(t):
    r'\b(Object-type)\b'
    return t

def t_TkBeginWorld(t):
    r'\b(begin-world)\b'
    return t

def t_TkEndWorld(t):
    r'\b(end-world)\b'
    return t

def t_TkBeginTask(t):
    r'\b(begin-task)\b'
    return t

def t_TkEndTask(t):
    r'\b(end-task)\b'
    return t

def t_TkTurnLeft(t):
    r'\b(turn-left)\b'
    return t

def t_TkTurnRight(t):
    r'\b(turn-right)\b'
    return t

def t_TkFrontClear(t):
    r'\b(front-clear)\b'
    return t

def t_TkLeftClear(t):
    r'\b(left-clear)\b'
    return t

def t_TkRightClear(t):
    r'\b(right-clear)\b'
    return t

def t_TkLookingNorth(t):
    r'\b(looking-north)\b'
    return t

def t_TkLookingEast(t):
    r'\b(looking-east)\b'
    return t

def t_TkLookingSouth(t):
    r'\b(looking-south)\b'
    return t

def t_TkLookingWest(t):
    r'\b(looking-west)\b'
    return t

def t_TkBlockComment(t):
    r'\{\{([^{}]*|(\{[^{}]*\}|\{\}[^{}]*|[^{}]*\{\}))+\}\}'
    t.type = 'TkBlockComment'
    #t.value = t.value
    return t

def t_TkNum(t):
    r'\b\d+\b'
    if (int(t.value) >= 0):
        t.value = int(t.value) 
        t.type = 'TkNum'
        return t

# Reconoce los IDs del lenguaje los cuales estan compuestos por por valores alfanumericos y _
# Los IDs no pueden comenzar por numeros
def t_TkId(t):
    r'\b[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'TkId')
    #t.type = 'TkId'
    #t.value = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignoramos espacios y tabs
t_ignore  = ' \t'

# calcula el numero de  columna.
#     input es el texto que entra como string
#     token es una instancia de un token
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Funcion: t_error
# Maneja el proceso de tokens no validos
# almacenandolos en una lista.
def t_error(t):
    errToks.append(t)
    t.lexer.skip(1)

#Funcion para imprimir todos los tokens
def imprimirB(t):
    for aux in arrToks:
        if(aux.type == 'TkId'):
            print( str(aux.type) +'(valor="' + str(aux.value)+'", linea='+ str(aux.lineno) +', columna='+ str(find_column(lexer.lexdata,aux)) + ')')
        elif(aux.type == 'TkNum'):
            print( str(aux.type) +'(valor=' + str(aux.value)+', linea=' + str(aux.lineno) +', columna='+ str(find_column(lexer.lexdata,aux)) + ')')
        elif(aux.type == 'TkBlockComment' or aux.type == 'TkLineComment'):
            pass
        else:
            print( str(aux.type)+'(linea=' + str(aux.lineno) +', columna='+ str(find_column(lexer.lexdata,aux)) + ')')

''' Funcion: inputError
    Retorna:
        -True si existe parametro de entrada desde terminal
        -False en caso contrario'''
def inputError():
    if (len(sys.argv)==2):
        return True
    else:
        return False

''' Funcion: exist_File
 Entrada:
   -String que representa el nombre de un archivo
 Retorna:
   -True si existe un archivo con el nombre ingresado
   -False en caso contrario'''

def exist_File(fname):
    if (os.path.isfile(fname)):
        return True
    else:
        return False

#Funcion Principal main
def main():
    #Construimos el lexer
    lexer = lex.lex()
    # Se verifica que se pasen los parametros de manera correcta
    if (inputError()):
        first_arg = sys.argv[1]
        # Se revisa si el nombre del archivo recibido existe 
        if (exist_File(first_arg)):
            input_file = open(first_arg, "r")
            lexer.input(input_file.read())
            while True:
                tok = lexer.token()
                if not tok: break
                arrToks.append(tok)
            # Si existe un error, se procedea imprimir el primer error
            if (len(errToks)!=0):
                for aux in errToks :
                    print("Error: Caracter ilegal encontrado '" + str(aux.value[0]) +"' en linea " + str(aux.lineno) + " , columna " + str(find_column(lexer.lexdata,aux)) + ". \n")
                    break
            # En caso de no haber errores, se proceden a imprimir todos los tokens
            else:
                for aux in arrToks:
                    if(aux.type == 'TkBlockComment' or aux.type == 'TkLineComment'):
                        pass
                    else:
                        tokenList.append(aux)

                # Generando la impresion del archivo
                tokenFinal = arrToks[-1]                # Ultimo token del programa
                k = 0                                   # Iterador sobre la lista de tokens
                tamTokenList = (len(tokenList))         # Cantidad de tokens
                lineaFinal = int(tokenFinal.lineno)     # Numero de la ultima linea del programa

                fila = 1
                imprimir = ""                           # Variable que contiene todo el string del output
                space = " "                             # espacio entre tokens de la misma fila
                booleano = False                        # ya he pasado por esta fila

                while (True):
                    # si la fila es menor que la fila del token pasamos a la siguiente linea
                    if (fila < tokenList[k].lineno):
                        imprimir = imprimir + "\n"
                        fila = fila + 1
                        booleano = False

                    elif(fila == tokenList[k].lineno):
                        # si estamos al principio de una fila imprimos n espacios segun la cantidad de columnas en las que se encuentre el primer token
                        if(booleano == False):
                            imprimir = imprimir + space * (find_column(lexer.lexdata,tokenList[k]) - 1)
                            if(tokenList[k].type == 'TkId'):
                                imprimir = imprimir +  str(tokenList[k].type) +'(valor="' + str(tokenList[k].value)+'", linea='+ str(tokenList[k].lineno) +', columna='+ str(find_column(lexer.lexdata,tokenList[k])) + ')'
                            elif(tokenList[k].type == 'TkNum'):
                                imprimir = imprimir + str(tokenList[k].type) +'(valor=' + str(tokenList[k].value)+', linea='+ str(tokenList[k].lineno) +', columna='+ str(find_column(lexer.lexdata,tokenList[k])) + ')'
                            else:
                                imprimir = imprimir + str(tokenList[k].type)+'(linea=' + str(tokenList[k].lineno) +', columna='+ str(find_column(lexer.lexdata,tokenList[k])) + ')'
                            
                            #Se coloca True dado a que la linea ya fue visitada por primera vez
                            booleano = True
                        
                        # si estamos en una linea ya visitada y falta un token por imprimir se proceden a realizar dicha accion
                        else:
                            imprimir = imprimir + space
                            if(tokenList[k].type == 'TkId'):
                                imprimir = imprimir +  str(tokenList[k].type) +'(valor="' + str(tokenList[k].value)+'", linea=' + str(tokenList[k].lineno) +', columna='+ str(find_column(lexer.lexdata,tokenList[k])) + ')'
                            elif(tokenList[k].type == 'TkNum'):
                                imprimir = imprimir + str(tokenList[k].type) +'(valor=' + str(tokenList[k].value)+', linea=' + str(tokenList[k].lineno) +', columna='+ str(find_column(lexer.lexdata,tokenList[k])) + ')'
                            else:
                                imprimir = imprimir + str(tokenList[k].type)+'(linea=' + str(tokenList[k].lineno) +', columna='+ str(find_column(lexer.lexdata,tokenList[k])) + ')'
                                                
                        # Procedemos a chequear el siguiente token
                        if (k < tamTokenList - 1): 
                            k = k + 1
                        
                        #Si ya recorrimos todos los tokens de la lista procedemos a salir e imprimir 
                        else:
                            break
                
                print(imprimir)

            input_file.close()
        
        else:
            print("Error: Imposible abrir el archivo \""+str(first_arg)+"\" \n") 
    else:
        print("Error: Entrada vacia")

if __name__ == '__main__':
      main()