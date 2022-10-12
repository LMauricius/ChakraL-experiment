# Comparison operators

## Usage
Comparison operators are operators usually used in math but also repurposed for other use-cases, similar to math operators. Their meaning depends on the traits of operands. They can be overloaded and overriden by defining a value with the operator identifier. The return trait of these functions must always be `bool`{.chakral}.
```{.chakral caption="Example of redefining the '?=' operator"}
equals\ def (l: Point, r: Point)->bool:
    return x l ?= x r and y l ?= y r
ok
```

## Supported operators

| Type   | Symbol | Operator identifier | Mathematical usage | Container usage | Bitwise usage |
| ------ | ------ | ------------------- | ------------------ | --------------- | ------------- |
| Binary | `?=` | equals\ | value compare | size and element compare | bit compare |
| Binary | `!=` | notequals\ | value compare | size and element compare | bit compare |
| Binary | `>` | greater\ | order | first different element / alphabetical / order | none |
| Binary | `>=` | greaterequals\ | order | first different element / alphabetical / order | none |
| Binary | `<` | less\ | order | first different element / alphabetical / order | none |
| Binary | `<=` | lessequals\ | order | first different element / alphabetical / order | none |