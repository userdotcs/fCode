import Interpreter.interpreter


while True:
    inp = input()
    if inp.endswith('.fcode'):
        source = open(inp)
        source_code = []
        for i in source.readlines():
            source_code.append(i.rstrip('\n'))
        source.close()
        def_interpreter = Interpreter.interpreter.Interpreter(source_code)
        def_interpreter.run()
        exit()
    else:
        print('Write \'.fcode\' file.')
