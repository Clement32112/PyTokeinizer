import re

class fileManger:
    @staticmethod
    def get_text(filePath):
        file = open(filePath)
        return (file.read()) 

class token:
    value:str
    token_type:str
 
    def __init__(self,value:str,type:str=""):
        self.value = value
        self.token_type = type
    def print(self):
        print("{",self.value,":",self.token_type,"}",end=",")
    def __str__(self) -> str:
        return self.value

class Tokenizer:
    tokenBreakers = [' ','\t',';'] #line breakers

    tokenTypes = {
        "keyword": r"\b(int|main|std|cout|endl|return)\b",
        "punctuator": r"[,{}():<>]",
        "int": r"[0-9*]",
        "operator": r"[+\-*/=%]"
    }
    
    

    def tokenize(self,text:str) -> list[token]:

        text += '\n'
        TokenStream:list[token] = []
        strInput = ""
        
        list_of_newline_delimed_tokens = text.split('\n')
        TokenStream:list[token] = []
        strInput = ""

        for i in list_of_newline_delimed_tokens:
            if i.startswith('#'):
                pass
            else:
                for value in i: #character by character not word by word
                    if value in self.tokenBreakers:
                        if len(strInput) == 0:
                            continue
                        TokenStream.append(token(strInput)) 
                        strInput = ""
                        continue
                    strInput += value
        return TokenStream
    
    def get_token_type(self, arr):
        token_arr = []
        
        for unprocessed_token in arr:
            found_value = ""
            for char_index in range(len(str(unprocessed_token))):
                found_value += str(unprocessed_token)[char_index]
                for key, value in self.tokenTypes.items():
                        if re.match(value, found_value):
                            token_arr.append(token(found_value,key))
                            found_value = ""
                            break
                        else:
                            pass
   
            if re.match(r"\"[a-zA-Z][a-zA-Z0-9\s]*", found_value):
                token_arr.append(token(found_value,"String"))
                
            elif re.match(r"[a-zA-Z][a-zA-Z0-9\s]*\"", found_value):
                token_arr.append(token(found_value,"String"))
            elif (found_value != ""):
                token_arr.append(token(found_value,"Identifier"))


        return token_arr



myTokenizer = Tokenizer()
text:str = fileManger.get_text("hello.txt")


my_token_list = myTokenizer.tokenize(text)

my_tokens = myTokenizer.get_token_type(my_token_list)
for i in my_tokens:
    i.print()
