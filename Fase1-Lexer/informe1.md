
#### Universidad Simón Bolívar
#### Departamento de Computación y Tecnología de la Información
#### Enero – Marzo 2020
#### Profesor: Blai Bonet  

<br />
<p align="center">

  <h2 align="center">Proyecto Traductores e Interpretadores: Willy*</h2>

  <p align="center">
	El proyecto consiste en implementar el ambiente de programación Willy*. <br>
	Willy* está inspirado en el ambiente/lenguaje Willy definido por el Prof. Ernesto Hernandez-Novich. 
  </p>
</p>


## Tabla de Contenidos

* [Acerca del Proyecto](#acerca-del-proyecto)
  * [Implementado Con](#implementado-con)
  * [Implementacion](#implementacion)
* [Comenzando](#comenzando)
  * [Prerequisitos](#prerequisitos)
  * [Instalacion](#instalacion)
* [Como se Usa](#como-se-usa)
* [Contacto](#contacto)


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

Esta Primera etapa consiste en un lexer, que con la ayuda de la libreria PLY <br>
Se encarga de leer el string y devolver los tokens asociados o error en caso de conseguir uno <br>
Para la implementación primero se definieron los tokens a ser reconocidos mediante el uso de  expresiones regulares, funciones y una lista de palabras reservadas. <br>
<br>
Luego de obtener los tokens, se hizo el recorrido sobre la lista y procedió a su impresión <br>
Adicionalmente se hizo un makefile para correr los programas como se describe más adelante <br>


## Comenzando

  Sigue los pasos

### Prerequisitos

Python 3 debe estar instalado. <br>
Ply está provisto en la carpeta. <br>
Hay que otorgar permisos de ejecución con el comando chmod 777 al archivo willy <br>
donde se encuentra el script que permite analizar el programa


### Instalacion
 
Nada más es necesario para su ejecución


<!-- USAGE EXAMPLES -->
## Como se Usa

Escriba su programa con palabras que pertenezcan al lenguaje. <br>
Ejecute el siguiente comando dentro de la carpeta donde tenga la librería de ply, lexer.py, su programa a
reconocer por el lexer y el archivo willy

```sh
./willy file.txt
```

En caso de no proveer un archivo, se pedirá por consola.

Si prefiere ejecutar los comandos por separado sería de la siguiente forma.

```sh
python3 lexer.py yourProgram.txt
```