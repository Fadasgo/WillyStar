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
errors = []

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
'TkLookingEast', 'TkLookingSouth', 'TkLookingWest', 'TkOpenPar', 'TkClosePar', 'TkSemicolon', 'TkNum']

# Expresiones regulares para reconocer los siguientes simbolos del lenguaje
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkSemicolon = r'\;'
#t_TkLineComment = r'\-\-.*'
t_ignore_TkCommentsBlock = r'{{(.|\n)[^{}]*}}'        
t_ignore_TkComments = r'\-\-.*'
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

#def t_TkBlockComment(t):
#    r'\{\{([^{}]*|(\{[^{}]*\}|\{\}[^{}]*|[^{}]*\{\}))+\}\}'
#    t.type = 'TkBlockComment'
#    #t.value = t.value

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
#def t_error(t):
#    errToks.append(t)
#    t.lexer.skip(1)

def t_error(t):
    global errors
    errString = ('Error: Unexpected character \"'+str(t.value[0])+'\" in row '+str(t.lineno))
    errors.append(errString)
    t.lexer.skip(1)

#Funcion para imprimir todos los tokens
def imprimirB(t):
    for aux in arrToks:
        if(aux.type == 'TkId'):
            print( str(aux.type) +'(valor="' + str(aux.value)+'", linea='+ str(aux.lineno) +', columna='+ str(find_column(lexer.lexdata,aux)) + ')')
        elif(aux.type == 'TkNum'):
            print( str(aux.type) +'(valor=' + str(aux.value)+', linea=' + str(aux.lineno) +', columna='+ str(find_column(lexer.lexdata,aux)) + ')')
        elif(aux.type == 't_ignore_TkCommentsBlock' or aux.type == 't_ignore_TkComments'):
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

def tokenize(lexer, data):
    lexer.input(data)
    global program_tokens
    global errors
    program_tokens = []
    errors = []
    for tok in lexer:
        if(tok.type == 't_ignore_TkCommentsBlock' or tok.type == 't_ignore_TkComments'):
            pass
        else:
            program_tokens.append(tok) 
        program_tokens.append(tok)
    return program_tokens, errors

def lexer():
	return lex.lex()