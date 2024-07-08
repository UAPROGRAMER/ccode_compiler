import sys
import os
from tokener import *
from translator import *

ARGC:int = len(sys.argv)
ARGV:list[str] = sys.argv

file:str = ""
if ARGC > 1 and os.path.isfile(ARGV[1]):
    file:str = ARGV[1]
else:
    raise ValueError("File not specified or doesn't exists.")

lines:list[str] = []
with open(file, "r") as program:
    lines = [
        line.strip() for line in program.readlines()
    ]
for line in lines.copy():
    if line == '':
        lines.remove(line)

tokens:list[Token] = []
i = 0
for line in lines:
    i+=1
    parser = Parser(line, i)
    parsed = parser.parse()
    for token in parsed:
        tokens.append(token)

translator = Translator(tokens)
assembley = translator.translateAll()

exitfilename = ARGV[1].split('.')[0]+'.asm'

exitfile = open(exitfilename, 'w')
exitfile.write(assembley)
exitfile.close()