# Operator as

## Usage
The `as` is the cast (conversion) operator. It returns a value with the right operand as its required trait. The conversion can be done in several ways.

## Table

| Type   | Symbol | Operator identifier | Meaning |
| ------ | ------ | ------------------- | ------- |
| Binary | `as` | `cast\` | conversion for usage with another trait |

## Temporary cast
Temporary cast happens when the cast value is used in an expression that modifies it. It is equivalent to casting the original before using the converted value, and casting the modified value back to its original trait after the converted value isn't used anymore.

```{.chakral caption="Example of a temporary cast"}
with output=console:
    myList: List = [1, 2]
    write myList **prints '[1, 2]'
    myList += [3, 4] **concatenates lists
    write myList **prints '[1, 2, 3, 4]'
    myList as Vector += [2, 1, 2, 1] **adds elements of a mathematical vector
    write myList **prints '[3, 3, 5, 5]'
ok
```

A temporary cast:
```{.chakral}
a: TraitA = ()
modifyB (a as TraitB)
```
...is equivalent to this:
```{.chakral}
a: TraitA = ()
b = a as TraitB
modifyB b
a = b as TraitA
```

## Borrow cast
A borrow cast is an extended version of temporary cast.

```{.chakral caption="Example of a borrow cast"}
NormalVars def:
    explicit
    a:int32
    b:int32
ok

DoubledVars def:
    explicit
    a:int32
    b:int32
ok

cast\ def (vars: NormalVars mut) volatile -> (vars: DoubledVars):
    a vars *= 2
    b vars *= 2
    write(output=console, msg="Doubled numbers!")
ok

cast\ def (vars: DoubledVars mut) volatile -> (vars: NormalVars):
    a vars /= 2
    b vars /= 2
    write(output=console, msg="Halved numbers!")
ok

v = NormalVars & (a = 3, b = 4)
write(output=console, msg=v) **prints '(a = 3, b = 4)'

using v as DoubledVars:
    **prints 'Doubled numbers!'
    write(output=console, msg=v) **prints '(a = 6, b = 8)'
ok
**prints 'Halved numbers!'
write(output=console, msg=v) **prints '(a = 3, b = 4)'
```

```{.chakral caption="Example of RAII using a borrow cast"}
myFile = File "hello.txt"

using myFile as Open:
    filecontent = read(input = text myFile, type = String)
    write(output = console, msg = filecontent)
ok
```

```{.chakral caption="Conscise example of RAII using a borrow cast"}
with input = Open File "hello.txt", output = console:
    filecontent = read String **from file
    write filecontent **to console
ok
```