import sys
from time import sleep
import copy

class world:
    def __init__(self, id=None, scopeNum=None):
        self.id = id
        self.scopeId = scopeNum
        self.cesta = []
        self.capacity = 1
        self.size = [1,1]                          # Columnas y filas
        self.mundo = [[0]]
        self.objects = {}                        # Se almacena todos los objetos referentes al mundo
        self.booleans = {}                       # Se almacenan todos los booleanos del mundo
        self.goals = {}
        self.finalGoal = []                         # Se guarda objeto de tipo final goal
        self.startAt = [1,1,"north"]               # Columna,fila, direccion 
        self.contadorStartAt = False               # se vuelve True si fue modificado una vez StartAt
        self.contadorCapacity = False              # se vuelve True si fue modificado una vez capacity
        self.contadorMundo = False                 # se vuelve True si fue modificado una vez mundo
        self.contadorFgoal = 0                     # Tiene que haber exactamente un final goal

# class TaskBlock sobre el cual se realizara la ejecucion 
class task:
    def __init__(self, id, block_id, m):
        self.idTarea = id
        self.scopeStart = block_id
        self.lookingWillyAt = copy.deepcopy(m.startAt[2])
        self.position = copy.deepcopy([m.startAt[0], m.startAt[1]]) # Columna y fila
        self.cesta = copy.deepcopy(m.cesta)
        self.capacity = copy.deepcopy(m.capacity)
        self.nombreMundo = copy.deepcopy(m.id)
        self.size = copy.deepcopy(m.size)
        self.mundo = copy.deepcopy(m.mundo)
        self.booleans = copy.deepcopy(m.booleans)
        self.objects = copy.deepcopy(m.objects)
        self.goals = copy.deepcopy(m.goals)
        self.finalGoal = copy.deepcopy(m.finalGoal)
        self.inst = ""  # Contiene la instruccion que ejecuta en dicho paso (esto es para la impresion paso a paso)
        self.item = ""
        self.valor = ""

# Clase que simula un nuevo bloque
class Block:
    def __init__(self, id=None, variables=None):
        self.id = id
        if variables:
            self.variables = variables
        else:
            self.variables = {}

    def insert_variable(self, id, dataType):
        if id in self.variables:
            print("Error de Ejecucion: No se puede redeclarar el identificador "+ id + " dentro del mismo scope \n")
            sys.exit()
        else:
            self.variables[id] = dataType

    def remove_variable(self, id):
        if id in self.variables:
            del self.variables[id]

class define:
    def __init__(self, id, tree=None, tipo=None):
        self.id = id
        self.tree = tree
        self.type = "func"


class objecto:
    def __init__(self, id, color, n = 0):
        self.id = id
        self.color = color
        self.type = "object"
        self.quantity = 0
        # self.quantityCesta = 0

class booleans:
    def __init__(self, id, valor):
        self.id = id
        self.valor = valor
        self.type = "boolean"

class goal:
    def __init__(self, id, caso,lista):
        self.id = id
        self.caso = ""  # el caso permite al clasificar el goal si es de Willy is at , objects in basket o objects at pos
        self.lista = lista
        self.type = "goal"

class fGoal:
    def __init__(self, tree):
        self.tree = tree                 # el caso permite al clasificar el goal si es de Willy is at , objects in basket o objects at pos
        self.lista = []                  # Se guarda cada identificador en la lista
        self.type = "Finalgoal"

# Permite calcular las indexaciones de willy
# Donde la fila 1 de willy es la fila n de la matriz
def willyIndexToMatrix(totalRows, willyAtRow):
    return totalRows - willyAtRow

#Permite saber si se puede ingresar un elemento en la cesta de willy
def cestaCapacidad(cesta,capacidad):
    inBasket = 0
    for elem in cesta:
        inBasket = inBasket + elem.quantity
    
    if inBasket < capacidad:
        return True
    elif inBasket >= capacidad:
        return False

class interfaceOutput:
    def __init__(self, instruction, world, fil, col, objName):
        self.instruction = instruction
        self.world = world
        self.willyFil = fil
        self.willyCol = col
        self.objName = objName


class Semantic:
    def __init__(self, tarea, flag, segundos):
        self.block_counter = -1
        self.blocks = []
        self.blocks_parents = []  # importante para reconocer el define id as begin
        self.iterators = []
        self.tree = None
        self.mundos = {}                             # Contiene los mundos y su informacion
        self.tareas = {}                             # Contiene los ids de las tareas y su info
        self.scopes = {}                
        self.impresion = []
        self.tarea = tarea
        self.flag = flag
        self.segundos = segundos
        self.starting = True
        self.finalGoal = False
        

    # Permite calcular las indexaciones de willy para interfaz
    # Donde la fila 1 de willy es la fila n de la matriz
    def willyIndexToMatrixUI(self,totalRows, willyAtRow):
        return totalRows - willyAtRow

    # probablemente esto sea con la estructura block
    def execute(self, tree):
        self.tree = tree
        self.e_start(self.tree)            

    def e_start(self,node):
        #print("Nodo start \n")
        self.e_program(node)
        if not self.tarea in self.tareas:
            print("\n\n La tarea pasada por consola no se encuentra dentro del script ejecutado \n\n")
            sys.exit()

    def e_program(self,node):
        #print("Nodo program \n")
        for child in node.children:
            if child.type == "World-Block":
                self.block_counter += 1
                self.e_worldBlock(child,self.block_counter) #crear scope y objeto mundo nuevo para luego agregar en la tabla de hash
            elif child.type == "taskBlock":
                self.block_counter += 1
                self.blocks.append(Block(self.block_counter))
                self.e_taskBlock(child,self.block_counter)            
            elif child.type == "Block":
                self.e_program(child)

    def e_worldBlock(self,node,block_id):
        #creamos objeto que va a almacenar todas las caracteristicas que se
        # almacenaran dentro del diccionario
        m = world()
        m.scopeId = block_id

        for child in node.children:
            #print(child.type + "\n")
            if child.type == "terminal": # Nombre del Mundo
                identificador = str(child.value)
                # Verificamos que dicho ID no haya sido utilizado anteriormente
                if identificador in self.mundos:
                    print("Error: " +  " Problema con el ID : '" + identificador + "' Ya se encuentra un mundo con ese nombre \n")
                    sys.exit()
                elif identificador in self.tareas:
                    print("Error: " +  " Problema con el ID : '" + identificador + "'Ya se encuentra una tarea con ese nombre \n")
                    sys.exit()                
                m.id = identificador
                self.mundos[identificador] = m
                self.scopes[identificador] = [m.scopeId,"world"]
            elif child.type == "worldSequencing": #Instrucciones de mundo
                self.e_worldSequence(child,m)
                # Verificamos que exista una instruccion Final Goal
                w = self.mundos[m.id]
                if len(w.finalGoal) == 0:
                    print("Error: en el mundo '" + m.id + "' es necesaria una instruccion Final Goal \n")
                    sys.exit()
        
    
    def e_worldSequence(self,node,m):
        for child in node.children:
            if child.type == "worldSequencing":
                self.e_worldSequence(child,m)

            elif child.type == "WorldInst":
                self.mundos[m.id] = m
                self.e_worldInst(child,m)
    
    def e_worldInst(self,node,m):
        for child in node.children:
            if child.type == "worldDef":
                self.e_worldDef(child,m)

            elif child.type == "wallDef":
                self.e_wallDef(child,m)
                    
            elif child.type == "objectTypeDef":
                self.e_objectTypeDef(child,m)
                    
            elif child.type == "placeDef":
                self.e_placeDef(child,m)
                    
            elif child.type == "startDef":
                self.e_startDef(child,m)
                    
            elif child.type == "basketDef":
                self.e_basketDef(child,m)
                    
            elif child.type == "booleanDef":
                self.e_booleanDef(child,m)
                    
            elif child.type == "goalDef":
                self.e_goalDef(child,m)
                    
            elif child.type == "finalGoalDef":
                self.e_finalGoalDef(child,m)
        
    def e_worldDef(self,node,m):
        identificador = m.id
        m1 = self.mundos[identificador]

        if int(node.children[0].value) < 1 or int(node.children[1].value) < 1:
            print("Error: Un mundo no puede tener al cero o un negativo como indexacion en willy* (conflicto en Def Mundo con id " + identificador +" )\n")
            sys.exit()
        
        if m1.contadorMundo == True:
            print("Error: La instruccion de Def World se puede utilizar a lo sumo una vez por mundo. (conflicto: Def World en el mundo " + identificador +" )\n")
            sys.exit()

        else:
            m1.contadorMundo = True
            m1.size[0] = int(node.children[0].value)  # Columna
            m1.size[1] = int(node.children[1].value)  # Fila
            m1.mundo = [[0 for col in range(m1.size[0])] for row in range(m1.size[1])]
        self.mundos[identificador] = m1

    def e_wallDef(self,node,m):
        identificador = m.id
        m1 = self.mundos[identificador]
        col0 = int(node.children[1].value)
        fil0 = int(node.children[2].value)
        col1 = int(node.children[3].value)
        fil1 = int(node.children[4].value)
        willyFil = int(m.startAt[1])
        willyCol = int(m.startAt[0])

        if col0 < 1 or fil0 < 1 or col1 < 1 or fil1 < 1 :
            print("Error: Un mundo no puede tener al cero o un negativo como indexacion en el lenguaje de willy* ( conflicto: En la Def Wall de mundo con id '"+ identificador +"' )\n")
            sys.exit()
        
        # Verificamos que no este fuera del rango del mundo la pared que se desea colocar
        if col0 > m1.size[0] or col1 > m1.size[0] or fil0 > m1.size[1] or fil1 > m1.size[1] :
            print("Error: No se puede colocar una pared fuera del dominio del mundo '" + identificador + "' \n")
            sys.exit()

        if node.children[0].value == "north":
            # Columnas iguales y fil1 >= fil0
            if col0 == col1 and fil0 <= fil1 :
                # Se resta uno debido a la diferencia entre las indexacion de python y willy* que es de uno
                for i in range(fil0, fil1+1):
                    #print(str(i)+"   "+str(willyIndexToMatrix(m1.size[1], i)))
                    if m1.mundo[willyIndexToMatrix(m1.size[1], i)][col0-1] != 0 and m1.mundo[willyIndexToMatrix(m1.size[1], i)][col0-1] != "wall":
                        print("Error: No se puede poner una pared en una posicion donde se encuentra un objeto.\n"+ " Problema en el mundo "+ m1.id +"\n")
                        sys.exit()
                    if willyFil == i  and willyCol == col0:
                        print("Error: No se puede poner una pared en una posicion donde se encuentra Willy.\n"+" Problema en el mundo "+ m1.id +"\n")
                        sys.exit()

                    m1.mundo[willyIndexToMatrix(m1.size[1], i)][col0-1] = "wall"
                

                # Actualizamos el objeto con los datos relacionados a la pared
                self.mundos[identificador] = m1
            else:
                print("Error: Declaracion de muro inconsistente para la direccion north en el mundo '"+m1.id +"' \n")
                sys.exit()
        
        elif node.children[0].value == "south":
            # Columnas iguales
            if col0 == col1 and fil0 >= fil1:
                for i in range(fil1, fil0+1):
                    #print(str(i)+"   "+str(willyIndexToMatrix(m1.size[1], i)))
                    if m1.mundo[willyIndexToMatrix(m1.size[1], i)][col0-1] != 0 and m1.mundo[willyIndexToMatrix(m1.size[1], i)][col0-1] != "wall":
                        print("Error: No se puede poner una pared en una posicion donde se encuentra un objeto o Willy.\n Problema en el mundo "+ m1.id+"\n")
                        sys.exit()

                    if willyFil == i  and willyCol == col0:
                        print("Error: No se puede poner una pared en una posicion donde se encuentra Willy.\n"+ " Problema en el mundo "+ m1.id +"\n")
                        sys.exit()

                    m1.mundo[willyIndexToMatrix(m1.size[1], i)][col0-1] = "wall"

                # Actualizamos el objeto con los datos relacionados a la pared
                self.mundos[identificador] = m1
            else:
                print("Error: Declaracion de muro inconsistente para la direccion south en el mundo "+m1.id +"\n")
                sys.exit()

        # Revisar sentido del east
        elif node.children[0].value == "east":
            if col0 <= col1 and fil0 == fil1 :
                for j in range(col0-1, col1):
                    #print(str(j) + "  " + str(willyIndexToMatrix(m1.size[1], fil0)))
                    if m1.mundo[willyIndexToMatrix(m1.size[1], fil0)][j] != 0 and m1.mundo[willyIndexToMatrix(m1.size[1], fil0)][j] != "wall":
                        print("Error: No se puede poner una pared en una posicion donde se encuentra un objeto o Willy.\n"+" Problema en el mundo "+ m1.id +"\n")
                        sys.exit()

                    if willyFil == fil0  and willyCol == j + 1:
                        print("Error: No se puede poner una pared en una posicion donde se encuentra Willy.\n"+ " Problema en el mundo "+ m1.id +"\n")
                        sys.exit()

                    m1.mundo[willyIndexToMatrix(m1.size[1], fil0)][j] = "wall"
                
                # Actualizamos el objeto con los datos relacionados a la pared
                self.mundos[identificador] = m1
            else:
                print("Error: Declaracion de muro inconsistente para la direccion east en el mundo "+m1.id +"\n")
                sys.exit()
        
        # Revisar sentido del west
        elif node.children[0].value == "west":
            if col1 <= col0 and fil1 == fil0 :
                for j in range(col1-1, col0):
                    #print(str(j) + "  " + str(willyIndexToMatrix(m1.size[1], fil0)))
                    if m1.mundo[willyIndexToMatrix(m1.size[1], fil0)][j] != 0 and m1.mundo[willyIndexToMatrix(m1.size[1], fil0)][j] != "wall":
                        print("Error: No se puede poner una pared en una posicion donde se encuentra un objeto o Willy.\n"+ " Problema en el mundo "+ m1.id +"\n")
                        sys.exit()

                    if willyFil == fil0  and willyCol == j + 1 :
                        print("Error: No se puede poner una pared en una posicion donde se encuentra Willy.\n"+ " Problema en el mundo "+ m1.id +"\n")
                        sys.exit()

                    m1.mundo[willyIndexToMatrix(m1.size[1], fil0)][j] = "wall"
                
                # Actualizamos el objeto con los datos relacionados a la pared
                self.mundos[identificador] = m1
            else:
                print("Error: Declaracion de muro inconsistente para la direccion west en el mundo "+m1.id +"\n")
                sys.exit()

    def e_objectTypeDef(self,node,m):
        identificador = m.id
        m1 = self.mundos[identificador]
        nombre = str(node.children[0].value)
        color = str(node.children[1].value)
        o1 = objecto(nombre, color)
        # El id a asignar no puede estar en objeto
        if nombre in m1.booleans :
            print("Error: Ya existe un elemento boolean con el identificador "+ nombre +" que ya fue declarado en el mundo '"+ identificador + "' (No se puede redeclarar el id) \n")
            sys.exit()

        if nombre in m1.goals :
            print("Error: Ya existe un elemento goal con el identificador "+ nombre +" que ya fue declarado en el mundo '"+ identificador + "' (No se puede redeclarar el id) \n")
            sys.exit()

        if nombre in m1.objects :
            print("Error: Ya existe un objeto con el identificador "+ nombre +" que ya fue declarado en el mundo '"+ identificador + "' (No se puede redeclarar el id) \n")
            sys.exit()

        #Actualizamos la tabla de objetos para el mundo actual(sin repeticion)
        m1.objects[nombre] = o1

        # Actualizamos el mundo agregando el ultimo objeto actualizado
        self.mundos[identificador] = m1


    def e_placeDef(self,node,m):
        identificadorMundo = m.id
        m1 = self.mundos[identificadorMundo]
        n = int(node.children[0].value)
        identificadorObj = str(node.children[1].value)
        b = False #Permite saber si se encuentra el objeto en la casilla del mundo
        
        if not identificadorObj in m1.objects:
            print("Error: El objeto "+ identificadorObj+ " no existe o no ha sido definido como tipo \n")
            sys.exit()

        o1 = m1.objects[identificadorObj]
        # Verificamos que n != 0, fil y col != 0, fil y col dentro del rango del mundo y que id sea un objeto existente
        # Place n id at col fil
        if len(node.children) == 4 :
            o2 = objecto(id = o1.id,color = o1.color)
            fil = int(node.children[3].value)
            col = int(node.children[2].value)

            if n == 0:
                print("Error: No se puede colocar cero objetos en la instruccion de Place para el mundo "+ identificadorMundo + " \n")
                sys.exit()
            if fil < 1 or col < 1:
                print("Error: No se puede colocar columna o fila de indexacion cero o negativa en la instruccion de Place para el mundo "+ identificadorMundo + " \n")
                sys.exit()
            if m1.size[0] < col or m1.size[1] < fil :
                print("Error: No se puede colocar un objeto fuera del rango del mundo "+ identificadorMundo + " ( Error en la instruccion Place) \n")
                rsys.exit()
            # Se procede a revisar el id exista y efectivamente sea un objeto
            if identificadorObj not in m1.objects :
                print("Error: El identificador pasado en la instruccion Place del mundo "+  identificadorMundo + " no es un objeto \n")
                sys.exit()

            # Se coloca el objeto en su casilla respectiva del mundo
            if m1.mundo[willyIndexToMatrix(m1.size[1], fil)][col-1] == "wall":
                print("Error: No se puede colocar un objeto en una posicion donde ya fue definida una pared. Problema en el mundo con id: '"+  identificadorMundo + "' \n")
                sys.exit()

            elif m1.mundo[willyIndexToMatrix(m1.size[1], fil)][col-1] == 0:
                o2.quantity = n
                m1.mundo[willyIndexToMatrix(m1.size[1], fil)][col-1] = [o2]
            
            elif isinstance(m1.mundo[willyIndexToMatrix(m1.size[1], fil)][col-1],list):
                b1 = False
                for x in m1.mundo[willyIndexToMatrix(m1.size[1], fil)][col-1]:
                    # buscamos por objetos a ver si el que vamos a introducir ya se encuentra en la lista
                    # y solo actualizamos la cantidad de objetos de ese tipo
                    if isinstance(x, objecto) and x.id == identificadorObj:
                        b1 = True
                        x.quantity = x.quantity + n

                if b1 == False:
                    o2.quantity = n
                    m1.mundo[willyIndexToMatrix(m1.size[1], fil)][col-1].append(o2)

            self.mundos[identificadorMundo] = m1
                
        # Place n id in basket
        elif len(node.children) == 2:
            o2 = objecto(id = o1.id,color = o1.color)
            b1 = False
            acum = 0
            if n == 0:
                print("Error: No se puede colocar cero objetos en canasta de willy en el mundo "+ identificadorMundo + " \n")
                sys.exit()

            if identificadorObj not in m1.objects :
                print("Error: El identificador pasado en la instruccion Place del mundo "+  identificadorMundo + " no es un objeto \n")
                sys.exit()
            
            # acum contiene la cantidad de objetos guardados en la cesta de willy
            for x in m1.cesta:
                if isinstance(x,objecto):
                    acum = acum + x.quantity

            
            # acum contiene la cantidad de elementos que hay en la cesta
            # n posee la cantidad de elementos a agregar en la cesta
            if acum + n <= m1.capacity:
                for x in m1.cesta:
                    if isinstance(x,objecto) and x.id == identificadorObj:
                        b1 = True
                        x.quantity = x.quantity + n
                        #print(x.quantity)
                        #o2.quantity = x.quantity
                
                if b1 == False:
                    o2.quantity = n
                    m1.cesta.append(o2)
                
                self.mundos[identificadorMundo] = m1
            elif acum + n > m1.capacity:
                print("Error: No se pueden ingresar más elementos de la capacidad que tiene la cesta. Problema en el mundo " + identificadorMundo + " \n")
                sys.exit()

    def e_startDef(self,node,m):
        identificador = m.id
        m1 = self.mundos[identificador]
        fila = int(node.children[1].value)
        columna = int(node.children[0].value)
        direction = str(node.children[2].value)
        columnaDimMundo = int(m1.size[0])
        filaDimMundo = int(m1.size[1])

        if columna < 1 or fila < 1 :
            print("Error: willy no puede comenzar en una posicion con indexacion cero o negativa (Def Start- en el mundo " + identificador +" )\n")
            sys.exit()
        
        if columna > columnaDimMundo or fila > filaDimMundo :
            print("Error: willy no puede comenzar en una indexacion fuera de las dimensiones del mundo (Def Start- en el mundo " + identificador +" )\n")
            sys.exit()
        
        # Verificamos que dicha posicion de inicio no tenga una pared
        if m1.mundo[willyIndexToMatrix(filaDimMundo, fila)][columna-1] == "wall":
            print("Error: willy no puede comenzar en una indexacion donde se encuentre una pared (Def Start- en el mundo " + identificador +" )\n")
            sys.exit()       
        
        # Es coloca el booleano para que no acepta mas instrucciones de este tipo
        if m1.contadorStartAt == True:
            print("Error: La instruccion de inicio de posicion de willy solo se puede usar a los sumo 1 vez (Def Start en el mundo " + identificador +" )\n")
            sys.exit()

        elif m1.contadorStartAt == False:
            m1.contadorStartAt = True
            m1.startAt = [columna, fila, direction] 
            self.mundos[identificador] = m1
        
        #print(m1.mundo)

    def e_basketDef(self,node,m):
        identificador = m.id
        m1 = self.mundos[identificador]
        if int(node.children[0].value) < 1:
            print("Error: No se le puede asignar capacidad 0 o menor a la cesta de willy* (Def Basket- en el mundo " + identificador +" )\n")
            sys.exit()
        
        if m1.contadorCapacity == True:
            print("Error: La instruccion de capacidad de la cesta solo se puede usar a los sumo 1 vez (Def Basket en el mundo " + identificador +" )\n")
            sys.exit()
        
        else:
            m1.contadorCapacity = True
            m1.capacity = int(node.children[0].value) 
            self.mundos[identificador] = m1


    def e_booleanDef(self,node,m):
        identificador = m.id
        m1 = self.mundos[identificador]
        nombre = str(node.children[0].value)
        v = None
        if (node.children[1].value == "true"):
            v = True
        elif (node.children[1].value == "false"):
            v = False
        b1 = booleans(nombre,v)
        # El id a asignar no puede estar en objeto
        
        if nombre in m1.booleans :
            print("Error: Ya existe un elemento boolean con el identificador "+ nombre +" ya fue declarado en el mundo "+ identificador + "(No se puede redeclarar el id) \n")
            sys.exit()

        if nombre in m1.goals :
            print("Error: Ya existe un elemento goal con el identificador "+ nombre +" ya fue declarado en el mundo "+ identificador + "(No se puede redeclarar el id) \n")
            sys.exit()

        if nombre in m1.objects :
            print("Error: Ya existe un objeto con el identificador "+ nombre +" ya fue declarado en el mundo "+ identificador + "(No se puede redeclarar el id) \n")
            sys.exit()

        #Actualizamos la tabla de boolean para el mundo actual
        m1.booleans[nombre] = b1
        
        # Actualizamos el mundo agregando el ultimo objeto actualizado
        self.mundos[identificador] = m1

    def e_goalDef(self,node,m):
        # Revisar columnas y filas != 0 y dentro de los limites del mundo (listo)
        # n objetos en la cesta no pueden ser mayor que la capacidad de la cesta 
        # el id del objeto debe existir y ser tipo objeto
        identificadorMundo = m.id
        m1 = self.mundos[identificadorMundo]
        idGoal = str(node.children[0].value)
        columnaDimMundo = int(m1.size[0])
        filaDimMundo = int(m1.size[1])

        if idGoal in m1.goals:
            print("Error: El goal con id '"+ idGoal +"' no pudo ser agregado en el mundo '"+ identificadorMundo +"' dado que ya existe un goal con ese nombre \n")
            sys.exit()
        if idGoal in m1.booleans:
            print("Error: El goal con id '"+ idGoal +"' no pudo ser agregado en el mundo '"+ identificadorMundo +"' dado que ya existe un boolean definido con ese nombre \n")
            sys.exit()
        # Borrar si no deberia haber conflicto con objetos
        if idGoal in m1.objects:
            print("Error: El goal con id '"+ idGoal +"' no pudo ser agregado en el mundo '"+ identificadorMundo +"' dado que ya existe un objeto definido con ese nombre \n")
            sys.exit() 

        # Se procede a guarda el goal
        if len(node.children) == 3:
            if node.leaf[3] == "is":
                goalName = str(node.children[0].value)
                col = int(node.children[1].value)
                fil = int(node.children[2].value)

                if col < 1 or fil < 1 :
                    print("Error: Un goal no puede estar en una posicion con indexacion cero o negativa (Def Goal- "+ idGoal +" en el mundo " + identificadorMundo +" )\n")
                    sys.exit()
                
                if col > columnaDimMundo or fil > filaDimMundo :
                    print("Error: Un goal no puede estar en una posicion fuera del mundo (Def Goal- "+ idGoal +" en el mundo " + identificadorMundo +" )\n")
                    sys.exit()

                if fil == 0 or col == 0:
                    print("Error: Las fila o columna del goal con nombre '"+ idGoal + "' en el mundo '"+ identificadorMundo + "'no puede tener indexacion 0 \n")
                    sys.exit()
                caso = "willyAt"            # willy llega a la posicion X del mundo
                #lista = node.children
                lista = [goalName, col, fil]
                #print(lista)
                g1 = goal(id=goalName,caso=caso,lista=lista)
                g1.id = goalName
                g1.caso = caso
                g1.lista = lista
                #Se actualiza en la tabla de los mundos
                m1.goals[goalName] = g1
                self.mundos[identificadorMundo] = m1
        
            elif node.leaf[3] == "in":
                # verificar que identificador del objeto exista
                # que la cesta tenga la capacidad de almacenarlo
                goalName = str(node.children[0].value)
                cantidad = int(node.children[1].value)
                nombreObj = str(node.children[2].value)

                if nombreObj not in m1.objects :
                    print("Error: En la instruccion Goal con id '"+ idGoal +"' dentro del mundo '"+ identificadorMundo + "' el identificador de los items que se van a poner en la cesta tiene que existir y deber ser de tipo objeto \n")
                    sys.exit()
                
                if m1.capacity < cantidad:
                    print("Error: En la instruccion Goal con id '"+ idGoal +"' dentro del mundo '"+ identificadorMundo + "' la cantidad de objetos a querer introducir en la cesta es mayor a su capacidad \n")
                    sys.exit()

                caso = "objectsInBasket"    # X objetos de id Y en la cesta de Willy
                lista = [goalName, cantidad, nombreObj]
                #print(lista)
                #lista = node.children
                g1 = goal(id=goalName,caso=caso,lista=lista)
                g1.id = goalName
                g1.caso = caso
                g1.lista = lista
                #Se actualiza en la tabla de los mundos
                m1.goals[goalName] = g1
                self.mundos[identificadorMundo] = m1

        elif len(node.children) == 5:
            goalName = str(node.children[0].value)
            col = int(node.children[3].value)
            fil = int(node.children[4].value)
            cantidad = int(node.children[1].value)
            nombreObj = str(node.children[2].value)
            
            if col < 1 or fil < 1 :
                print("Error: Un goal no puede estar en una posicion con indexacion cero o negativa (Def Goal- "+ idGoal +" en el mundo " + identificadorMundo +" )\n")
                sys.exit()
            
            if col > columnaDimMundo or fil > filaDimMundo :
                print("Error: Un goal no puede estar en una posicion fuera del mundo (Def Goal- "+ idGoal +" en el mundo " + identificadorMundo +" )\n")
                sys.exit()
            
            if nombreObj not in m1.objects :
                print("Error: En la instruccion Goal con id '"+ idGoal +"' dentro del mundo '"+ identificadorMundo + "' el identificador de los items que se van a poner en la cesta tiene que existir y deber ser de tipo objeto \n")
                sys.exit()

            if m1.capacity < cantidad:
                print("Error: En la instruccion Goal con id '"+ idGoal +"' dentro del mundo '"+ identificadorMundo + "' la cantidad de objetos a querer introducir en la cesta es mayor a su capacidad \n")
                sys.exit()
            
            caso = "objectsAt"              # X objetos de id Y en la posicion Z del mundo
            lista = [goalName,cantidad,nombreObj,col,fil]
            g1 = goal(id=goalName,caso=caso,lista=lista)
            g1.id = goalName
            g1.caso = caso
            g1.lista = lista
            #Se actualiza en la tabla de los mundos
            m1.goals[goalName] = g1
            self.mundos[identificadorMundo] = m1
        
    def e_finalGoalDef(self,node,m):
        # tiene que contener exactamente un finalGoal
        # los ids tienen que ser de tipo goal o booleans
        identificadorMundo = m.id
        m1 = self.mundos[identificadorMundo]
        fg1 = fGoal(node)
        
        if m1.contadorFgoal == 0:
            m1.contadorFgoal = 1
        else:
            print("Error: Tiene que existir exactamente una instruccion de tipo Final Goal en el mundo '"+ identificadorMundo +"' \n")
            sys.exit()
        
        # Verificamos que todos los ids dentro del final goal sean de tipo  booleans o goal
        if node.type == "finalGoalDef":
            self.checkFgoal(node.children[0],m1)
        
        # guardar fg1 en su mundo respectivo
        m1.finalGoal.append(fg1)
        self.mundos[identificadorMundo] = m1
    
    # Verifica los tipos de los ids dentro de un final goal que sean goal o booleans
    def checkFgoal(self, expression,m):
        # Caso en el que sea un id
        if len(expression.leaf) == 0:
            b1 = False      # Permite verificar si el id es de tipo boolean
            b2 = False      # Permite verificar si el id es de tipo goal
            identificador = str(expression.children[0].value)
            if identificador in m.booleans:
                b1 = True
            if identificador in m.goals:
                b2 = True

            if b1 == False and b2 == False:
                print("Error: Dentro de la instruccion Final Goal, el identificador '"+ identificador +"' en el mundo '"+m.id+"' no es de tipo Goal o Boolean \n")
                #raise SystemExit
                sys.exit()
            #fg1.lista.append(identificador)
       
        # Caso de expresion con not
        elif expression.leaf[0] == "not":
            self.checkFgoal(expression.children[0],m)
        
        # Caso de expresion and/or
        elif expression.leaf[0] == "and" or expression.leaf[0] == "or":
            self.checkFgoal(expression.children[0],m)
            self.checkFgoal(expression.children[1],m)
        
        # Caso de expresion (exp)
        elif expression.leaf[0] == "(":
            self.checkFgoal(expression.children[0],m)
    
    # TASKs
    # Instrucciones de Tareas
    def e_taskBlock(self,node,block_id):
        nombreMundo = str(node.children[1].value)
        nombreTarea = str(node.children[0].value)
        if nombreMundo not in self.mundos:
            print("Error: El mundo asociado a la tarea '" + nombreTarea + "' no existe \n")
            sys.exit()
        m1 = self.mundos[nombreMundo]      # Objeto de tipo mundo con todas sus declaraciones 
        
        if nombreTarea in self.mundos:
            print("Error: La tarea '" + nombreTarea + "' no puede llamarse igual a un mundo que ya fue definido \n")
            sys.exit()
        
        if nombreTarea in self.tareas:
            print("Error: La tarea '" + nombreTarea + "' no puede llamarse igual a otra tarea que ya fue definida \n")
            sys.exit()
        
        t = task(nombreTarea,block_id,m1)
        
        # Guardamos en la tabla de las tareas
        self.tareas[nombreTarea] = t
        
        # Caso en el que la tarea tiene instrucciones / para el caso contrario se procede de manera directa a la verificacion del final goal
        if len(node.children) == 3:
            child = node.children[2]
            if child.type == "taskSeq":
                self.e_taskSeq(child, t, block_id)

        t1 = self.tareas[t.idTarea]
        self.mundos[t.idTarea] = m1
 

        # Aqui se puede hacer la condicion de si la variable NombreTarea == a la tarea pasada por consola se procede a imprimir el mundo de 
        # acuerdo al flag pasado  
        if (t1.idTarea == self.tarea):
            print('********************************')
            print('Tarea ', self.tarea, ' Recorrido ', self.flag)
            print('\n')
            print('********************************')
            print('Willy esta en row: '+str(t1.position[1])+' col: '+str(t1.position[0]) )
            print('Looking At ', t1.lookingWillyAt)
            print('\n')
            print('********************************')
            print('\n')

            # impresion final
            tCopy = copy.deepcopy(self.tareas[t.idTarea])
            self.printMatrizWilly(tCopy.mundo, tCopy.position)
        

            # Procedemos en esta parte a hacer la verificacion de final goal para el mundo (falta replicar esta llamada en el terminate para poder verificar alla)
            # Buscamos el  sub-arbol que contiene los datos de la ejecucion del finalGoal asociado a la tarea
            fg = t1.finalGoal[0]
            # Se verifican las condiciones del final goal
            check = self.finalGoalCheck(fg.tree.children[0],t)
            self.finalGoal = check
            if check == True:
                print("\n#####################################################################\n")
                print("\n La condicion meta del programa se ha cumplido de manera exitosa. \n")
                print("\n#####################################################################\n")

            elif check == False:
                print("\n#####################################################################\n")
                print("\n La condicion meta del programa NO se cumplio. El final goal evaluó Falso  \n")
                print("\n#####################################################################\n")

    #Funcion para imprimir la matriz
    def printMatrizWilly(self, matriz, position):
        xes = [] # arreglo de los objetos que son x en el mapa
        mundo = ''
        for r in range(len(matriz)): # filas
            fila = ''
            for c in range(len(matriz[r])): # columnas
                willyLocation = (c == position[0] - 1 and r == willyIndexToMatrix(len(matriz), position[1]) )
                if (type(matriz[r][c]) == list):
                    if (willyLocation):
                        if (type(matriz[r][c][0]) != str ):
                            matriz[r][c].insert(0, 'row: '+str(willyIndexToMatrix(len(matriz), r))+','+' col: '+str(c+1))
                        xes.append(matriz[r][c])
                        fila = fila + '\t' + 'willy-X'
                    else:
                        if (type(matriz[r][c][0]) != str ):
                            matriz[r][c].insert(0, 'row: '+str(willyIndexToMatrix(len(matriz), r))+','+' col: '+str(c+1))

                        xes.append(matriz[r][c])
                        fila = fila + '\t' + 'X'
                else:
                    if (willyLocation and (matriz[r][c] == 0 or matriz[r][c] == 'willy')):
                        fila = fila + '\t' + 'willy'
                    elif (matriz[r][c] == 'willy' ):
                        fila = fila + '\t' + str(0)
                    else:
                        fila = fila + '\t' + str(matriz[r][c])
            mundo = mundo + '\n' + fila
        print(mundo + '\n')
        # impresion lista X
        for l in xes:
            for e in l:
                if (e != 'willy' and type(e) != str):
                    print('X = ', e.__dict__)
                elif(e != 'willy'):
                    print('posicion ', e)
            print('\n')
        

    #Funcion para verificar si se cumple el final goal 
    def finalGoalCheck(self, node, t):
        t1 = self.tareas[t.idTarea]
        totalRow = int(t1.size[1])
        totalCol = int(t1.size[0])

        if node.type == "finalGoalBinOp":
            
            if node.leaf[0] == "and":
                leftOp = self.finalGoalCheck(node.children[0], t1)
                rightOp = self.finalGoalCheck(node.children[1], t1)

                return (leftOp and rightOp)

            elif node.leaf[0] == "or":
                leftOp = self.finalGoalCheck(node.children[0], t1)
                rightOp = self.finalGoalCheck(node.children[1], t1)

                return (leftOp or rightOp)

        
        elif node.type == "finalGoalParen":
            exp = self.finalGoalCheck(node.children[0], t1)
            return exp

        elif node.type == "finalGoalNot":
            exp = self.finalGoalCheck(node.children[0], t1)
            return (not exp)
            
        elif node.type == "finalGoalID":
            b7 = False # Nos permite saber que si no es booleana la variable hay que verificar que sea goal
            valor = str(node.children[0].value)
            # Chequeamos que efectivamente sea un goal y que no sea un id de booleano u objeto
            if valor in t1.booleans:
                b7 = True

            if valor in t1.objects:
                print("Error de ejecucion: El id '"+ valor +"' pasado dentro de la instruccion de final goal es de tipo objeto. Se esperaba algo de goal o booleano. \n Conflicto en el mundo con id '" +t1.nombreMundo + "' \n")
                sys.exit()

            if b7 == False:
                if valor not in t1.goals:
                    print("Error de ejecucion: El id '"+ valor +"' pasado dentro de la instruccion de final goal no se encuentra dentro los goals ni booleanos declarados. \n Conflicto en el mundo con id '" +t1.nombreMundo + "' \n")
                    sys.exit()
                
                g = t1.goals[valor]

                # Luego procedemos a verificar si se cumplio el goal, para retornar el valor booleano
                
                if g.caso == "willyAt":
                    lista = g.lista
                    col = int(lista[1])
                    fil = int(lista[2])
                    
                    if totalRow < fil or totalCol < col:
                        return False
                    
                    # si es una pared o un 0 retorna false, para el otro caso si posee la cantidad de elementos retorna true
                    if t1.mundo[willyIndexToMatrix(totalRow,fil)][col-1] == "wall":
                        return False
                    
                    if col == t1.position[0] and fil == t1.position[1]:
                        return True
                    
                    elif col != t1.position[0] or fil != t1.position[1]:
                        return False
                    

                elif g.caso == "objectsInBasket":
                    lista = g.lista
                    cantidadObj = int(lista[1])
                    nombreObj = str(lista[2])

                    b = False
                    for x in t1.cesta:
                        if (x.id == nombreObj) and (x.quantity == cantidadObj):
                            return True
                    
                    if b == False:
                        return False

                elif g.caso == "objectsAt":
                    lista = g.lista
                    cantidadObj = int(lista[1])
                    nombreObj = str(lista[2]) 
                    col = int(lista[3])
                    fil = int(lista[4])

                    if totalRow < fil or totalCol < col:
                        return False

                    if t1.mundo[willyIndexToMatrix(totalRow,fil)][col-1] == "wall":
                        return False

                    if t1.mundo[willyIndexToMatrix(totalRow,fil)][col-1] == 0:
                        return False
                    
                    b = False
                    for x in t1.mundo[willyIndexToMatrix(totalRow,fil)][col-1]:
                        if (x.id == nombreObj) and (x.quantity == cantidadObj):
                            return True
                        else:
                            pass
                    return False

            elif b7 == True:
                # Traemos el valor del booleano y retornamos su valor
                val = t1.booleans[valor]
                #print(val.valor)
                if val.valor == True:
                    return True
                
                elif val.valor == False:
                    return False

    def e_taskSeq(self, node, t , block_id, parent_id = None):
        child = node.children
        if child[0].type == "taskInst" and len(child) == 1:
             self.e_taskInst(child[0], t, block_id)
        elif len(node.leaf) == 1 and child[0].type == "taskSeq":
             self.e_taskSeq(child[0], t, block_id)
        elif len(child) == 2:
             self.e_taskSeq(child[0], t, block_id)
             self.e_taskSeq(child[1], t, block_id)
    
    def e_taskInst(self, node, t, block_id, parent_id = None):
        child = node.children[0]
        t1 = self.tareas[t.idTarea]
        if child.type == "terminal":
            
            identificador = str(child.value)
            # serian aquellas instrucciones almacenadas en un id (no puede ser de tipo objeto, booleana o goal)                
            if identificador in t1.booleans:
                print("Error: a se encuentra otro elemento con el id '"+ identificador +"' y es de tipo boolean en la tarea '"+ t.idTarea +"' \n")
                sys.exit()

            if identificador in t1.goals:
                print("Error: a se encuentra otro elemento con el id '"+ identificador +"' y es de tipo goal en la tarea '"+ t.idTarea +"' \n")
                sys.exit()

            if identificador in t1.objects:
                print("Error: a se encuentra otro elemento con el id '"+ identificador +"' y es de tipo objeto en la tarea '"+ t.idTarea +"' \n")
                sys.exit()

            tx = self.tareas[t.idTarea]
            tx.inst = "funcion"
            tx.item = identificador
            
            initScope = t.scopeStart
            b = False # Se busca la variable definida desde el marco mas interno al mas externo

            for x in reversed(self.blocks):
                #print(x.id)
                if identificador in x.variables:
                    var = x.variables[identificador]
                    #Vemos si es una funcion
                    if isinstance(var,define):
                        # Nos permite saber que fue conseguida una funcion en algun marco de pila
                        b = True
                        # Le ponemos al objeto de tipo define el id asociado
                        var.id = identificador
                        primeraInst = var.tree

                        if primeraInst.type == "beginInst":
                            self.block_counter += 1
                            self.blocks.append(Block(self.block_counter))
                            self.blocks_parents.append(block_id)
                            new_block_id = self.block_counter
                            self.e_beginInst(primeraInst, t, new_block_id, block_id)
                            self.blocks.pop(len(self.blocks)-1)
                            self.blocks_parents.pop(len(self.blocks_parents)-1)

                        elif primeraInst.type == "ifInst":
                            self.e_ifInst(primeraInst, t, block_id)

                        elif primeraInst.type == "repeatInst":
                            self.e_repeatInst(primeraInst, t, block_id)
                        
                        elif primeraInst.type == "whileInst":
                            self.e_whileInst(primeraInst, t, block_id)
                    
                    break
                
                # Si llegamos al marco de pila inicial y todavia no se ha conseguido el id
                if x.id == initScope:
                    break

            if b == False:
                print("Error de ejecucion: El identificador '" +identificador+ "' no ha sido definido hasta el momento de su llamada. \n Conflicto en la tarea '"+t.idTarea+"' \n")
                sys.exit()

        elif child.type == "primitiveInst":
            self.e_primitiveInst(child, t, block_id)

            
        elif child.type == "ifInst":
            tx = self.tareas[t.idTarea]
            tx.inst = "If-Inst"
            self.e_ifInst(child, t, block_id)
        
        elif child.type == "repeatInst":
            tx = self.tareas[t.idTarea]
            tx.inst = "Repeat"
            self.e_repeatInst(child, t, block_id)
        
        elif child.type == "whileInst":
            tx = self.tareas[t.idTarea]
            tx.inst = "While"
            self.e_whileInst(child, t, block_id)
        
        elif child.type == "defineInst":
            # Se encarga en agregar valores a la tabla en el marco actual
            tx = self.tareas[t.idTarea]
            tx.inst = "define"
            self.e_defineInst(child, t, block_id)


        elif child.type == "beginInst":
            tx = self.tareas[t.idTarea]
            tx.inst = "begin"
            self.e_beginInst(child, t, block_id)

    def e_primitiveInst(self, node, t, block_id, parent_id = None):
        # Sacamos de la tabla de Hash los valores actualizados de la instruccion
        t1 = self.tareas[t.idTarea]

        col = int(t1.position[0])
        row = int(t1.position[1])
        totalCol = int(t1.size[0])
        totalRow = int(t1.size[1])

        if len(node.children) == 0 and len(node.leaf) == 1:
            if node.leaf[0] == "move":
                # Impresion antes de inicial
                if (self.starting and t1.idTarea == self.tarea):
                    tz = copy.deepcopy(t1.mundo)
                    filW = copy.deepcopy(t1.position[1])
                    colW = copy.deepcopy(t1.position[0])
                    out = interfaceOutput(instruction= "move", world=tz, fil = filW, col = colW, objName=" ")
                    self.impresion.append(out)
                    # Impresion Manual
                    if (self.flag == 'manual'):
                        tCopy = copy.deepcopy(self.tareas[t.idTarea])
                        self.printMatrizWilly(tCopy.mundo, tCopy.position)

                    elif (self.flag == 'auto' and self.segundos != None): # impresion automatica
                        tCopy = copy.deepcopy(self.tareas[t.idTarea])
                        self.printMatrizWilly(tCopy.mundo, tCopy.position)
                    self.starting = False

                    ''' CASO 1 Verificar que en la direccion a la que mira y se va a 
                            mover willy no hay una pared(Devolver error de ejecucion si no esta libre la pos)'''
                    ''' CASO 2 Verificar que la posicion nueva no se encuentre fuera del
                            mundo (Devolver error de ejecucion si no esta libre la pos)'''
                    ''' CASO 3 Si la posicion es un cero o una lista mover al willy 
                                y actualizar el atributo posicion de willy de la tarea'''
                if t1.lookingWillyAt == "north":
                    if row + 1 > totalRow:
                        print("Error de ejecucion: Willy no puede moverse en la orientacion north ya que se sale de la indexacion del mundo.\n  Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()
                    
                    # Verificamos que willy no se intente mover a una posicion donde hay una pared
                    elif t1.mundo[willyIndexToMatrix(totalRow,row + 1)][col-1] == "wall":
                        print("Error de ejecucion: Willy no puede moverse en la orientacion north a una posicion en la que se encuentra una pared. \n  Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()

                    else:
                        # movemos a willy a la nueva posicion
                        t1.position = [col, row+1] # Mantenemos la convecion columna,fila

                elif t1.lookingWillyAt == "west":
                    
                    if col-1 < 1:
                        print("Error de ejecucion: Willy no puede moverse en la orientacion west ya que se sale de la indexacion del mundo.\n  Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()

                    # Verificamos que willy no se intente mover a una posicion donde hay una pared
                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col-2] == "wall":
                        print("Error de ejecucion: Willy no puede moverse en la orientacion west a una posicion en la que se encuentra una pared. \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()

                    else:
                        # movemos a willy a la nueva posicion
                        t1.position = [col-1, row] # Mantenemos la convecion columna, fila

                    
                elif t1.lookingWillyAt == "south":
                    # Verificamos que willy no se intente mover a una posicion donde hay una pared
                    
                    # Si nos salimos del mapa en la direccion south entonces devolver error de ejecucion
                    if row-1 < 1:
                        print("Error de ejecucion: Willy no puede moverse en la orientacion south ya que se sale de la indexacion del mundo.\n  Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()
                    
                    elif t1.mundo[willyIndexToMatrix(totalRow,row - 1)][col-1] == "wall":
                        print("Error de ejecucion: Willy no puede moverse en la orientacion south a una posicion en la que se encuentra una pared. \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()

                    else:
                        # movemos a willy a la nueva posicion
                        t1.position = [col, row-1] # Mantenemos la convecion columna,fila
                    
                elif t1.lookingWillyAt == "east":
                    
                    # Verificamos que willy no se intente mover a una posicion donde hay una pared
                    if col+1 > totalCol:
                        print("Error de ejecucion: Willy no puede moverse en la orientacion east ya que se sale de la indexacion del mundo.\n  Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()

                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col] == "wall":
                        print("Error de ejecucion: Willy no puede moverse en la orientacion east a una posicion en la que se encuentra una pared. \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()

                    else:
                        # movemos a willy a la nueva posicion
                        t1.position = [col+1, row] # Mantenemos la convecion columna,fila
                
                tx = self.tareas[t.idTarea]
                tCopy = copy.deepcopy(self.tareas[t.idTarea])
                filW = copy.deepcopy(tx.position[1])
                colW = copy.deepcopy(tx.position[0])
                tz = copy.deepcopy(tx.mundo)
                out = interfaceOutput(instruction= "move", world=tz, fil = filW, col = colW, objName=" ")
                tx.inst = "move"
                self.impresion.append(out)
                if (t1.idTarea == self.tarea):
                    if (self.flag == 'manual'): # Impresion Manual
                        ## hacer input para cada tarea
                        # impresion intrucciones
                        myInput = input("presione enter para continuar")
                        print(tx.inst, "", "")
                        willyWorld = copy.deepcopy(tCopy.mundo)
                        willyPosition = copy.deepcopy(tCopy.position)
                        self.printMatrizWilly(willyWorld, willyPosition)

                    elif (self.flag == 'auto'): # impresion automatica
                        if (self.segundos != None): # se tienen segundos
                        # impresion intruccione
                            sleep(self.segundos) # entre cada paso
                            print(tx.inst, "", "")
                            willyWorld = copy.deepcopy(tCopy.mundo)
                            willyPosition = copy.deepcopy(tCopy.position)
                            self.printMatrizWilly(willyWorld, willyPosition)

            elif node.leaf[0] == "turn-left":
                if t1.lookingWillyAt == "north":
                    t1.lookingWillyAt = "west"
                elif t1.lookingWillyAt == "west":
                    t1.lookingWillyAt = "south"
                elif t1.lookingWillyAt == "south":
                    t1.lookingWillyAt = "east"
                elif t1.lookingWillyAt == "east":
                    t1.lookingWillyAt = "north"
                
                tx = self.tareas[t.idTarea]
                tx.inst = "turn-left"

            elif node.leaf[0] == "turn-right":
                if t1.lookingWillyAt == "north":
                    t1.lookingWillyAt = "east"
                elif t1.lookingWillyAt == "west":
                    t1.lookingWillyAt = "north"
                elif t1.lookingWillyAt == "south":
                    t1.lookingWillyAt = "west"
                elif t1.lookingWillyAt == "east":
                    t1.lookingWillyAt = "south"
                
                tx = self.tareas[t.idTarea]
                tx.inst = "turn-right"

            elif node.leaf[0] == "terminate":
                if (t.idTarea == self.tarea):
                    tCopy = copy.deepcopy(self.tareas[t.idTarea])
                    self.printMatrizWilly(tCopy.mundo, tCopy.position) # imprimir antes de terminar
                    fg = t1.finalGoal[0]
                    # Se verifican las condiciones del final goal
                    tx = self.tareas[t.idTarea]
                    tx.inst = "terminate"
                    check = self.finalGoalCheck(fg.tree.children[0],t)
                    self.finalGoal = check
                    if check == True:
                        print("\n#####################################################################\n")
                        print("\n La condicion meta del programa se ha cumplido de manera exitosa. \n")
                        print("\n#####################################################################\n")
                    elif check == False:
                        print("\n#####################################################################\n")
                        print("\n La condicion meta del programa NO se cumplio. El final goal evaluó Falso  \n")
                        print("\n#####################################################################\n")
                    sys.exit()
            
        elif len(node.children) == 1 and len(node.leaf) == 1 :
            identificador = str(node.children[0].value)
            if node.leaf[0] == "pick":

                if identificador not in t1.objects:
                    print("Error de ejecucion: No se le puede aplicar la instruccion pick al id '"+identificador+" dado a que no es un objeto \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()

                if t1.mundo[willyIndexToMatrix(totalRow,row)][col-1] == 0:
                    print("Error de ejecucion: No se puede agarrar un elemento en una casilla donde no existe dicho objeto \n. Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()

                # Revisamos la lista de los objetos
                elif isinstance(t1.mundo[willyIndexToMatrix(totalRow,row)][col-1],list):
                    # devuelve true si existe capacidad para agregar cosas en la cesta
                    if cestaCapacidad(t1.cesta,t1.capacity) == False:
                        # En el caso que sea una lista de tipo [obj]
                        print("Error de ejecucion: El objeto que se intenta agarrar con id '"+ identificador +"' no se puede almacenar en la cesta porque no hay espacio. \n Conflicto en la tarea con id '"+t1.idTarea +"'\n")
                        sys.exit()

                    b = False   # booleano para verificar que el objeto que deseamos hacerle pick este en la posicion del mundo
                    
                    for x in t1.mundo[willyIndexToMatrix(totalRow,row)][col-1]:
                        if isinstance(x, objecto) and x.id == identificador:
                            b = True
                    
                    # Si el objeto no se encuentra en la posicion. Error de ejecucion
                    if b == False:
                        print("Error de ejecucion: El objeto con que desea agarrar con id '"+identificador+"' no se encuentra en la posicion donde se encuentra willy. \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                        sys.exit()

                    # Ahora sacamos el objeto de la posicion
                    if len(t1.mundo[willyIndexToMatrix(totalRow,row)][col-1]) == 1:
                        for x in t1.mundo[willyIndexToMatrix(totalRow,row)][col-1]:
                            # Si hay solo un objeto con una cantidad al recogerlo ponemos que la posicion esta vacia (0)
                            if isinstance(x, objecto) and x.id == identificador:
                                if x.quantity == 1:
                                    t1.mundo[willyIndexToMatrix(totalRow,row)][col-1] = 0
                                    break

                                # Si hay solo un objeto con una cantidad mayor a 1 al recogerlo dejamos la lista igual pero le reducimos la cantidad al objeto                           
                                elif x.quantity > 1:
                                    cantidad = copy.deepcopy(x.quantity - 1)
                                    x.quantity = cantidad
                                    break
                            else:
                                pass

                    # En el caso de que sea una lista con multiples objetos
                    elif len(t1.mundo[willyIndexToMatrix(totalRow,row)][col-1]) > 1:
                        # Llevamos un contador con las posiciones de la lista interna
                        pos = 0
                        for x in t1.mundo[willyIndexToMatrix(totalRow,row)][col-1]:
                            # Si hay solo un objeto con uno de cantidad al recogerlo ponemos que la posicion esta vacia (0)
                            if isinstance(x, objecto) and x.id == identificador:
                                if x.quantity == 1:
                                    t1.mundo[willyIndexToMatrix(totalRow,row)][col-1].pop(pos)
                                    break
                                # Si el objeto tiene mas de una cantidad                         
                                elif x.quantity > 1:
                                    cantidad = copy.deepcopy(x.quantity - 1)
                                    x.quantity = cantidad
                                    break
                            pos = pos + 1
                    
                    # ponemos el elemento en la cesta
                    check = False # El objeto esta dentro de la cesta entonces check tiene el valor True
                    for x in t1.cesta:
                        # Si el objeto esta dentro de la cesta, actualizamos la cantidad
                        if isinstance(x, objecto) and x.id == identificador:
                            cantidad = copy.deepcopy(x.quantity + 1)
                            x.quantity = cantidad
                            #x.quantity = x.quantity + 1
                            check = True
                            break
                    
                    # Si el elemento no se encontraba en la cesta, lo agregamos
                    if check == False:
                        o1 = copy.deepcopy(t1.objects[identificador])
                        o1.quantity = 1
                        t1.cesta.append(o1)
                
                tx = self.tareas[t.idTarea]
                tCopy = copy.deepcopy(self.tareas[t.idTarea])
                tz = copy.deepcopy(tx.mundo)
                filW = copy.deepcopy(tx.position[1])
                colW = copy.deepcopy(tx.position[0])
                out = interfaceOutput(instruction= "pick", world=tz, fil = filW, col = colW, objName= identificador)
                self.impresion.append(out)
                tx.inst = "pick"
                tx.item = identificador
                if (t1.idTarea == self.tarea):
                    if (self.flag == 'manual'): # Impresion Manual
                        ## hacer input para cada tarea
                        # impresion intrucciones
                        myInput = input("presione enter para continuar")
                        print(tx.inst, tx.item, tx.valor)
                        willyWorld = copy.deepcopy(tCopy.mundo)
                        willyPosition = copy.deepcopy(tCopy.position)
                        self.printMatrizWilly(willyWorld, willyPosition)

                    elif (self.flag == 'auto'): # impresion automatica
                        if (self.segundos != None): # se tienen segundos
                        # impresion intruccione
                            sleep(self.segundos) # entre cada paso
                            print(tx.inst, tx.item, tx.valor)
                            willyWorld = copy.deepcopy(tCopy.mundo)
                            willyPosition = copy.deepcopy(tCopy.position)
                            self.printMatrizWilly(willyWorld, willyPosition)

            elif node.leaf[0] == "drop":
                # Si no existe el objeto con el id dado. ERROR DE EJECUCION
                if identificador not in t1.objects:
                    print("Error de ejecucion: No se le puede aplicar la instruccion drop al id '"+identificador+" dado a que no es un objeto \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()
                
                # Si la cesta esta vacia ERROR DE EJECUCION
                if len(t1.cesta) == 0:
                    print("Error de ejecucion: No se le puede aplicar la instruccion drop al id '"+identificador+" ya que la cesta se encuentra vacia \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()
                
                # Si el objeto no se encuentra en la lista, error de ejecucion
                # Si la cesta tiene objetos, buscamos el del id y disminuimos la cantidad
                b1 = False
                index = 0
                for x in t1.cesta:
                    if isinstance(x, objecto) and x.id == identificador:
                        b1 = True
                        if x.quantity == 1:
                            t1.cesta.pop(index)
                            break

                        elif x.quantity > 1:
                            cantidad = copy.deepcopy(x.quantity - 1)
                            x.quantity = cantidad
                            break
                    index = index + 1
                
                # Si el objeto no se encuentra en la cesta. ERROR DE EJECUCION
                if b1 == False:
                    print("Error de ejecucion: No se le puede aplicar la instruccion drop al id '"+identificador+" ya que no se encuentra en la cesta \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()

                # dejamos el objeto en la posicion actual de willy
                # Si la posicion es 0 (originalmente vacia)
                if t1.mundo[willyIndexToMatrix(totalRow,row)][col-1] == 0:
                    o1 = copy.deepcopy(t1.objects[identificador])
                    o1.quantity = 1
                    t1.mundo[willyIndexToMatrix(totalRow,row)][col-1] = [o1]

                    # si es una lista y el objeto esta y no esta
                elif isinstance(t1.mundo[willyIndexToMatrix(totalRow,row)][col-1],list):
                    b2 = False # Permite saber si en la posicion de mundo se encuentra un objeto de ese tipo
                    for x in t1.mundo[willyIndexToMatrix(totalRow,row)][col-1]:
                        if isinstance(x, objecto) and x.id == identificador:
                            cantidad = copy.deepcopy(x.quantity + 1)
                            x.quantity = cantidad
                            #x.quantity = x.quantity + 1
                            b2 = True
                            break

                    # si el objeto no se encuentra en la posicion actual del mundo
                    if b2 == False:
                        o1 = copy.deepcopy(t1.objects[identificador])
                        o1.quantity = 1
                        t1.mundo[willyIndexToMatrix(totalRow,row)][col-1].append(o1)

                tx = self.tareas[t.idTarea]
                tCopy = copy.deepcopy(self.tareas[t.idTarea])
                tz = copy.deepcopy(tx.mundo)
                filW = copy.deepcopy(tx.position[1])
                colW = copy.deepcopy(tx.position[0])
                out = interfaceOutput(instruction= "drop", world=tz, fil = filW, col = colW, objName= identificador)
                self.impresion.append(out)
                tx.inst = "drop"
                tx.item = identificador
                if (t1.idTarea == self.tarea):
                    if (self.flag == 'manual'): # Impresion Manual
                        ## hacer input para cada tarea
                        # impresion intrucciones
                        myInput = input("presione enter para continuar")
                        print(tx.inst, tx.item, tx.valor)
                        willyWorld = copy.deepcopy(tCopy.mundo)
                        willyPosition = copy.deepcopy(tCopy.position)
                        self.printMatrizWilly(willyWorld, willyPosition)

                    elif (self.flag == 'auto'): # impresion automatica
                        if (self.segundos != None): # se tienen segundos
                        # impresion intruccione
                            sleep(self.segundos) # entre cada paso
                            print(tx.inst, tx.item, tx.valor)
                            willyWorld = copy.deepcopy(tCopy.mundo)
                            willyPosition = copy.deepcopy(tCopy.position)
                            self.printMatrizWilly(willyWorld, willyPosition)

            elif node.leaf[0] == "set":
                if identificador not in t1.booleans:
                    print("Error de ejecucion: No se le puede aplicar la instruccion set al id '"+identificador+" dado a que no es de tipo booleano \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()
                b = t1.booleans[identificador]
                b.valor = True

                # guardamos el booleano con su valor actualizado
                t1.booleans[identificador] = b
                
                tx = self.tareas[t.idTarea]
                tx.inst = "set"
                tx.item = identificador

            elif node.leaf[0] == "clear":
                if identificador not in t1.booleans:
                    print("Error de ejecucion: No se le puede aplicar la instruccion clear al id '"+identificador+" dado a que no es de tipo booleano \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()
                
                b = t1.booleans[identificador]
                b.valor = False
                # guardamos el booleano con su valor actualizado
                t1.booleans[identificador] = b

                tx = self.tareas[t.idTarea]
                tx.inst = "clear"
                tx.item = identificador

            elif node.leaf[0] == "flip":

                if identificador not in t1.booleans:
                    print("Error de ejecucion: No se le puede aplicar la instruccion flip al id '"+identificador+" dado a que no es de tipo booleano \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()
                b = t1.booleans[identificador]
                b.valor = not(b.valor)
                # guardamos el booleano con su valor actualizado
                t1.booleans[identificador] = b

                tx = self.tareas[t.idTarea]
                tx.inst = "flip"
                tx.item = identificador
                tx.valor = str(b.valor)
        
            # Caso de la instruccion set id to valor
        elif len(node.children) == 2 and len(node.leaf) == 2:
            identificador = str(node.children[0].value)
            v = str(node.children[1].value)
            b = t1.booleans[identificador]
            if node.leaf[0] == "set":
                #verificamos que el booleano se encuentre definido
                if identificador not in t1.booleans:
                    print("Error de ejecucion: No se le puede aplicar la instruccion set al id '"+identificador+" dado a que no es de tipo booleano \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()

                if v == "true":
                    b.valor = True
                elif v == "false":
                    b.valor = False

            t1.booleans[identificador] = b

            tx = self.tareas[t.idTarea]
            tx.inst = "set-id-toValor"
            tx.item = identificador
            tx.valor = str(b.valor)

        # GUARDAR EN LA TABLA DE HASH DE LAS TAREAS  
        self.tareas[t1.idTarea] = t1

    def e_test(self, node, t, block_id, parent_id = None):
        t1 = self.tareas[t.idTarea]
        row = int(t1.position[1])
        col = int(t1.position[0])
        totalCol = int(t1.size[0])
        totalRow = int(t1.size[1])
        child = node.children

        # Caso carrying/found
        if node.type == "test-fc":
            
            identificador = str(node.children[0].value)

            if node.leaf[0] == "carrying":

                if identificador not in t1.objects:
                    print("Error de ejecucion: A la condicion carrying se le paso el identificador '"+identificador+"' el cual no es un objeto existente. \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()
                
                # Devuelve True si el objeto se encuentra en la cesta. 
                # Devuelve False en caso contrario
                b1 = False
                for x in t1.cesta:
                    if  isinstance(x, objecto) and x.id == identificador:
                        b1 = True
                        return True
                    else:
                        pass
                return False
                

            elif node.leaf[0] == "found":

                if identificador not in t1.objects:
                    print("Error de ejecucion: A la condicion found se le paso el identificador '"+identificador+"' el cual no es un objeto existente. \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()

                # Si la posicion tiene un cero (vacio) | devuelve false ya que no se encuentra el objeto en la posicion
                if t1.mundo[willyIndexToMatrix(totalRow,row)][col-1] == 0:
                    return False

                # Si la posicion es una lista de objetos
                b1 = False
                if isinstance(t1.mundo[willyIndexToMatrix(totalRow,row)][col-1], list):
                    for x in t1.mundo[willyIndexToMatrix(totalRow,row)][col-1]:
                        if isinstance(x, objecto) and x.id == identificador:
                            b1 = True
                            return True
                        else:
                            pass
                    return False


        #Caso parentesis
        elif node.type == "test-paren":
            valor = self.e_test(node.children[0], t ,block_id)
            return valor
        
        # Caso and/or
        elif node.type == "test-binOp":
            if node.leaf[0] == "and" :
                leftOp = self.e_test(node.children[0], t ,block_id)
                rightOp = self.e_test(node.children[1], t ,block_id)
                return (leftOp and rightOp)

            elif node.leaf[0] == "or":
                leftOp = self.e_test(node.children[0], t ,block_id)
                rightOp = self.e_test(node.children[1], t ,block_id)
                return (leftOp or rightOp)
        
        # Caso de aplicar la negacion
        elif node.type == "test-not":
            print(node.children[0].type)
            negation = not self.e_test(node.children[0], t, block_id)
            return negation 
        
        # Caso de obtener un literal
        elif node.type == "test-lit":
            return self.e_test(child[0], t, block_id)

        
        elif node.type == "literal":
            literal = str(node.value)
            lookAt = str(t1.lookingWillyAt)

            if literal == "false":
                return False
            
            elif literal == "true":
                return True
            
            elif literal == "front-clear":
                # Traer valores para hacer la verificacion
                # CASO 1: Revisar si la posicion esta fuera de la matriz (Retorna False)
                # Caso 2: Revisar si la posicion es un muro (Retorna False)
                # Caso 3: El resto de los casos devuelve true (posicion 0 o que sea una lista)
                
                if lookAt == "north":

                    if row + 1 > totalRow:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row+1)][col-1] == "wall":
                        return False
                    else:
                        # Si es una lista o un 0
                        return True
                    
                elif lookAt == "south":

                    if row - 1 < 1:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row-1)][col-1] == "wall":
                        return False
                    else:
                        return True

                elif lookAt == "east":
                    
                    if col + 1 > totalCol:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col] == "wall":
                        return False
                    else:
                        return True

                elif lookAt == "west":
                    
                    if col - 1 < 1:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col-2] == "wall":
                        return False
                    else:
                        return True
            
            
            elif literal == "left-clear":

                if lookAt == "north":
                    
                    if col - 1 < 1:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col-2] == "wall":
                        return False
                    else:
                        return True
                    
                elif lookAt == "south":

                    if col + 1 > totalCol:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col] == "wall":
                        return False
                    else:
                        return True

                elif lookAt == "east":
                    
                    if row + 1 > totalRow:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row + 1)][col-1] == "wall":
                        return False
                    else:
                        return True

                elif lookAt == "west":
                    
                    if row - 1 < 1:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row - 1)][col-1] == "wall":
                        return False
                    else:
                        return True

            elif literal == "right-clear":

                if lookAt == "north":
                    
                    if col + 1  >  totalCol:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col] == "wall":
                        return False
                    else:
                        return True
                    
                elif lookAt == "south":

                    if col - 1 < 1:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row)][col-2] == "wall":
                        return False
                    else:
                        return True

                elif lookAt == "east":
                    
                    if row - 1 < 1:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row - 1)][col-1] == "wall":
                        return False
                    else:
                        return True

                elif lookAt == "west":
                    
                    if row + 1 > totalRow:
                        return False
                    elif t1.mundo[willyIndexToMatrix(totalRow,row + 1)][col-1] == "wall":
                        return False
                    else:
                        return True

            elif literal == "looking-north":
                
                if lookAt == "north" :
                    return True
                elif lookAt != "north":
                    return False

            elif literal == "looking-east":
                
                if lookAt == "east" :
                    return True
                elif lookAt != "east":
                    return False

            elif literal == "looking-south":

                if lookAt == "south" :
                    return True
                elif lookAt != "south":
                    return False
            
            elif literal == "looking-west":

                if lookAt == "west" :
                    return True
                elif lookAt != "west":
                    return False

            else:
                # si el literal no es un booleano. Error de ejecucion
                if literal not in t1.booleans:
                    print("Error de ejecucion: A la condicion Test se le paso el identificador '"+literal+"' el cual no es un objeto existente. \n Conflicto en la tarea '"+ t1.idTarea +"' \n")
                    sys.exit()
                
                # Si es de tipo booleano, lo retornamos
                b = t1.booleans[literal]
                return b.valor

    def e_ifInst(self, node, t, block_id, parent_id = None):
        child = node.children
        if len(child) == 2:
            test = self.e_test(child[0], t, block_id)
            if test:
                self.e_taskInst(child[1], t, block_id)
        
        elif len(child) == 3:
            test = self.e_test(child[0], t, block_id)
            if test:
                self.e_taskInst(child[1], t, block_id)
            else:
                self.e_taskInst(child[2], t, block_id)

    
    def e_repeatInst(self, node, t, block_id, parent_id = None):
        child = node.children
        nTimes = int(child[0].value)

        for x in range(0,nTimes):
            #print(x)
            self.e_taskInst(child[1], t, block_id)

    def e_whileInst(self, node, t, block_id, parent_id = None):
        child = node.children

        while(True):
            test = self.e_test(child[0], t, block_id)
            
            if test == True:
                self.e_taskInst(child[1], t, block_id)
            
            elif test == False:
                break


    def e_defineInst(self, node, t, block_id, parent_id = None):
        t1 = self.tareas[t.idTarea]
        identificador = str(node.children[0].value)
        child = node.children
        nieto = node.children[1].children[0] # Accedemos al nieto para poder ver la siguiente instruccion (nos saltamos taskInst)

        # Verificamos que el id no este en el marco actual

        # Verificar tambien que el identificador no se de tipo objeto, booleano o goal (willy* no acepta sobre)
        
        if identificador in self.blocks[len(self.blocks)-1].variables:
            print("Error: Ya se encuentra otro elemento con el id '"+ identificador +"' en el marco actual"+"\n"+ "(Conflicto en la instruccion Define en la tarea '"+ t.idTarea +"' \n")
            sys.exit()

        if identificador in t1.booleans:
            print("Error: Ya se encuentra otro elemento con el id '"+ identificador +"' y es de tipo boolean en la tarea '"+ t.idTarea +"' \n")
            sys.exit()

        if identificador in t1.goals:
            print("Error: Ya se encuentra otro elemento con el id '"+ identificador +"' y es de tipo goal en la tarea '"+ t.idTarea +"' \n")
            sys.exit()

        if identificador in t1.objects:
            print("Error: Ya se encuentra otro elemento con el id '"+ identificador +"' y es de tipo objeto en la tarea '"+ t.idTarea +"' \n")
            sys.exit()
        
        # NO SE PUEDE DEFINIR CON UN ID ALGO DE TIPO INSTRUCCION PRIMITIVA (ERROR) (Enunciado general del proyecto)
        if nieto.type == "primitiveInst":
            print("Error: No se puede definir el id '"+ identificador +"' con una instruccion primitiva del lenguaje. " +" \n"+ " Conflicto en la tarea '"+ t.idTarea +"' \n")
            sys.exit()
        
        # Caso 1: Error si se utiliza el id de  un objeto, goal o booleano
        # En caso de ser un terminal de tipo identificador, se busca a ver si contiene una funcion 
        # Si existe la definicion, verificamos que sea una funcion y procedemos a ejecutarla, si comienza por un begin creamos un nuevo marco de pila
        # En caso contrario no creamos nuevo marco de pila
        if nieto.type == "terminal":
            func = nieto.value
            #print("FUNC "+func)

            if func in t1.objects:
                print("Error: No se puede aplicar un define a algo que no es de tipo instruccion, el tipo encontrado es objeto \n" +"Task '"+ t.idTarea +"'\n"+ "Objeto: " + identificador +"\n")
                sys.exit()

            if func in t1.booleans:
                print("Error: No se puede aplicar un define a algo que no es de tipo instruccion, el tipo encontrado es booleano \n" +"Task '"+ t.idTarea +"'\n"+ "Booleano: " + identificador +"\n")
                sys.exit()

            if func in t1.goals:
                print("Error: No se puede aplicar un define a algo que no es de tipo instruccion, el tipo encontrado es goal \n" +"Task '"+ t.idTarea +"'\n"+ "Goal: " + identificador +"\n")
                sys.exit()

            # Se busca el subarbol asociado en el marco actual, si no se encuentra en el marco actual buscamos en los anteriores
            initScope = t.scopeStart
            #Contamos la cantidad de elementos entre el primero del scope y el ultimo index de scope(marco actual) y procedemos a recorrerlo bajo esa indexacion en orden inverso (downto)
            # Verificado hasta encontrar la variable que buscamos en alguno de los marcos.
            # Si la variable no se encuentra en alguno de los marcos ERROR

            #Volteamos la lista
            self.blocks.reverse()
            b = False

            # Se busca la variable definida desde el marco mas interno al mas externo
            for x in self.blocks:
                if func in x.variables:

                    var = x.variables[func]
                    #Vemos si es una funcion
                    if isinstance(var,define):
                        # Nos permite saber que fue conseguida una funcion en algun marco de pila
                        b = True
                        var.id = identificador
                        x.insert_variable(identificador,var)
                    
                    break
                
                # Si llegamos al marco de pila inicial y todavia no se ha conseguido el id
                if x.id == initScope:
                    break
            #print(b)
            if b == False:
                print("Error de ejecucion: El identificador '" +identificador+ "'no ha sido definido en ningun marco, por lo que no pudo ser encontrado. \n Conflicto en la tarea '"+t.idTarea+"' \n")
                sys.exit()

            # La dejamos como se encontraba originalmente
            self.blocks.reverse()

            # Caso 2:  Si el nieto es otra instruccion de tipo define (guardo ambos ids con el mismo sub-arbol)
        elif nieto.type == "defineInst":
            idInterno = str(nieto.children[0].value)
            instInterna = nieto.children[1]
            hijoInstInterna = instInterna.children[0] #nuevo nieto
            b5 = False
            # Buscamos el arbol ligado al define mas interno y se lo asignamos al mas externo (si hay mas de dos define) (si el nieto del nieto es un define)
            # Cargamos de la tabla de hash el valor del mas interno para asignarselo al mas externo
            if hijoInstInterna.type == "defineInst":
                self.e_defineInst(nieto, t, block_id)
                defin = self.blocks[len(self.blocks)-1].variables[str(hijoInstInterna.children[0].value)]
                defineTree = define(idInterno,defin.tree)
                self.blocks[len(self.blocks)-1].insert_variable(identificador, defineTree)
                

            # Si el nieto del nieto no es un define asignamos child[1] al idInterno y al identificador
            elif hijoInstInterna.type != "defineInst" and hijoInstInterna.type != "terminal":
                defineTree1 = define(idInterno, hijoInstInterna)
                self.blocks[len(self.blocks)-1].insert_variable(identificador, defineTree1)
                self.blocks[len(self.blocks)-1].insert_variable(idInterno, defineTree1)

            elif hijoInstInterna.type != "defineInst" and hijoInstInterna.type == "terminal":
                defineTree1 = define(idInterno, hijoInstInterna)
                b22 = 0
                b11 = False
                for x in range(len(self.blocks)-1,-1,-1):
                    if str(hijoInstInterna.value) in self.blocks[x].variables:
                        b22 = x
                        b11 = True
                        break
                    #print(x)
                if b11 == True:
                    defin = self.blocks[b22].variables[str(hijoInstInterna.value)]
                    self.blocks[len(self.blocks)-1].insert_variable(identificador, defin)
                    self.blocks[len(self.blocks)-1].insert_variable(idInterno, defin)
                elif b11 == False:
                    print("Error de Ejecucion: No ha sido definida la funcion "+str(hijoInstInterna.value)+ " en ningun parte del codigo \n")
                    sys.exit()


        # Caso 3  si su nieto es un begin o cualquier otro tipo de instruccion, se guarda el subarbol formado en el marco actual de la pila dentro de un objeto de tipo define
        if nieto.type != "primitiveInst" and nieto.type != "defineInst" and nieto.type != "terminal":
            defineTree = define(identificador, nieto)
            self.blocks[len(self.blocks)-1].insert_variable(identificador,defineTree)
    
    def e_beginInst(self, node, t, block_id, parent_id = None):
        child = node.children[0]
        self.e_taskSeq(child, t, block_id)

def semantic(tarea, flag, segundos):
    return Semantic(tarea, flag, segundos)
        