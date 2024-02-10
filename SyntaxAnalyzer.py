import CFG
import tokenizer

myLexicalAnalyzer = tokenizer.tokenFrontEnd("hello.txt")

# Create Start Symbol
startSymbol = "E"

# Initialize Production rules
myRule = CFG.production_rule("E", "E+T")
myRule2 = CFG.production_rule("E", "T")
myRule3 = CFG.production_rule("T", "T*F")
myRule4 = CFG.production_rule("T", "F")
myRule5 = CFG.production_rule("F", "(E)")
myRule6 = CFG.production_rule("F", "id")

# Create syntax Analyzer using context free grammar
mySyntaxAnalyzer = CFG.context_free_grammar("E", [myRule, myRule2,myRule3,myRule4,myRule5,myRule6], ["+","*","(",")","id"], ["E", "T","F"])

print("\nProduction rules: ")
mySyntaxAnalyzer.print_prod_rules()

print("\nEliminate left recursion: ")
mySyntaxAnalyzer.left_recursion()
mySyntaxAnalyzer.removeDuplicateProdRules()
mySyntaxAnalyzer.print_prod_rules()

# Inializes pridictive matix with terminal as rows and Non Terminals as columns
mySyntaxAnalyzer.define_predictive_matrix()

print("\nCompute first and follow funtions: ")

first_set = mySyntaxAnalyzer.compute_first()
print("\nFirst:")
for non_terminal, terminals in first_set.items():
    print(non_terminal, ":", terminals) 

follow_set = mySyntaxAnalyzer.compute_follow()
print("\nFollow:")
for non_terminal, terminals in follow_set.items():
    print(non_terminal, ":", terminals) 

mySyntaxAnalyzer.add_epsilon_rules_predictive()
# Display output of predictive matrix to the console
mySyntaxAnalyzer.print_predictive_matrix()
print("\n")
#mySyntaxAnalyzer.compute_stack(display=True)
temp = "" 

while not myLexicalAnalyzer.tokenEnd():
    
    value = myLexicalAnalyzer.get_next_token()
    if value == "":
        if temp != "":
            if (mySyntaxAnalyzer.compute_stack(temp,display=True)):
                print(temp,"is a valid sentence\n")
            else:
                print(temp,"failed to be parsed\n")
        temp = ""
    else:
        temp = value
