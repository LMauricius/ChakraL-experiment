# Logical operators

## Usage
Logical operators are used in condition checking for boolean alghebra. They can be overloaded and overriden by defining a value with the operator identifier. The return trait of these functions is always `bool`{.chakral}.

```{.chakral caption="Example of 'and' operator'"}
with output=console:
    if health ?= 0.0 and extralives ?= 0:
        write "You died!"
ok
```

## Supported operators

| Type   | Symbol | Meaning |
| ------ | ------ | ------- |
| Unary | `not` | whether it's not true |
| Binary | `and` | whether both is true |
| Binary | `or` | whether at least one is true |
| Binary | `xor` | whether only one is true |