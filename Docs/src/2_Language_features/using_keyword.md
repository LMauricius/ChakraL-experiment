# using keyword

## Description
The `using` keyword is used to define values based on already named values. 

## Usage
Use: `using NAMED_VALUE`

For example, if we want to use the `sin` function from the `Math` module without typing `sin(module Math)` every time, we can write:
```
using sin(module Math)
```
...and then use it like this:
```
amp = sin 30°
```

For a more complex example, if we have a following context:
```
myComplexContext def (
    numValue = 0.5,
    textValue = "Hello!",
    subContext = (
        subSubValue = 1.5
    )
)
```
...and we need to use the `subSubValue` often, we could shorten the future code by doing this:
```
subSubValue def subSubValue(subContext myComplexContext)
write(subSubValue)
```
...or we could use the `using` keyword to do the same:
```
using subSubValue(subContext myComplexContext)
write(subSubValue)
```