import sys
import ply.lex as lex
import lexer
import parser
import logging


# Funcion que recorre el arbol y lo imprime. 
def printTree(nodo, tabs):
    print('\t'*tabs + str(nodo))
    if not (isinstance(nodo, Node)):
        return
    for i in range(len(nodo.child)):
            if nodo.child[i] != None:
                printTree(nodo.child[i], tabs+1)

def print_node_recursive(node, depth=None):
	spaces = ''
	if depth:
		for i in range(0, depth):
			if (i + 1) % 4 == 0:
				spaces = spaces + '|'
			else:
				spaces = spaces + ' '
	else:
		depth = 0

	if (node.tag and node.value):  
		if node.tag == "bool":
			print(spaces + node.tag + ': "' + node.value + '"')
		else:
			print(spaces + node.tag + ':', node.value)
	else:
		print(spaces + node.type)

	if node.children:
		for child in node.children:
			print_node_recursive(child, depth + 1)

if (len(sys.argv) == 2):
    try:
        f = open(sys.argv[1], 'r')
    except FileExistsError as e:
        print('Ha ocurrido un error al abrir el archivo:', e)
        sys.exit()
    data = f.read()
    f.close()

    # Build lexer
    myLexer = lexer.lexer()

    program_tokens, errors = lexer.tokenize(myLexer, data)

    if len(errors) > 0:
        for err in errors:
            print(err)
        sys.exit()

    # Build parser
    log = logging.getLogger()
    myParser = parser.parser()
    result_tree = myParser.parse(data, lex, debug=log)
    print_node_recursive(result_tree)


