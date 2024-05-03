# Converts single variables to a list containing that variable
# If given a list, returns the list untouched
def to_list(x: any) -> list:
    if not isinstance(x, list):
        return [x]
    return x

# Represents a symbol in lambda calculus expressions
class Symbol(object):
    # Initialises a Symbol object with an identifier
    def __init__(self, ID: str) -> None:
        self.ID: str = ID # Identifier for the symbol
    
    # Override __str__ method to return the symbol identifier
    def __str__(self) -> str:
        return self.ID

    # Substitute old symbol with new one if the identifiers match
    def substitute(self, old_symbol: 'Symbol', new_symbol: 'Symbol') -> 'Symbol':
        if self.ID == old_symbol.ID:
            return new_symbol
        else:
            return self

# Represents a lambda expression in lambda calculus
class LambdaExpression(object):
    # Initialises a LambdaExpression object with symbols and a body
    def __init__(self, symbols: 'Symbol | list[Symbol]', body: 'Symbol | list[Symbol | LambdaExpression]') -> None: 
        self.symbols: list['Symbol'] = to_list(symbols) # List of the expression's symbols
        self.body: list['Symbol' | 'LambdaExpression'] = to_list(body) # List containing the body of the expression 

    # Override __str__ method to return a string representation of the expression
    def __str__(self) -> str:
        symbols_string: str = "".join(str(var) for var in self.symbols) # Convert symbols to string representation
        body_string: str = "".join(str(part) for part in self.body) # Convert body to string representation
        return f"λ{symbols_string}.{body_string}" # Return the lambda expression as a string
    
    # Substitutes symbols in the lambda expression with new expressions
    def substitute(self, old_symbols: 'Symbol | list[Symbol]', new_expressions: 'LambdaExpression | list[LambdaExpression]') -> 'LambdaExpression | Application':
        old_symbols: list['Symbol'] = to_list(old_symbols) # Convert old symbols to a list if not already
        new_expressions: list['LambdaExpression'] = to_list(new_expressions) # Convert new expressions to a list if not already
        sub_bodies: list['Symbol' | 'LambdaExpression'] = [] # Initialises sub_bodies as a list
        for i in self.body:
            sub_bodies.append(i) # Copy body to sub_bodies

        # Iterate over sub_bodies to perform substitution
        for body in sub_bodies:
            for symbol in old_symbols:
                if body == symbol:
                    # Substitute the current symbol in the body with the corresponding new expression, then update the body with the substituted expression
                    sub_bodies[sub_bodies.index(body)] = sub_bodies[sub_bodies.index(body)].substitute(symbol, new_expressions[old_symbols.index(symbol)])
                    break
        
        # Check if the resulting substitution should be an Application or LambdaExpression
        if len(sub_bodies) > 1:
            return Application(sub_bodies[0], sub_bodies[1:])
        else:
            return LambdaExpression(self.symbols, sub_bodies)
        
    # Evaluates the lambda expression with given arguments
    def evaluate(self, arguments: 'LambdaExpression | list[LambdaExpression]') -> 'LambdaExpression | Application | list[Symbol | LambdaExpression]':
        arguments: list['LambdaExpression'] = to_list(arguments) # Converts arguments to a list if not already
        if len(self.body) > 1:
            return self.substitute(self.symbols, arguments).evaluate() # Recursively evaluate the substituted expression
        elif len(self.symbols) > 1:
            return arguments[self.symbols.index(self.body[0])] # Return the appropriate argument from the list
        else:
            return self.body.substitute(self.symbols, arguments) # Perform substitution if only one symbol

# Represents an application of a lambda expression
class Application(object):
    # Initialises an Application object with an operator and arguments
    def __init__(self, operator: 'LambdaExpression', arguments: 'LambdaExpression | list[LambdaExpression]') -> None:
        self.operator: 'LambdaExpression' = operator # The operator of the application
        self.arguments: list['LambdaExpression'] = to_list(arguments) # List of arguments to be applied
    
    # Override __str__ method to return a string representation of the Application
    def __str__(self):
        operator_string: str = str(self.operator) # Convert operator to string
        arguments_string: str = "".join(str(arg) for arg in self.arguments) # Convert arguments to string representation
        return f"({operator_string}){arguments_string}" # Return the application as a string

    # Substitute the old symbols with new expressions in both the operator and the arguments of the application
    def substitute(self, old_symbols: 'Symbol | list[Symbol]', new_expressions: 'LambdaExpression | list[LambdaExpression]') -> 'Application':
        return Application(self.operator.substitute(old_symbols, new_expressions), self.arguments[0].substitute(old_symbols, new_expressions))
    
    # Evaluates the application
    def evaluate(self) -> 'LambdaExpression | Application | list[Symbol | LambdaExpression]':
        if isinstance(self.arguments[0], Application):
            return self.operator.evaluate(self.arguments[0].evaluate()) # Recursively evaluate if the argument is an application
        else:
            return self.operator.evaluate(self.arguments) # Evaluate the operator with the argument

# Create Symbols
x = Symbol("x")
y = Symbol("y")

# Create LambdaExpressions
T = LambdaExpression([x,y], x)
F = LambdaExpression([x,y], y)
AND = LambdaExpression([x, y], [x, y, F])
OR = LambdaExpression([x, y], [x, T, y])
NOT = LambdaExpression(x, [x, F, T])

# Apply expressions
NT = Application(NOT, T)
NF = Application(NOT, F)
NNT = Application(NOT, NT)
NNNT = Application(NOT, NNT)
TORF = Application(OR, [T, F])
FORF = Application(OR, [F, F])
FANDT = Application(AND, [F, T])
TANDT = Application(AND, [T, T]) 

# Put applications and names of applications in list for iteration
names: list[str] = ["NOT TRUE", "NOT FALSE", "NOT NOT TRUE", "NOT NOT NOT TRUE", "TRUE OR FALSE", "FALSE OR FALSE", "FALSE AND TRUE", "TRUE AND TRUE"]
apps: list['Application'] = [NT, NF, NNT, NNNT, TORF, FORF, FANDT, TANDT]

if __name__ == '__main__':
    print()
    print("\033[1mLambda Expressions\033[0m")
    print(f"True: {T}")
    print(f"False: {F}")
    print(f"And: {AND}")
    print(f"Or: {OR}")
    print(f"Not: {NOT}")
    print()
    print("\033[1mApplications and their evaluations\033[0m")
    for n in range(len(apps)):
        print(f"{names[n]}: {apps[n]} ==> {apps[n].evaluate()}")
    print()