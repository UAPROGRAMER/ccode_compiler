from tokener import *
import os

class Translator:
    def __init__(self, tokens:list) -> None:
        self.pos:int = -1
        self.tokens:list = tokens
        self.curtoken:Token|None = None
        self.next()
        self.data = 'section .data\n'
        self.bss = 'section .bss\n'
        self.text = 'section .text\nglobal _start'
        self.includes = ''
        self.start = '_start:\n'
        self.curconstnum:int = 1
        self.curscope = {
            "func":[],
            "const":[],
            "var":[],
        }

    def next(self):
        if len(self.tokens) > self.pos+1:
            self.pos += 1
            self.curtoken = self.tokens[self.pos]
        else:
            self.curtoken = None

    def translateAll(self) -> str:
        while self.curtoken != None:
            self.translateToken()
            self.next()
        return self.groupUp()

    def groupUp(self) -> str:
        ret = f"\n;compiler by UAPROGRAMER.\n{self.includes}\n{self.data}\n{self.bss}\n{self.text}\n{self.start}\n"
        return ret
    
    def translateToken(self):
        include = ''
        if self.curtoken.type == TT_STRING:
            self.translateString()
            return
        if self.curtoken.type == TT_INT:
            self.start += f"mov rax, {self.curtoken.value}\npush rax\n"
            return
        if self.curtoken.type == TT_LABEL:
            if self.curtoken.value == "#include":
                self.include()
                return
            
            if self.tokens[self.pos+1].type == TT_PARENL:
                self.translateFunccall()
                return
        if self.curtoken.type == TT_NLINE:
            return
        raise ValueError("Translator: bad token or conbination of tokens.")
    
    def expectNLINE(self):
        self.next()
        if self.curtoken == None or self.curtoken.type == TT_NLINE:
            return
        else:
            raise ValueError("Translator: unexpected token after command.")
    
    def include(self):
        self.next()
        if self.curtoken.type != TT_STRING:
            raise ValueError("Translator: bad #include.")
        
        if not os.path.isfile(self.curtoken.value):
            raise ValueError("Translator: #include file unreacheble or does not exists.")
        
        with open(self.curtoken.value, 'r') as ofile:
            include:str = ofile.read()

        rules:str = include.partition('\n')[0]
        rulesarray:list = rules.split()

        for i in range(len(rulesarray)):
            if rulesarray[i] == ';':
                continue

            if rulesarray[i] == 'func':
                self.curscope["func"].append((rulesarray[i+1], int(rulesarray[i+2])))
                continue
            if rulesarray[i] == 'const':
                self.curscope["const"].append(rulesarray[i+1])
                continue

        include += '\n'
        include = '\n'+include
        self.includes += include
        self.expectNLINE()
        return

    def translateFunccall(self):
        name = self.curtoken.value
        declared = False
        argc = 0
        for func in self.curscope["func"]:
            if func[0] == name:
                declared = True
                argc = func[1]
                break
        if not declared:
            raise ValueError("Translator: function not declared.")
        self.next()
        self.next()
        count = 0
        while self.curtoken.type != TT_PARENR:
            self.translateToken()
            count += 1
            self.next()
        if count != argc:
            raise ValueError(f"Translator: function have bad arguments, expected {argc} while resived exactly {count}.")
        self.start += f'call {name}\n'
        self.expectNLINE()

    def translateString(self):
        strarray = []
        j = 0
        prevchar = ''
        for char in self.curtoken.value:
            if char == '\n' or prevchar == '\n':
                j+=1
            if len(strarray) > j:
                strarray[j] += char
            else: 
                strarray.append(char)
            prevchar = char

        for i in range(len(strarray)):
            if strarray[i] == '\n':
                strarray[i] = 10
        data = '__constValue'+str(self.curconstnum)+'__ db '
        name = '__constValue'+str(self.curconstnum)+'__'
        for i in strarray:
            if type(i) is int:
                data += f"{i}, "
                continue
            data += f'"{i}", '
        data += '0\n'
        self.curconstnum += 1
        self.data += data
        self.start += f"mov rax, {name}\npush rax\n"
