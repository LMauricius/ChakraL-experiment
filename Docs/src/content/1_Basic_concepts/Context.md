# Context

## Definition

A context is the most primitive structure of ChakraL language. A context can be described and distinguished from other contexts by requirements opposed on it and functions that map from it into a possibly different context. There are two ways to define a context in ChakraL.

## The short way
 
```{.chakral caption="Example"}
(lives = 3, score = 0)
```

A context can be defined as a comma-separated list of descriptions. The short definition is used in expressions. A single trailing comma is optional in the single-line version and mandatory in the multiline version, where descriptions also have to be on independent lines from the parentheses.
 
```{.chakral caption="Example"}
(
    lives = 3,
    score = 0,
)
```
 
```{.chakralspec caption="Single-line usage"}
( DESCRIPTION1, DESCRIPTION2 <...> )
```

```{.chakralspec caption="Multi-line usage"}
(
    DESCRIPTION1,
    DESCRIPTION2, DESCRIPTION3,
    DESCRIPTION4, <...>
)
```

## The long way

A context can also be defined as a list of descriptions each starting at its own line of code. The long definition can be used in specific language constructs that require it. It is considered the long way because you can't put more than one description per line, and because it is only used in longer language constructs.

```{.chakral caption="Example"}
lives = 3
score = 0
```
 
```{.chakralspec caption="Multi-line usage"}
DESCRIPTION1
DESCRIPTION2
DESCRIPTION3
<...>
```

## What is a description
The descriptions tell the compiler how the context can be used. They describe what data can be associated with it and what states can the context be in. The *members* are values that are uniquely connected to one context. Each member has the respective mapping from 

Example of member declaration (and an assignment): `lives = 3`{.chakral}  
Example of requirement (the `lives` never reach zero): `?? lives > 0`{.chakral}  
Example of composition (the context 'includes' the description of a `Movable` context): `! Movable`{.chakral}

## Similar ideas in other languages
primitive data (integers or real numbers), complex objects, literal values, code blocks