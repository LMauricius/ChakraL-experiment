# Context

## Definition

A context is the most primitive structure of ChakraL language. A context can be described and distinguished from other contexts by requirements opposed on it and functions that map from it into a possibly different context. There are two ways to define a context in ChakraL.

## The short way

Example:  
```
(lives = 3, score = 0)
```

A context can be defined as a comma-separated list of descriptions. The short definition is used in expressions. A single trailing comma is optional in the single-line version and mandatory in the multiline version, where descriptions also have to be on independent lines from the parentheses.

Example:  
```
(
    lives = 3,
    score = 0,
)
```

Write:  
```
( DESCRIPTION1, DESCRIPTION2 <...> )
```
Or:  
```
(
    DESCRIPTION1,
    DESCRIPTION2, DESCRIPTION3,
    DESCRIPTION4, <...>
)
```

## The long way

A context can also be defined as a list of descriptions each starting at its own line of code. The long definition can be used in specific language constructs that require it. It is considered the long way because you can't put more than one description per line, and because it is only used in longer language constructs.

Example: 
```
lives = 3
score = 0
```

Write:  
```
DESCRIPTION1
DESCRIPTION2
DESCRIPTION3
<...>
```

## Description

Example of assignment: `lives = 3`  
Example of requirement: `?? lives > 0`
Example of composition: `! Movable`

## Similar ideas in other languages
primitive data (integers or real numbers), complex objects, literal values, code blocks