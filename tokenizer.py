import re

class fileManger:
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
        "keyword": r"\b(int|main|std|cout|endl|return|float)\b",
        "punctuator": r"[,{}():<>]",
        "int": r"\d+",
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
            char_index = 0
            while char_index < len(str(unprocessed_token)):
                found_value += str(unprocessed_token)[char_index]
                for key, value in self.tokenTypes.items():
                        if re.match(value, found_value):
                            if key == "int":
                                ind = 0;
                                bool = True
                                while bool == True:
                                    ind += 1; 
                                    if((char_index+ind) < len(str(unprocessed_token))):
                                        if re.match(value, str(unprocessed_token)[char_index + ind]):
                                            found_value += str(unprocessed_token)[char_index + ind]
                                        else:
                                            bool = False
                                    else:
                                        bool = False
                                print(ind)
                                char_index += ind
                            token_arr.append(token(found_value,key))
                            found_value = ""
                            break
                        else:
                            pass
                char_index+= 1
   
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
