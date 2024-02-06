class production_rule:
    value:str
    start_symbol =""
    def __init__(self,start_symbol,value):
        self.start_symbol=start_symbol
        self.value = value
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

    def print_prod_rules(self):
        for i in self.prod_rules:
            print(i.start_symbol, " => ",i.value)
        pass

    def fixLeftRecursion(self,recursive,non_recursive):
        new_prod = production_rule(recursive.start_symbol, non_recursive.value + recursive.start_symbol+"`") #unprimed version
        new_prod2 = production_rule(recursive.start_symbol + "`", recursive.value[1:]+recursive.start_symbol+"`") #primed version
        new_prod3 = production_rule(recursive.start_symbol + "`", "£") #epsilon
        
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
    
    # def removeDuplicateProdRules(self):
    #     arr = []
    #     for i in range(0,len(self.print_prod_rules)):
    #         for j in range(0,len(self.print_prod_rules)):
    #         if self.prod_rules.count(self.prod_rules[i]) >1:
    #             self.prod_rules.pop(i)


    


myRule = production_rule("A","Aa")
#print(myRule.isLeftRecursive())

myRule2 = production_rule("A","b")


#print(myRule2.isLeftRecursive())

myCFG = context_free_grammar("E",[myRule,myRule2],"e","f")
myCFG.add_prod_rule(production_rule("A","A+R"))


myCFG.left_recursion()
myCFG.removeDuplicateProdRules()
myCFG.print_prod_rules()
