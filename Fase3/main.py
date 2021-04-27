import sys
import ply.lex as lex
import lexer
import parser
import logging
import semantic

def main(argv):
    if (len(argv) >= 1):
        try:
            f = open(argv[0], 'r')
        except FileExistsError as e:
            print('Ha ocurrido un error al abrir el archivo:', e)
            sys.exit()
        data = f.read()
        f.close()

        # tarea
        tarea = argv[1]

        # flags
        if (argv[2] == '-a' or argv[2] == '--auto'):
            flag = 'auto'
            if (len(argv) == 4):
                segundos = argv[3]
                # manejo formato segundos
                print(segundos.isdigit())
                if (segundos.isdigit()):
                    segundos = int(segundos)
                else:
                    segundos = None
                    print('Los segundos deben ser numeros')
                    sys.exit()
            else:
                segundos = None
            # print(flag)


        elif (argv[2] == '-m' or argv[2] == '--manual'):
            flag = 'manual'
            if (len(argv) == 4):
                print('Error con operacion manual no es necesario segundos')
                sys.exit()
            else:
                segundos = None

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

        mySemantic = semantic.semantic(tarea, flag, segundos)
        mySemantic.execute(result_tree)
        
        #print_node_recursive(result_tree)
    else:
        print('Faltan argumentos')

if __name__ == "__main__":
    main(sys.argv[1:])
