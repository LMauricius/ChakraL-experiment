# Math operators

## Usage
Math operators are operators usually used in math but also repurposed for other use-cases. Their meaning depends on the traits of operands. They can be overloaded and overriden by defining a value with the operator identifier.

```{.chakral caption="Example of addition"}
with input=console, output=console:
    write "Enter X:"
    x = read Int
    write "Enter Y:"
    y = read Int

    write x+y
ok
```
```{.chakral caption="Example of redefining the '+' operator"}
plus\ def (left: Point, right: Point)->Point:
    return Point(x = x left + x right, y = y left + y right)
ok
```

## Supported operators

| Type   | Symbol | Operator identifier | Mathematical usage | Container usage | Bitwise usage |
| ------ | ------ | ------------------- | ------------------ | --------------- | ------------- |
| Unary | `-` | `negative\` | negation | none | negation |
| Binary | `+` | `plus\` | addition | concatenation | or |
| Binary | `-` | `minus\` | subtraction | removal | and not |
| Binary | `*` | `star\` | multiplication | none | and |
| Binary | `/` | `divide\` | division | none | none |
| Binary | `^` | `superscript\` | power | none | xor |
| Binary | `%` | `percent\` | modulo | none | none |
| Binary | `×` | `cross\` | cross product | none | none |
| Binary | `⋅` | `dot\` | dot product | none | none |