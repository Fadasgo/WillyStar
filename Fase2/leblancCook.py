#FALTA HACER METODO DE IMPRESION DE LA TABLA DE HASH
class entry:
    def __init__(self, nombreID,blockID,tipo,mundoId,tareaId):
        self.nombreID = nombreID
        self.blockID = blockID
        self.tipo = tipo
        self.mundoId = mundoId
        self.tareaId = tareaId

    

class leblancCook:
    def __init__(self):
        self.dict = {}
        self.stack = []

    
    def find(self,id):
        x = self.dict[id]
        return x

    #revisa si el id se encuentra ya dentro de la tabla de hash
    # Devuelve False si no se puede agregar debido a que ya existe
    # Devuelve True en caso de agregarlo de manera satisfactoria
    # ver cuando crecer la pila
    def insert(self,id,entries):
        if id in self.dict:
            #verificamos que no esten en el mismo scope
            x = self.dict[id]
            for elem in x:
                if entries.blockID == elem.blockID:
                    msg = "No puede haber renombramiento de variable dentro del mismo scope. "+"\n"
                    self.error(id,msg)
            #si no estan en el mismo scope que alguno de los de la lista con el mismo id
            x.insert(0,entries)
            d1 = {id:x}
            self.dict.update(d1)
            return True
        else:
            if isinstance(entries, entry):
                d1 = {id:[entries]}
                self.dict.update(d1)
                return True
        
        # Si se consigue un nuevo marco de pila
    def push(self,blockID):
        self.stack.append(blockID)
    
    def pop(self):
        self.stack.pop()
    
    def isEmpty(self):
        if (len(self.stack) == 0):
            return True
        else:
            return False
    
    def error(self,id,msg):
        print("Error: "+ msg +  " Problema con el ID : '" + str(id) + "'\n")
        raise SystemExit

#Pruebas de los metodos

symbolTable = leblancCook()
print(symbolTable.isEmpty())
entrada = entry("mundo1",0,"bool","mundo1","t1") 
entrada1 = entry("mundo1",1,"bool","mundo1","t1") 
entrada2 = entry("mundo1",1,"bool","mundo1","t1") 
symbolTable.insert("mundo1",entrada)
symbolTable.insert("mundo1",entrada1)
#symbolTable.insert("mundo1",entrada2)
print(symbolTable.dict)
l = symbolTable.find("mundo1")
#l = symbolTable.dict["mundo1"]
print("Tamanio de la lista "+ str(len(l)) + "\n")
'''d = {}
d1 = {"a":"1"}
d2 = {"a":"2"}
d.update(d1)
d.update(d2)
print(d)'''