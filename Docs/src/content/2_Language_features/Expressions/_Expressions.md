# Expressions

## Examples
Literals are expressions. 
Variables are expressions. 
`a + 2` is an expression. 
`score + 100` is an expression. 
`sin 30°` is an expression. 
`[0.5, 1.5, 8.3]` is an expression. 
`normalized vector [0.5, 1.5, 8.3]` is an expression. 



## Named expressions
Expressions can have a name associated with them, which is used in other language features. We haven't yet introduced all types of expressions, but here is a cheat sheet describing how we deduce the name of various expressions.

The name associated with a variable/constant is its identifier.
The name associated with the `module MODULE.SUBMODULE1.<...>` expression is the name of the most significant (deepest) submodule.
The name associated with the `FUNCTION ARGUMENT` (a function call) expression is the name of the function.
The name associated with the `LEFT as RIGHT` expression is the name of the left expression.