
#### CI-3725 Traductores e Interpretadores
#### Profesor: Blai Bonet  

<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h2 align="center">Interprete Willy*</h2>

  <p align="center">
	El proyecto consiste en implementar el intérprete del ambiente de programación Willy* diseñado por el Prof. Blai Bonet. <br>
	Willy* está inspirado en el ambiente/lenguaje Willy definido por el Prof. Ernesto Hernandez-Novich. 
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Tabla de Contenidos

* [Acerca del Proyecto](#acerca-del-proyecto)
  * [Implementado Con](#implementado-con)
  * [Implementacion](#implementacion)
* [Comenzando](#comenzando)
  * [Prerequisitos](#prerequisitos)
  * [Instalacion](#instalacion)
* [Como se Usa](#como-se-usa)
* [Contacto](#contacto)



<!-- Acerca del Proyecto -->
## Acerca del Proyecto

  Proyecto del Curso CI-3725 para el trimestre Enero-Marzo 2020

  Función: Interprete de Willy*

  Descripción: El ambiente consiste de un robot llamado Willy que se desenvuelve dentro de una cuadrícula
  finita en la cual existen paredes. <br>
  Willy tiene sensores, brazos actuadores, una cesta para guardar objetos, y medios para desplazarse. 
  El robot puede navegar libremente en la cuadrícula, puede recoger y dejar objetos en las celdas de la cuadrícula. <br>
  Willy es controlado por un programa que contiene una o mas definiciones del mundo, la definición de los procedimentos y el programa principal.  <br>
  Willy es controlado por un programa que contiene una o mas deniciones del mundo, y la definicion de los procedimentos y el programa principal. <br>


### Implementado Con

* [Python3](Python3)
* [Ply](Ply)

### Implementacion

#### Fase 1

Esta Primera etapa consiste en un lexer, que con la ayuda de la librería PLY <br>
Se encarga de leer el string y devolver los tokens asociados o error en caso de conseguir uno. <br>

Para la implementación primero se definieron los tokens a ser reconocidos mediante el uso de expresiones regulares, <br>
funciones y una lista de palabras reservadas. <br>


#### Fase 2

Esta Segunda etapa consiste en un parser, con el AST y su tabla de símbolos, <br>
con la ayuda de la librería PLY. <br>
<br>
Partiendo de donde termina la fase 1 (lexer) se procede en dicha segunda entrega crear las producciones <br>
que permiten satisfacer la sintaxis del lenguaje, luego de eso se procede a generar la tabla de símbolos <br>
que será importante para el análisis semántico y posteriormente la interpretación del lenguaje. <br>
<br>
La estructura implementada para la parte de la tabla de símbolos fue un diccionario para los mundos, <br>
otro para las tareas y por último una pila que donde cada nivel es un marco nuevo de inmersión <br>
dentro del programa y a su vez cada marco tiene su diccionario para la declaración de variables en ese nivel. <br>
<br>
 
#### Fase 3

Por último esta última fase consistió en corregir detalles de entregas anteriores e implementar <br>
el intérprete del lenguaje de modo que al suministrar un programa correcto de willy* se devuelve la corrida del mismo. <br>
<br>
<strong> En nuestro intérprete no aceptamos defines como instrucciones primitivas como dice <br>
en el enunciado del proyecto, </strong> adicionalmente para que la ejecución de un programa se lleve a cabo, <br>
incluso las tareas que no se suministran para la corrida del intérprete deben ser correctas <br>
hasta su nivel de ejecución, de lo contrario se presentará el error. <br>
<br>
Primero se hace la verificación léxica del programa, una vez verificada esta se hace una verificación <br>
gramática del programa, luego se revisa que este programa corra correctamente y por último se imprime <br>
por consola la corrida correspondiente a la instrucción que se indica, dependiendo del flag que se pase <br>
se tiene distintas formas de salida, consideramos necesario que se pase alguno de estos flags. <br>
<br>
En caso de ser el flag automático se puede pasar un parámetro numérico que corresponde <br>
al intervalo de segundos que transcurre entre cada paso de la ejecución, si se pasa segundos <br>
en tipo de ejecución manual se considera un error, en caso de no pasar segundos en tipo automático, <br>
se imprime el resultado final de la ejecución. <br>
Se puede simular la corrida de los mundos mediante una representación por interfaz gráfica  o terminal <br>


## Comenzando

  Sigue los pasos

### Prerequisitos

Python 3 debe estar instalado para el funcionamiento del interprete. <br>
Ply debe estar provisto en la carpeta de ejecución para el funcionamiento de la herramienta. <br>
Hay que otorgar permisos de ejecución con el comando chmod 777 a los archivos willy e interfaz <br>
donde se encuentra el script que permite analizar el programa <br>


### Instalacion
 
Nada más es necesario para su ejecución


<!-- USAGE EXAMPLES -->
## Como se Usa

Escriba su programa siguiendo las reglas del lenguaje willy*. <br>
Ejecute el siguiente comando dentro de la carpeta donde <br>
tenga la librería de ply y se procederá a ejecutar su programa <br>

```sh
./willy nombreArchivo nombreTarea flag tiempo
```
En caso de no proveer los parámetros, se pedirá por consola. <br>
Si prefiere ejecutar los comandos por separado sería de la siguiente forma. <br>

```sh
python3 main.py nombreArchivo nombreTarea flag tiempo
```
<strong> Interfaz </strong> <br>

<strong> Como adición extra al proyecto, se pudo implementar una interfaz gráfica con PyQt5 </strong> <br>
Para correr la misma no es necesario tener instalado el paquete <br>
Se agregó otra forma de correr el programa en esta se muestra la corrida por consola y <br>
luego se abre la interfaz gráfica. Para correr la versión con interfaz es de la siguiente forma. <br>

```sh
./interfaz nombreArchivo nombreTarea flag tiempo
```

Al igual que el anterior para ejecutar los comandos por separado seria. <br>

```sh
python3 willy.py nombreArchivo nombreTarea flag tiempo
```

<br>

<strong> Dentro cada casilla de la interfaz si aparece algo de la forma corneta(5) </strong> <br>
<strong> significa que hay 5 objetos de tipo corneta en dicha posición.</strong> <br>

<strong> Para poder visualizar mejor el contenido de las casillas, puede ampliar las filas y columnas acercando el mouse </strong> <br>
<strong> a los bordes de la tabla. (cualquier casilla que se vea con ... es necesario ampliarla para ver su contenido) </strong> <br>

<strong> Cabe destacar que el último flag, el del tiempo es opcional </strong>  si se va a ejecutar <br>
con el flag -m o --manual y por otro lado es opcional para la corrida del flag -a o --auto, <br>
dicho parámetro debe ser un entero y va sin corchetes. <br>
 
 <strong> Para el caso de la interfaz, si se ejecuta con el flag manual se avanza mediante el boton Next y </strong> <br>
 <strong> para el caso de ser auto el flag con n segundos se avanza automáticamente cada n segundos </strong> <br>
  
  
<strong> Nota:</strong> En el Archivo que se genera parselog.txt se puede ver el parseo del programa producción a producción <br>

### Impresion
	El formato de impresión utilizado para el mundo es el de una matriz con el siguiente formato para cada posicion:
		- Si la posición contiene "wall" es que se encuentra situada una pared en esa casilla.
		- Si la posición contiene "0" es que se encuentra vacia.
		- Si la posición contiene "willy" es que se encuentra situado solamente willy en esa casilla.
		- Si la posición contiene una X es que se encuentra situado al menos un objeto en dicha posición.
		- Si la posición contiene willy-X es que se encuentra el robot willy y al menos un objeto.
	
En general para cada vez que se imprime una instancia de la matriz del mundo, en su parte superior izquierda se imprime <br>
la instrucción que se ejecutó. Luego de eso se procede a imprimir en la parte inferior de la matriz <br>
la cantidad de objetos  que se encuentran en dicha posición y su indexación. <br>

Los objetos que se encuentran bajo la misma indexación están impresos de manera continua y luego se imprime <br>
un salto de línea, para colocar la posición del siguiente grupo de objetos.<br>

	
	##Ejemplo ilustrativo:
	
		move:
			wall	wall	wall	wall	wall	wall
			wall	0	0	0	0	0
			wall	0	0	0	0	0
			wall	0	0	0	0	0
			wall	X	X	0	willy-X	0
			wall	0	0	0	0	X

		posicion  row: 2, col: 2
		X =  {'id': 'corneta', 'color': 'blue', 'type': 'object', 'quantity': 1}

		posicion  row: 2, col: 3
		X =  {'id': 'pelota', 'color': 'red', 'type': 'object', 'quantity': 1}

		posicion  row: 2, col: 5                                                      
		X =  {'id': 'corneta', 'color': 'red', 'type': 'object', 'quantity': 1}
		X =  {'id': 'celular', 'color': 'red', 'type': 'object', 'quantity': 2}

		posicion  row: 1, col: 6
		X =  {'id': 'pelota', 'color': 'red', 'type': 'object', 'quantity': 5}


	
	cabe destacar que este formato es tanto para el modo manual como el auto


<!-- CONTACT -->
## Contacto
Implementado por:
        Luis Carlos Marval - 12-10620 - luiscarm77@gmail.com 
		Fabio Suárez - 12-10578 - fadasgo@gmail.com

