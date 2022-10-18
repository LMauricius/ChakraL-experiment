# Operator as

## Usage
The `as` is the cast (conversion) operator. It returns a value with the right operand as its required trait. The conversion can be done in several ways.

## Table

| Type   | Symbol | Operator identifier | Meaning |
| ------ | ------ | ------------------- | ------- |
| Binary | `as` | `cast\` | conversion for usage with another trait |

## Temporary cast

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