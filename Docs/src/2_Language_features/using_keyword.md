# using keyword

## Description
The `using` keyword is used to define values based on already named values. 

## Usage
Write: `using NAMED_VALUE`

For example, if we want to use the `sin` function from the `MyMath` module without typing `sin(module MyMath)` every time, we can write:
```
using sin (module MyMath)
```
...and then use it like this:
```
amp = sin 30°
```

For a more complex example, if we have a following context:
```
myComplexContext def (
    numValue def 0.5,
    textValue def "Hello!",
    subContext def (
        subSubNum def 1.5,
        subSubText def "foo"
    )
)
```
...and we need to use the `subSubNum` often, we could shorten the future code by doing this:
```
subSubValue def subSubNum subContext myComplexContext
write subSubNum #Hint: prints 1.5
```
...or we could use the `using` keyword to do the same:
```
using subSubNum subContext myComplexContext
write subSubNum #Hint: prints 1.5
```

If we want to use multiple values from a module, and we don't want to write `using` for each value from it, we can perform a `using` statement on the whole module: `using module MyMath`. This is of course equivalent to writing `MyMath def module MyMath`. Then instead of writing hard to read code:
```
y = (sin (module MyMath)) angle
x = (cos (module MyMath)) angle
```
...we can clean it up:
```
y = (sin MyMath) angle
x = (cos MyMath) angle
```
This requires us to still write longer code than if we were `using` each specific function from `MyMath`, but it makes it clear from where we got the function values `sin` and `cos`.