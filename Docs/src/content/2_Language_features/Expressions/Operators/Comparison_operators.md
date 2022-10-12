# Comparison operators

## Usage
Comparison operators are operators usually used in math but also repurposed for other use-cases, similar to math operators. Their meaning depends on the traits of operands. They can be overloaded and overriden by defining a value with the operator identifier. The return trait of these functions must always be `bool`{.chakral}.

```{.chakral caption="Example of comparison"}
with input=console, output=console:
    write "Enter X:"
    x = read Int
    write "Enter Y:"
    y = read Int

    if x > y:
        write "X is greater"
    elif x < y:
        write "Y is greater"
    else:
        write "They are equal"
ok
```

```{.chakral caption="Example of redefining the '?=' operator"}
equals\ def (left: Point, right: Point)->bool:
    return whether x left ?= x right and y left ?= y right
ok
```

## Supported operators

| Type   | Symbol | Operator identifier | Mathematical usage | Container usage | Bitwise usage |
| ------ | ------ | ------------------- | ------------------ | --------------- | ------------- |
| Binary | `?=` | `equals\` | value compare | size and element compare | bit compare |
| Binary | `!=` | `notequals\` | value compare | size and element compare | bit compare |
| Binary | `>` | `greater\` | order | first different element / alphabetical / order | none |
| Binary | `>=` | `greaterequals\` | order | first different element / alphabetical / order | none |
| Binary | `<` | `less\` | order | first different element / alphabetical / order | none |
| Binary | `<=` | `lessequals\` | order | first different element / alphabetical / order | none |