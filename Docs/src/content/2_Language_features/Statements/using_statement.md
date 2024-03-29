# using statement

## Description
The `using` keyword is used to define values based on already named values. 

## Formal usage
Write: `using NAMED_EXPRESSION`.

This is equivalent to writing `NAME def NAMED_EXPRESSION`, where the expression's value has the same name asociated with it as the value we are defining. The expression can be complex, but its result must have a name associated with it.

## Examples

### Basic example
The `using` statement is often used along with the `module` expression described in the chapter [module expression](module_expression.html). For example, if we want to use the `sin` function from the `MyMath` module without typing `sin(module MyMath)` every time, we can write:
```{.chakral caption="Example"}
using sin (module MyMath)
```
...and then use it like this:
```{.chakral caption="Example"}
amp = sin 30°
```
This is because the expression `sin (module MyMath)`'s result has the name `sin` associated with it.

### Complex example
For a more complex example, if we have a following context:
```{.chakral caption="Example problem"}
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
```{.chakral caption="Example long solution"}
subSubNum def subSubNum subContext myComplexContext
a = subSubNum **Hint: a equals to 1.5
```
...or we could use the `using`{.chakral} keyword to do the same:
```{.chakral caption="Example good solution"}
using subSubNum subContext myComplexContext
a = subSubNum **Hint: a equals to 1.5
```

### *using module* example
If we want to use multiple values from a module, and we don't want to write `using` for each value from it, we can perform a `using` statement on the whole module: `using module MyMath`{.chakral}. This is of course equivalent to writing `MyMath def module MyMath`. Then instead of writing hard to read code:
```{.chakral caption="Example unreadable code"}
y = (sin (module MyMath)) angle
x = (cos (module MyMath)) angle
```
...we can clean it up:
```{.chakral caption="Example clean code"}
using module MyMath
y = (sin MyMath) angle
x = (cos MyMath) angle
```
This requires us to still write longer code than if we were `using` each specific function from `MyMath`, but it makes it clear from where we got the function values `sin` and `cos`. To shorten it further, we need to be `using` each required function:
```{.chakral caption="Example shortest code"}
using sin (module MyMath)
using cos (module MyMath)
y = sin angle
x = cos angle
```
