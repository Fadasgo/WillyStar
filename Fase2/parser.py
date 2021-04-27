###############################################################
# Etapa 2
# 	- Archivo: parser.py
#   - Lenguaje: Python
#   - Version: 3
# 	- Enero-Marzo 2020
# 	- CI-3725
# 	- Funcion: Analizador Sintactico y parte del Semantico del lenguaje Willy* (fase 2)
# 	
#	 - Autores:
#		-Fabio Suarez  12-10578
#       -Luis  Marval  12-10620
#  
################################################################

import ply.yacc as yacc
from lexer import tokens
import logging
import sys

logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
l = []

# Diccionario que contiene todos los mundos definidos en el programa
mundo = {}

#class Task:

class Node:
    def __init__(self, type, tag=None, children=None, leaf=None, value=None,mundo=0):
        self.type = type
        self.mundo = mundo
        if children:
            self.children = children
        else:
            self.children = []
        self.tag = tag
        if leaf:
            self.leaf = leaf
        else:
            self.leaf = []
        self.value = value
        self.blocks = []

precedence = (
	('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('nonassoc', 'TkNot'),
    ('left', 'TkThen'),
    ('left', 'TkElse')

	
)

# regla inicial de la gramatica
def p_start(p):
    ''' start : program '''
    p[0] = p[1]

def p_program(p):
    ''' program : worldBlock
                | taskBlock
                | worldBlock program
                | taskBlock program 
    '''
    #print("Block \n")
    if (len(p) == 2):
        p[0] = Node('Block', children=[p[1]],leaf=None)
    elif (len(p) == 3):
        p[0] = Node('Block', children=[p[1],p[2]],leaf=None)

def p_worldBlock(p):
    ''' worldBlock : TkBeginWorld identificador worldSeq TkEndWorld 
                | TkBeginWorld identificador TkEndWorld
    
    '''
    #print("World-Block \n")
    if (len(p) == 4):
        p[0] = Node('World-Block', children=[p[2]],leaf=[p[1],p[3]])
    elif (len(p) == 5):
        p[0] = Node('World-Block', children=[p[2],p[3]],leaf=[p[1],p[4]])


def p_worldSeq(p):
    ''' worldSeq : worldInst
                | worldInst worldSeq
    '''
    #print("World-Seq \n")
    if(len(p) == 2):
        p[0] = Node('worldSequencing', children=[p[1]])
    elif (len(p) == 3):
        p[0] = Node('worldSequencing', children=[p[1],p[2]])

def p_worldInst(p):
    ''' worldInst : TkSemicolon
                | worldDef TkSemicolon 
                | wallDef TkSemicolon 
                | objectTypeDef TkSemicolon 
                | placeDef TkSemicolon 
                | startDef TkSemicolon 
                | basketDef TkSemicolon 
                | booleanDef TkSemicolon 
                | goalDef TkSemicolon 
                | finalGoalDef TkSemicolon 
    '''

    #print("WorldInst \n")
    if (len(p)==2):
        p[0] = Node('WorldInst',leaf=[p[1]])
    elif (len(p)==3):
        p[0] = Node('WorldInst', children=[p[1]], leaf=[p[2]])

def p_worldDef(p):
    ''' worldDef : TkWorld num num
    '''

    p[0] = Node('worldDef', children=[p[2],p[3]],leaf=[p[1]])

def p_wallDef(p):
    ''' wallDef : TkWall direction TkFrom num num TkTo num num
    '''
    p[0] = Node('wallDef', children=[p[2],p[4],p[5],p[7],p[8]],leaf=[p[1],p[3],p[6]])

def p_objectTypeDef(p):
    ''' objectTypeDef : TkObjectType identificador TkOf TkColor color
    '''
    p[0] = Node('objectTypeDef', children=[p[2],p[5]],leaf=[p[1],p[3],p[4]],tag='Object-Type')

def p_placeDef(p):
    ''' placeDef : TkPlace num TkOf identificador TkAt num num
            | TkPlace num TkOf identificador TkIn TkBasket 
    '''
    if (len(p) == 8):
        p[0] = Node('placeDef', children=[p[2],p[4],p[6],p[7]],leaf=[p[1],p[3],p[5]])
    elif (len(p) == 7):
        p[0] = Node('placeDef', children=[p[2],p[4]],leaf=[p[1],p[3],p[5],p[6]])


def p_startDef(p):
    ''' startDef : TkStart TkAt num num TkHeading direction
    '''
    p[0] = Node('startDef', children=[p[3],p[4],p[6]],leaf=[p[1],p[2],p[5]])

def p_basketDef(p):
    ''' basketDef : TkBasketUppercase TkOf TkCapacity num
    '''
    p[0] = Node('basketDef', children=[p[4]],leaf=[p[1],p[2],p[3]])

#excluir TkNum (Verificacion)
def p_booleanDef(p):
    ''' booleanDef : TkBoolean identificador TkWith TkInitial TkValue valor 
    '''
    # terminal no puede tomar el valor de num
    p[0] = Node('booleanDef', children=[p[2],p[6]],leaf=[p[1],p[3],p[5]])

def p_goalDef(p):
    ''' goalDef : TkGoalUppercase identificador TkIs TkWilly TkIs TkAt num num
            | TkGoalUppercase identificador TkIs num identificador TkObjects TkIn TkBasketUppercase
            | TkGoalUppercase identificador TkIs num identificador TkObjects TkAt num num 
    '''
    if (len(p) == 9):
        if (p[4] == 'willy'):
            p[0] = Node('goalDef', children=[p[2],p[7],p[8]],leaf=[p[1],p[3],p[4],p[5],p[6]],tag="goal")
        else:
            p[0] = Node('goalDef', children=[p[2],p[4],p[5]],leaf=[p[1],p[3],p[6],p[7],p[8]],tag="goal")
        
    else:
        p[0] = Node('goalDef', children=[p[2],p[4],p[5],p[8],p[9]],leaf=[p[1],p[3],p[6],p[7]],tag="goal")

def p_finalGoalDef(p):
    ''' finalGoalDef : TkFinal TkGoal TkIs finalGoal
    '''
    p[0] = Node('finalGoalDef', children=[p[4]],leaf=[p[1],p[2],p[3]])

def p_direction(p):
    ''' direction : TkNorth
                | TkEast
                | TkSouth
                | TkWest 
    '''
    p[0] = Node('direction', leaf=[p[1]],value=p[1])

def p_color(p):
    ''' color : TkRed
            | TkBlue
            | TkMagenta
            | TkCyan
            | TkGreen
            | TkYellow
    '''
    p[0] = Node('color', leaf=[p[1]],value=p[1])

# tipo de TkId puede ser goalTest o Booleano
def p_finalGoal(p):
    ''' finalGoal : identificador
                | TkOpenPar finalGoal TkClosePar
                | TkNot finalGoal
                | finalGoal TkAnd finalGoal
                | finalGoal TkOr finalGoal
    '''
    if (len(p) == 4):
        if (p[2] == 'and' or p[2] == 'or'):
            # Caso BinOp and/or
            p[0] = Node('finalGoalBinOp', children=[p[1],p[3]],leaf=[p[2]],tag="finalGoal")
        else:
            #Caso parentesis
            p[0] = Node('finalGoalParen', children=[p[2]],leaf=[p[1], p[3]],tag="finalGoal")
    elif (len(p) == 3):
        # Caso not
        p[0] = Node('finalGoalNot', children=[p[2]],leaf=[p[1]], tag="finalGoal")
    else:
        # caso ID
        p[0] = Node('finalGoalID', children=[p[1]], leaf = [], tag="finalGoal")

def p_valor(p):
    ''' valor : TkTrue
            | TkFalse 
    '''
    p[0] = Node('terminal', value=p[1],leaf=[p[1]], tag="bool")

def p_identificador(p):
    ''' identificador : TkId
    '''
    p[0] = Node('terminal', value=p[1],leaf=[p[1]])

def p_num(p):
    ''' num : TkNum
    '''
    p[0] = Node('terminal', value=p[1],leaf=[p[1]], tag="int")

# PARTE DE LAS INSTRUCCIONES DE TASK

def p_taskBlock(p):
    '''
    taskBlock : TkBeginTask identificador TkOn identificador TkEndTask
        | TkBeginTask identificador TkOn identificador taskSeq TkEndTask 
    '''
    #print("Task-Block \n")
    if (len(p)) == 6:
        p[0] = Node('taskBlock', children=[p[2],p[4]],leaf=[p[1],p[3],p[5]])
    
    else:
        p[0] = Node('taskBlock', children=[p[2],p[4],p[5]],leaf=[p[1],p[3],p[6]])

def p_taskSeq(p):
    ''' taskSeq : taskSeq TkSemicolon
            | taskSeq taskSeq
            | taskInst
    '''
    #print("Task-Seq \n")
    if (len(p) == 2):
        p[0] = Node('taskSeq', children=[p[1]],leaf=[]) 

    else:
        if(p[2]==';'):
            p[0] = Node('taskSeq', children=[p[1]],leaf=[p[2]])

        else:
            p[0] = Node('taskSeq', children=[p[1],p[2]], leaf = [])      

def p_taskInst(p):
    ''' taskInst : identificador TkSemicolon
                | primitiveInst TkSemicolon 
                | ifInst
                | repeatInst
                | whileInst
                | beginInst
                | defineInst

    '''
    if (len(p) == 2):
        p[0] = Node('taskInst', children=[p[1]])
    else:
        p[0] = Node('taskInst', children=[p[1]],leaf=[p[2]])

def p_primitiveInst(p):
    ''' primitiveInst : TkMove
                    | TkTurnLeft
                    | TkTurnRight 
                    | TkTerminate
                    | TkPick identificador
                    | TkDrop identificador
                    | TkSet identificador
                    | TkClear identificador
                    | TkFlip identificador
                    | TkSet identificador TkTo valor
    '''
    if (len(p) == 2):
        p[0] = Node('primitiveInst', children=[],leaf=[p[1]], value=p[1])
    elif (len(p) == 3):
        p[0] = Node('primitiveInst', children=[p[2]],leaf=[p[1]])
    else:
        p[0] = Node('primitiveInst', children=[p[2],p[4]],leaf=[p[1],p[3]])

def p_test(p):
    ''' test : literal
            | TkFound TkOpenPar identificador TkClosePar
            | TkCarrying TkOpenPar identificador TkClosePar
            | TkNot test
            | TkOpenPar test TkClosePar
            | test TkAnd test
            | test TkOr test
    '''
    if (len(p) == 2):
        p[0] = Node('test-lit', children=[p[1]], leaf=[],tag="bool")
    elif (len(p) == 3):
        p[0] = Node('test-not', children=[p[2]],leaf=[p[1]], tag="bool")
    elif (len(p) == 4):
        if (p[2] == 'and' or p[2] == 'or'):
            p[0] = Node('test-binOp', children=[p[1], p[3]],leaf=[p[2]], tag="bool")
        else:
            p[0] = Node('test-paren', children=[p[2]],leaf=[p[1],p[3]], tag="bool")
    else:
        p[0] = Node('test-fc', children=[p[3]],leaf=[p[1],p[2],p[4]], tag="bool")

def p_literal(p):
    ''' literal : TkTrue
            | TkFalse 
            | TkId
            | TkFrontClear
            | TkLeftClear
            | TkRightClear
            | TkLookingNorth
            | TkLookingEast
            | TkLookingSouth
            | TkLookingWest 
    '''
    p[0] = Node('literal',leaf=[p[1]],value=p[1], tag="bool")

def p_ifInst(p):
    ''' ifInst : TkIf test TkThen taskInst TkElse taskInst
    | TkIf test TkThen taskInst
    '''
    if (len(p) == 5):
        p[0] = Node('ifInst', children=[p[2],p[4]],leaf=[p[1],p[3]])
    else:
        p[0] = Node('ifInst', children=[p[2],p[4],p[6]],leaf=[p[1],p[3],p[5]])

def p_repeatInst(p):
    ''' repeatInst : TkRepeat num TkTimes taskInst
    '''
    p[0] = Node('repeatInst', children=[p[2],p[4]], leaf=[p[1],p[3]])

def p_whileInst(p):
    ''' whileInst : TkWhile test TkDo taskInst
    '''
    p[0] = Node('whileInst', children=[p[2],p[4]],leaf=[p[1],p[3]])

def p_defineInst(p):
    ''' defineInst : TkDefine identificador TkAs taskInst
    '''
    p[0] = Node('defineInst', children=[p[2],p[4]],leaf=[p[1],p[3]])

def p_beginInst(p):
    ''' beginInst : TkBegin taskSeq TkEnd
    '''
    p[0] = Node('beginInst', children=[p[2]],leaf=[p[1],p[3]])

# Error rule for syntax error
def p_error(p):
    print("No es un token " + str(p.value) + " en la linea " + str(p.lineno) + ", columna " + str(p.lexpos + 1) + " \n")
    sys.exit()

def parser():
    return yacc.yacc(debug=True)
