class production_rule:
    value:str
    start_symbol =""
    def __init__(self,start_symbol,value):
        self.start_symbol=start_symbol
        self.value = value
    def __eq__(self, __value) -> bool:
        if isinstance(__value,production_rule):
            return self.value == __value.value and self.start_symbol == __value.start_symbol
        return False
    
    def isLeftRecursive(self):
        if self.start_symbol==self.value[0]:
            return True
        return False
    
    def output(self):
        if self.start_symbol=="":
            return ""
        return self.start_symbol+" => "+self.value
        
    def copy(self):
        return production_rule(self.start_symbol,self.value)
    def is_null(self):
        return self.start_symbol == "";

class context_free_grammar:
    def __init__(self,start_symbol,prod_rules,terminals,non_terminals):
        self.start_symbol=start_symbol
        self.prod_rules = prod_rules
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.predictive_matrix={}
        
    def define_predictive_matrix(self):
        for i in self.non_terminals:
            self.predictive_matrix[i]={}
            for j in self.terminals:
                if j!="£":
                    self.predictive_matrix[i][j] = production_rule("","")

    def print_predictive_matrix(self):
        #print column headers
        print("\nPredictive Parsing Table")
        print("\n\t",end="")
        for i in self.terminals:
            if i!="£":
                print("{:<10}".format(i),end="|")
        #print("\n______________________________________________________",end="")
        for i in self.predictive_matrix:
            print("\n"+i+":",end="\t")
            for j in self.predictive_matrix[i]:
                print("{:<10}".format(self.predictive_matrix[i][j].output()),end="|")
                #print (self.predictive_matrix[i][j]+"\t\t",end="|")
        print()

    def add_prod_rule(self,prod_rule):
        self.prod_rules.append(prod_rule)

    def group_pro_rules(self):
        prod_rules_dictionary = {}
        for i in self.prod_rules:
            if i.start_symbol in prod_rules_dictionary:
                prod_rules_dictionary[i.start_symbol].append(i.value)
            else:
                prod_rules_dictionary[i.start_symbol] = [i.value]
        return prod_rules_dictionary
    
    def compute_first(self):
        
        first = {}
        for non_terminal in self.non_terminals:
            first[non_terminal] = set() #first is dict, key is non_terminal

        while True:
            updated = False
            for rule in self.prod_rules:
                non_terminal, production = rule.start_symbol, rule.value
                if production[0] in self.terminals:  # if first symbol is terminal, add it to first set
                    if production[0] not in first[non_terminal]:
                        if production[0]!="£":
                            self.predictive_matrix[non_terminal][production[0]] = rule.copy() #add rule to predictive table matrix
                        first[non_terminal].add(production[0])
                        updated = True
                elif production[0:2] == "id":
                    if "id" not in first[non_terminal]:
                        first[non_terminal].add(production[0:2])
                        self.predictive_matrix[non_terminal][production[0:2]] = rule.copy() #add rule to predictive table matrix
                        updated = True
                elif production[0] in self.non_terminals:  # if first symbol is non-terminal, add its first set
                    for terminal in first[production[0]]:
                        if terminal not in first[non_terminal]:
                            first[non_terminal].add(terminal)
                            self.predictive_matrix[non_terminal][terminal] = rule.copy() #add rule to predictive table matrix
                            updated = True
            if not updated:
                break

        return first


    def compute_follow(self):
        follow = {}
        for non_terminal in self.non_terminals:
            follow[non_terminal] = set() # {E,E`,T,T`,F} 
        follow[self.start_symbol].add('$')  # add end marker to start symbol {E: [$] }
        if "$" not in self.terminals:
            self.terminals.append("$")

        while True:
            updated = False
            for rule in self.prod_rules: # each production rule
                non_terminal, production = rule.start_symbol, rule.value
                production = self.valueToProdArray(production) # converts E+id+T` to [E,+,id,T`]
                for i in range(len(production)): # E' => [+,T,E`]
                    if production[i] in self.non_terminals:  # if symbol is non-terminal
                        if i == len(production) - 1:  # if it's the last symbol in production
                            for terminal in follow[non_terminal]:
                                if terminal not in follow[production[i]]:
                                    follow[production[i]].add(terminal)
                                    updated = True
                        else:
                            next_symbol = production[i + 1]
                          
                            if next_symbol in self.terminals :  # if next symbol is terminal
                                #print("check: ",production[i], production[i+1])
                                if next_symbol not in follow[production[i]]:
                                    follow[production[i]].add(next_symbol)
                                    updated = True
                            else:  # if next symbol is non-terminal
                                for terminal in self.compute_first()[next_symbol]:

                                    if terminal == "£":
                                        follow[production[i]] =follow[production[i]].union(follow[next_symbol])
                                        """for i in follow[next_symbol]:
                                            print("in followof next ",i)
                                            self.predictive_matrix[next_symbol][i] = production_rule(next_symbol,"£") """
                                        continue
                                      #  print("£ ", next_symbol ," ", non_terminal, "=>", production)

                                    if terminal not in follow[production[i]]:
                                        follow[production[i]].add(terminal)
                                        updated = True

            if not updated:
                break

        return follow

    def valueToProdArray(self,value):
        prod_array =[]
        i = 0
        while i < len(value):  #loops through all charaters in production value

            if i+1 >= len(value): # Stop converting if at end
                prod_array.append(value[i])
                return prod_array
                
            if value[i+1] == '`':
                prod_array.append(value[i:i+2]) # add Termial with backtick(`)
                i+= 1
            elif value[i:i+2] == "id":
                 prod_array.append(value[i:i+2]) # add id 
                 i+= 1
            else:
                prod_array.append(value[i])
            i+= 1
        return prod_array
        
    # M[A,b] = A ==> a, if epsilon is in the First(a), b is in the Follow(A)
    def add_epsilon_rules_predictive(self):
        first_set = self.compute_first()
        for non_terminal, terminals in first_set.items():
     #       print(non_terminal,": ",terminals)
            if "£" in terminals:
                for term in self.compute_follow()[non_terminal]:
                    new = production_rule(non_terminal,"£")
                    self.predictive_matrix[non_terminal][term] = new.copy()

    def print_prod_rules(self):
        for i in self.prod_rules:
            print(i.start_symbol, " => ",i.value)
        pass

    def fixLeftRecursion(self,recursive,non_recursive):
        newNT = recursive.start_symbol + "`"

        new_prod = production_rule(recursive.start_symbol, non_recursive.value + recursive.start_symbol+"`") #unprimed version
        new_prod2 = production_rule(recursive.start_symbol + "`", recursive.value[1:]+recursive.start_symbol+"`") #primed version
        new_prod3 = production_rule(recursive.start_symbol + "`", "£") #epsilon
        
        if newNT not in self.non_terminals:
            self.non_terminals.append(newNT)

        if "£" not in self.terminals:
            self.terminals.append("£")
        
        return [new_prod,new_prod2,new_prod3]

    def left_recursion(self):
        fixed_prod_rules=[]
        fixers = []  #production rules used in fixing left recusive production rules
        for i in self.prod_rules:
            if i.isLeftRecursive():
                fixed = False
                for j in self.prod_rules:
                    if j.start_symbol==i.start_symbol:
                        if (not j.isLeftRecursive()):
                            fixed_prod_rules.extend(self.fixLeftRecursion(i,j))
                            if not j in fixers: # don't add rule if present in fixers
                                fixers.append(j)
                            fixed = True
                            continue
                if (not fixed):
                    print("Error: no rule with similar start symbol")
                    return

            else: 
                fixed_prod_rules.append(i)

        self.prod_rules = fixed_prod_rules
        for i in fixers:
            self.prod_rules.remove(i)

    def removeDuplicateProdRules(self):
        arr = []
        for i in self.prod_rules:
                    if arr.count(i) ==0:
                        arr.append(i)
        self.prod_rules = arr 

    def compute_stack(self,w = "id*id+id",display=False):
        parse_string= w
        parse_string= self.valueToProdArray(parse_string) #separate the terminals in the string
        if display:
            print(parse_string)
        stack=["$"]
        parse_string.append("$")
        stack.append(self.start_symbol)
        output=""
        if display:
            print("{:<30} {:<30} {:<30}".format("STACK","INPUT","OUTPUT"),end="") #print table column headings
        if display:
            print("\n{:<30} {:<30} {:<30}".format(''.join(stack), ''.join(parse_string), ''.join(output)),end="|") #print values in stack, input, and output

        while stack != ["$"]:
            #when input is empty, so use epsilon
            if len(parse_string)==0:
                rule = self.predictive_matrix[stack[-1]]["$"] #get prod rule in matrix cell
                stack.pop(-1)
                output = rule.start_symbol+"=>"+"".join(rule.value)
                if display:
                    print("\n{:<30} {:<30} {:<30}".format(''.join(stack), ''.join(parse_string), ''.join(output)),end="|") #print values in stack, input, and output
                continue 

            #when last element in stack is a terminal
            if stack[-1] == parse_string[0]: #compare last element of stack to first element of input string
                parse_string.pop(0) #remove first element in parse string
                stack.pop(-1) #remove last element in stack
                output=[]
                if display:
                    print("\n{:<30} {:<30} {:<30}".format(''.join(stack), ''.join(parse_string), ''.join(output)),end="|") #print values in stack, input, and output
                continue

            #when last element in stack is a non terminal
            else:
                rule = self.predictive_matrix[stack[-1]][parse_string[0]].copy() #get prod rule in matrix cell
                if rule.is_null():
                    print()
                    return False
                stack.pop(-1)

                rule.value = self.valueToProdArray(rule.value) #consider terminals with back ticks
                output = rule.start_symbol+"=>"+"".join(rule.value)
                #print("type ", type(rule.value))
                if rule.value!= ["£"]:         
                    rule.value.reverse() #read prod rule backwards
                    for i in rule.value:
                        stack.append(i)
                if display:
                    print("\n{:<30} {:<30} {:<30}".format(''.join(stack), ''.join(parse_string), ''.join(output)),end="|") #print values in stack, input, and output
                continue 

        print()
        if parse_string[0] == stack[0] == "$":
                return True
        else:
            return False
        
        
    def remove_duplicates_from_list(self, input_list):
        unique_list = []
        for item in input_list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list


    def leftFactor(self):
        prod_dict = self.group_pro_rules()
        prod_temp_store = {}
        for key, value in prod_dict.items():
            list_of_items = []
            for token in value:
                for i in range(len(token)):
                    if(i == 0):
                        list_of_items.append(token[i])
                    else:
                        for j in value:
                            if(j != token):
                                if token[:i + 1] == j[:i + 1]:
                                    if token[: i] in list_of_items:
                                        index = list_of_items.index(token[: i])  
                                        list_of_items[index] = token[:i + 1]

            unique_list = self.remove_duplicates_from_list(list_of_items)
            prod_temp_store[key] = unique_list
        left_factored_rules = {}
        for key, value in prod_temp_store.items():
            values_to_compare_with = prod_dict[key]
            count = 0
            for shortened_token in value:
                for full_token in values_to_compare_with:
                    if shortened_token == full_token[: len(shortened_token)]:
                        count += 1
                if count  == 1:
                    for full_token in values_to_compare_with:
                        if shortened_token == full_token[: len(shortened_token)]:
                            if key in left_factored_rules:
                                left_factored_rules[key].append(full_token)
                            else:
                                left_factored_rules[key] = [full_token]
                else:
                    substituted_values = []
                    if key in left_factored_rules:
                        left_factored_rules[key].append(shortened_token + key + "_prime")
                    else:
                        left_factored_rules[key] = [shortened_token + key + "_prime"]

                    for full_token in values_to_compare_with:
                        if shortened_token == full_token[: len(shortened_token)]:
                            result = full_token[len(shortened_token):]
                            if(result == ""):
                                substituted_values.append("$")
                            else:
                                substituted_values.append(result)
                    left_factored_rules[key + "_prime"] = substituted_values
                count = 0
        for key, value in left_factored_rules.items():
            for i in value:
                self.add_prod_rule(production_rule(key,i))
"""
myRule = production_rule("E", "E+T")
myRule2 = production_rule("E", "T")
myRule3 = production_rule("T", "T*F")
myRule4 = production_rule("T", "F")
myRule5 = production_rule("F", "(E)")
myRule6 = production_rule("F", "id")

myCFG = context_free_grammar("E", [myRule, myRule2,myRule3,myRule4,myRule5,myRule6], ["+","*","(",")","id"], ["E", "T","F"])

print("\nProduction rules: ")
myCFG.print_prod_rules()

print("\nEliminate left recursion: ")
myCFG.left_recursion()
myCFG.removeDuplicateProdRules()
myCFG.print_prod_rules()

myCFG.define_predictive_matrix()
print("\nCompute first and follow funtions: ")
first_set = myCFG.compute_first()
print("\nFirst:")
for non_terminal, terminals in first_set.items():
    print(non_terminal, ":", terminals) 

follow_set = myCFG.compute_follow()
print("\nFollow:")
for non_terminal, terminals in follow_set.items():
    print(non_terminal, ":", terminals) 

myCFG.add_epsilon_rules_predictive()
myCFG.print_predictive_matrix()
#print(myCFG.predictive_matrix)
print()
test = ["id+id+id+id","id","()"]
for i in test:
    if (myCFG.compute_stack(i,display=True)):
        print(i,"is valid")
    else:
        print(i,"failed to be parsed")
"""
