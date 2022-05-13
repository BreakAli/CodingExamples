from enum import Enum

# This is a python script that mimics an object orientated language.
# Allowing for many expressions that an OO language would
# such as variables, equivalency, function declarations and calls.


# Name
class Name:
    def __init__(self, theName):
        self.theName = theName


# Binding
class Binding:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def toString(self):
        return str(self.name) + " " + str(self.value)


# Environment
class Environment:
    def __init__(self, binding, referencingEnvironment):
        self.binding = binding
        self.referencingEnvironment = referencingEnvironment

    def bind(self, name, value):
        return Environment(Binding(name, value), self)

    def lookup(self, name):
        if(self.binding == None):
            raise NameError("No Such Element Exception")

        if(self.binding.name.theName == name.theName):
            return self.binding.value

        return self.referencingEnvironment.lookup(name)


# Expression
class Expression:
    class IntConstant():
        def __init__(self, val):
            self.val = val

        def toString(self):
            return "IntConstant(" + str(self.val) + ")"

    class BinOpExpression():
        class Operator(Enum):
            PLUS = 1
            MINUS = 2
            TIMES = 3
            DIV = 4

        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

    class LetExpression():
        def __init__(self, variableName, value, body):
            self.variableName = variableName
            self.value = value
            self.body = body

    class VariableExpression():
        def __init__(self, variable):
            self.variable = variable

    class EqExpression():
        def __init__(self, left, right):
            self.left = left
            self.right = right

    class IfExpression():
        def __init__(self, cond, thenSide, elseSide):
            self.cond = cond
            self.thenSide = thenSide
            self.elseSide = elseSide

    class FunctionDeclExpression():
        def __init__(self, name, formalArguments, functionBody, scope):
            self.name = name
            self.formalArguments = formalArguments
            self.functionBody = functionBody
            self.scope = scope

    class FunctionCallExpression():
        def __init__(self, name, actualArguments):
            self.name = name
            self.actualArguments = actualArguments


# Value
class Value:
    class IntValue:
        def __init__(self, val):
            self.val = val

        def toString(self):
            return "IntValue(" + "val=" + self.val + ")"

    class BoolValue:
        def __init__(self, val):
            self.val = val

        def toString(self):
            return "BoolValue(" + "val=" + str(self.val) + ")"

    class FunctionValue:
        def __init__(self, pythonFunction):
            self.pythonFunction = pythonFunction

    class Closure:
        def __init__(self, caputuredEnvironment, formalArguments, functionBody):
            self.caputuredEnvironment = caputuredEnvironment
            self.formalArguments = formalArguments
            self.functionBody = functionBody


# Program
class Program:
    f1 = Expression.IntConstant(474)
    f2 = Expression.BinOpExpression(
        Expression.BinOpExpression.Operator.PLUS,
        Expression.IntConstant(400),
        Expression.IntConstant(74)
    )
    f3 = Expression.BinOpExpression(
        Expression.BinOpExpression.Operator.PLUS,
        Expression.IntConstant(400),
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.PLUS,
            Expression.IntConstant(70),
            Expression.IntConstant(4)
        )
    )
    f4 = Expression.LetExpression(
        Name("var"),
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.PLUS,
            Expression.IntConstant(400),
            Expression.IntConstant(70)
        ),
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.PLUS,
            Expression.VariableExpression(Name("var")),
            Expression.IntConstant(4)
        )
    )

    f5 = Expression.LetExpression(
        Name("v1"),
        Expression.IntConstant(400),
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.PLUS,
            Expression.LetExpression(
                Name("v2"),
                Expression.IntConstant(70),
                Expression.VariableExpression(Name("v2"))
            ),
            Expression.BinOpExpression(
                Expression.BinOpExpression.Operator.PLUS,
                Expression.IntConstant(4),
                Expression.VariableExpression(Name("v1"))
            )
        )
    )

    f6 = Expression.LetExpression(
        Name("var"),
        Expression.IntConstant(400),
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.PLUS,
            Expression.LetExpression(
                Name("var"),
                Expression.IntConstant(70),
                Expression.VariableExpression(Name("var"))
            ),
            Expression.BinOpExpression(
                Expression.BinOpExpression.Operator.PLUS,
                Expression.IntConstant(4),
                Expression.VariableExpression(Name("var"))
            )
        )
    )
    DBZ = Expression.BinOpExpression(
        Expression.BinOpExpression.Operator.DIV,
        Expression.IntConstant(474),
        Expression.IntConstant(0)
    )

    # 474   -> 474
    P1 = Expression.IntConstant(474)

    # ( ( 400 + 74 ) / 3)   -> 158
    P2 = Expression.BinOpExpression(
        Expression.BinOpExpression.Operator.DIV,
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.PLUS,
            Expression.IntConstant(400),
            Expression.IntConstant(74)
        ),
        Expression.IntConstant(3)
    )

    # ( ( 400 + 74 ) / 3) == 158  -> True
    P3 = Expression.EqExpression(
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.DIV,
            Expression.BinOpExpression(
                Expression.BinOpExpression.Operator.PLUS,
                Expression.IntConstant(400),
                Expression.IntConstant(74)
            ),
            Expression.IntConstant(3)
        ),
        Expression.IntConstant(158)
    )

    # if ((( 400 + 74 ) / 3) == 158 ) then 474 else 474/0 -> 474 no DBZ error
    P4 = Expression.IfExpression(
        Expression.EqExpression(
            Expression.BinOpExpression(
                Expression.BinOpExpression.Operator.DIV,
                Expression.BinOpExpression(
                    Expression.BinOpExpression.Operator.PLUS,
                    Expression.IntConstant(400),
                    Expression.IntConstant(74)
                ),
                Expression.IntConstant(3)
            ),
            Expression.IntConstant(158)
        ),
        Expression.IntConstant(474),
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.DIV,
            Expression.IntConstant(474),
            Expression.IntConstant(0)
        )
    )

    # let bot = 3 in
    #   (let bot = 2 in bot)
    #   +
    #   (if (bot == 0) then 474/0 else (400+74)/bot)  -> 160 or 239, no DBZ error

    P5 = Expression.LetExpression(
        Name("bot"),
        Expression.IntConstant(3),
        Expression.BinOpExpression(
            Expression.BinOpExpression.Operator.PLUS,
            Expression.LetExpression(
                Name("bot"),
                Expression.IntConstant(2),
                Expression.VariableExpression(Name("bot"))
            ),
            Expression.IfExpression(
                Expression.EqExpression(
                    Expression.VariableExpression(Name("bot")),
                    Expression.IntConstant(0)
                ),
                Expression.BinOpExpression(
                    Expression.BinOpExpression.Operator.DIV,
                    Expression.IntConstant(474),
                    Expression.IntConstant(0)
                ),
                Expression.BinOpExpression(
                    Expression.BinOpExpression.Operator.DIV,
                    Expression.BinOpExpression(
                        Expression.BinOpExpression.Operator.PLUS,
                        Expression.IntConstant(400),
                        Expression.IntConstant(74)
                    ),
                    Expression.VariableExpression(Name("bot"))
                )
            )
        )
    )

    # function f(top,bot) :
    #  if (bot == 0) then 0 else top/bot
    #
    #
    #   let bot = 3 in
    #      (let bot = 2 in bot)
    #        +
    #      (f(400+74,bot) + f(470+4,0))
    P6 = Expression.FunctionDeclExpression(
        Name("f"),
        [Name("top"), Name("bot")],
        Expression.IfExpression(
            Expression.EqExpression(
                Expression.VariableExpression(Name("bot")),
                Expression.IntConstant(0)
            ),
            Expression.IntConstant(0),
            Expression.BinOpExpression(
                Expression.BinOpExpression.Operator.DIV,
                Expression.VariableExpression(Name("top")),
                Expression.VariableExpression(Name("bot"))
            )
        ),
        Expression.LetExpression(
            Name("bot"),
            Expression.IntConstant(3),
            Expression.BinOpExpression(
                Expression.BinOpExpression.Operator.PLUS,
                Expression.LetExpression(
                    Name("bot"),
                    Expression.IntConstant(2),
                    Expression.VariableExpression(Name("bot"))
                ),
                Expression.BinOpExpression(
                    Expression.BinOpExpression.Operator.PLUS,
                    Expression.FunctionCallExpression(
                        Name("f"),
                        [Expression.BinOpExpression(
                            Expression.BinOpExpression.Operator.PLUS,
                            Expression.IntConstant(400),
                            Expression.IntConstant(74)
                        ),
                            Expression.VariableExpression(Name("bot"))]
                    ),
                    Expression.FunctionCallExpression(
                        Name("f"),
                        [Expression.BinOpExpression(
                            Expression.BinOpExpression.Operator.PLUS,
                            Expression.IntConstant(470),
                            Expression.IntConstant(4)
                        ),
                            Expression.IntConstant(0)]
                    )
                )
            )
        )
    )


class Interpreter:
    def functionHelper(actualValues, env, c, knownFunctions):
        envThatKnowsArgs = env
        formalArguments, functionBody = knownFunctions[c.name.theName]
        for i in range(len(actualValues)):
            envThatKnowsArgs = envThatKnowsArgs.bind(
                formalArguments[i], actualValues[i])
        return Interpreter.eval(functionBody, envThatKnowsArgs, knownFunctions)

    def eval(c, env, knownFunctions):
        className = c.__class__.__name__

        # Lack of Switch Statements in Python, so resorting to if else chain
        if(className == "IntConstant"):
            return Expression.IntConstant(c.val)

        elif(className == "BinOpExpression"):
            op = c.op
            left = Interpreter.eval(c.left, env, knownFunctions).val
            right = Interpreter.eval(c.right, env, knownFunctions).val

            if(op == Expression.BinOpExpression.Operator.PLUS):
                return Expression.IntConstant(left + right)
            elif(op == Expression.BinOpExpression.Operator.MINUS):
                return Expression.IntConstant(left - right)
            elif(op == Expression.BinOpExpression.Operator.TIMES):
                return Expression.IntConstant(left * right)
            elif(op == Expression.BinOpExpression.Operator.DIV):
                if(right == 0):
                    return Expression.IntConstant(0)
                return Expression.IntConstant(left // right)
            else:
                raise NameError("Unknown Operator in BinOp")

        elif(className == "LetExpression"):
            val = Interpreter.eval(c.value, env, knownFunctions)

            newE = env.bind(c.variableName, val)

            return Interpreter.eval(c.body, newE, knownFunctions)

        elif(className == "VariableExpression"):
            return env.lookup(c.variable)

        elif(className == "EqExpression"):
            left = Interpreter.eval(c.left, env, knownFunctions)
            right = Interpreter.eval(c.right, env, knownFunctions)

            result = (left.val == right.val)

            return Value.BoolValue(result)

        elif(className == "IfExpression"):
            cond = Interpreter.eval(c.cond, env, knownFunctions)

            if(cond.val):
                return Interpreter.eval(c.thenSide, env, knownFunctions)
            else:
                return Interpreter.eval(c.elseSide, env, knownFunctions)

        elif(className == "FunctionDeclExpression"):
            knownFunctions[c.name.theName] = (
                c.formalArguments, c.functionBody)

            return Interpreter.eval(c.scope, env, knownFunctions)

        elif(className == "FunctionCallExpression"):
            actualValues = []
            for i in range(len(c.actualArguments)):
                actualValues.append(Interpreter.eval(
                    c.actualArguments[i], env, knownFunctions))

            return Interpreter.functionHelper(actualValues, env, c, knownFunctions)

        else:
            raise NameError("Unknown Expression passed to eval()")


# Main Function
def main():
    env = Environment(None, None)
    knownFunctions = {}
    print(Interpreter.eval(Program.P1, env, knownFunctions).toString())


if __name__ == "__main__":
    main()
