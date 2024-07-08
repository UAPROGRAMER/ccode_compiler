TT_LABEL = "label"
TT_STRING = "string"
TT_INT = "int"
TT_PARENL = "parenl"
TT_PARENR = "parenr"

class Token:
    def __init__(self, type_, value:any) -> None:
        self.type:int = type_
        self.value = value
    
    def __repr__(self) -> str:
        return f"{self.type}:{self.value}"

class Parser:
    def __init__(self, line:str, lineNum:int) -> None:
        self.pos:int = -1
        self.line:str = line
        self.char:str|None = ''
        self.lineNum:int = lineNum
        self.next()
    
    def next(self) -> None:
        if len(self.line) > self.pos+1:
            self.pos += 1
            self.char = self.line[self.pos]
        else:
            self.char = None
    
    def parse(self) -> list[Token]:
        tokens:list[Token] = []
        while self.char != None:
            if self.char in ' \n':
                self.next()
                continue
            if self.char in ';':
                break
            
            if self.char in '0123456789':
                tokens.append(self.getNum())
                continue
            
            if self.char in '"':
                tokens.append(self.getString())
                continue

            if self.char == '(':
                tokens.append(Token(TT_PARENL, None))
                self.next()
                continue
            if self.char == ')':
                tokens.append(Token(TT_PARENR, None))
                self.next()
                continue
            
            if self.char in "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ_.$#":
                tokens.append(self.getLabel())
                continue

            raise ValueError(f"Parser: bad char. ({self.lineNum}:{self.pos})")
        return tokens
    
    def getNum(self) -> Token:
        num = ''
        while self.char in '0123456789':
            num += self.char
            self.next()
        return Token(TT_INT, int(num))
    
    def getString(self) -> Token:
        string = ''
        self.next()
        while self.char != '"':
            if self.char == None:
                raise ValueError(f"Parser: string hasn't been closed. ({self.lineNum}:{self.pos})")
      
            if self.char == '\\':
                self.next()
                if self.char == 'n':
                    string += '\n'
                    self.next()
                    continue 
                    
            string += self.char

            self.next()
        self.next()
        return Token(TT_STRING, string)
    
    def getLabel(self) -> Token:
        label = ''
        while self.char in 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ_.$#':
            label += self.char
            self.next()
        return Token(TT_LABEL, label)