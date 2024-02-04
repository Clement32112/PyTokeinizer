class fileManger:
    def get_text(filePath):
        file = open(filePath)
        return (file.read()) 

class token:
    value:str
    def __init__(self,value:str):
        self.value = value
    def print(self):
        print(self.value,end=",")

class Tokenizer:
    tokenBreakers = ['\n',' ','\t',';']
    def __init__(self):
        pass
    def tokenize(self,text:str) -> list[token]:
        text += '\n'
        TokenStream:list[token] = []
        strInput = ""
        for i in text:
            if i in self.tokenBreakers:
                if len(strInput) == 0:
                    continue
                TokenStream.append(token(strInput)) 
                print("Token: "+strInput)
                strInput = ""
                continue
            strInput += i
        return TokenStream

myTokenizer = Tokenizer()
text:str = fileManger.get_text("hello.txt")

for i in myTokenizer.tokenize(text):
    i.print()