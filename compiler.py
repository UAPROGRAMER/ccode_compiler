import sys
import os
from tokener import *
from translator import *

ARGC:int = len(sys.argv)
ARGV:list[str] = sys.argv

if ARGC > 1 and os.path.isfile(ARGV[1]):
    path:str = ARGV[1]
else:
    raise ValueError("File not specified or doesn't exists.")

file = open(path, 'r')
text = file.read()
file.close()

lexer = Lexer(text)
tokens = lexer.lexe()

print(tokens)

translator = Translator(tokens)
assembley = translator.translateAll()

exitfilename = ARGV[1].split('.')[0]+'.asm'

exitfile = open(exitfilename, 'w')
exitfile.write(assembley)
exitfile.close()
