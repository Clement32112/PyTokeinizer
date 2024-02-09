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

class context_free_grammar:
    def __init__(self,start_symbol,prod_rules,terminals,non_terminals):
        self.start_symbol=start_symbol
        self.prod_rules = prod_rules
        self.terminals = terminals
        self.non_terminals = non_terminals

    def add_prod_rule(self,prod_rule):
        self.prod_rules.append(prod_rule)
    
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
                        first[non_terminal].add(production[0])
                        updated = True
                elif production[0:2] == "id":
                    if "id" not in first[non_terminal]:
                        first[non_terminal].add(production[0:2])
                        updated = True
                elif production[0] in self.non_terminals:  # if first symbol is non-terminal, add its first set
                    for terminal in first[production[0]]:
                        if terminal not in first[non_terminal]:
                            first[non_terminal].add(terminal)
                            updated = True
            if not updated:
                break

        return first

    def compute_follow(self):
        follow = {}
        for non_terminal in self.non_terminals:
            follow[non_terminal] = set()
        follow[self.start_symbol].add('$')  # add end marker to start symbol

        while True:
            updated = False
            for rule in self.prod_rules:
                non_terminal, production = rule.start_symbol, rule.value
                for i in range(len(production)):
                    if production[i] in self.non_terminals:  # if symbol is non-terminal
                        if i == len(production) - 1:  # if it's the last symbol in production
                            for terminal in follow[non_terminal]:
                                if terminal not in follow[production[i]]:
                                    follow[production[i]].add(terminal)
                                    updated = True
                        else:
                            next_symbol = production[i + 1]
                            if next_symbol in self.terminals:  # if next symbol is terminal
                                if next_symbol not in follow[production[i]]:
                                    follow[production[i]].add(next_symbol)
                                    updated = True
                            else:  # if next symbol is non-terminal
                                for terminal in self.compute_first()[next_symbol]:
                                    if terminal not in follow[production[i]]:
                                        follow[production[i]].add(terminal)
                                        updated = True

            if not updated:
                break

        return follow
    
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
                print("me left recurs")
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
                    print("Error: no reule with simiar start symbol")
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

myRule = production_rule("E", "E+T")
myRule2 = production_rule("E", "T")
myRule3 = production_rule("T", "T*F")
myRule4 = production_rule("T", "F")
myRule5 = production_rule("F", "(E)")
myRule6 = production_rule("F", "id")


terminals = set()
for rule in [myRule, myRule2]:
    for symbol in rule.value:
        if symbol:
            terminals.add(symbol)
            
myCFG = context_free_grammar("E", [myRule, myRule2,myRule3,myRule4,myRule5,myRule6], ["+","*","(",")","id"], ["E", "T","F"])

myCFG.left_recursion()
myCFG.removeDuplicateProdRules()
myCFG.print_prod_rules()

first_set = myCFG.compute_first()
print("First:")
for non_terminal, terminals in first_set.items():
    print(non_terminal, ":", terminals)

follow_set = myCFG.compute_follow()
print("\nFollow:")
for non_terminal, terminals in follow_set.items():
    print(non_terminal, ":", terminals)
