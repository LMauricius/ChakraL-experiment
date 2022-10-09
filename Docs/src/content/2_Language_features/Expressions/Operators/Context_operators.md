# Context operators


## Context combination (&) operator
```{.chakral}
C = A & B
```

Combines two operand contexts `A` and `B` into one result context `C`. `C` will have all descriptions of `A` and `B`. 

If a member of the same name is found in both operands `A` and `B`, the result context `C` will have one member of that name with the required type of the left operand `A` and the starting assigned data of the right operand `B`. In that case, `B`'s member value must satisfy the required trait of `A`'s member value and `B`'s member value's access specifiers must be the same as' `A`'s member value's access specifiers. In such a situation we say that `A`'s member value was overriden by `B`'s.

```{.chakral caption="Example of combination"}
A def:
    a = 1
    b = 2
ok

B def:
    b = 3
    c = 4
ok

C def A & B

with output=console:
    write C **prints '(a = 1, b = 3, c = 4)'
ok
```

```{.chakral caption="Example of wrong data"}
A def:
    a = 1
    b = 2
ok

B def:
    b = "Hello"
    c = 4
ok

C def A & B ** ERROR: String is not Integer for override of member 'b'
```

A context `d` satisfied the combination result trait `C` if and only if it satisfies all the operand contexts that are part of `C`.

```{.chakral caption="Example of a combined trait"}
NonZero def:
    ? context != 0
ok

NonZero32 def int32 & NonZero

with output=console:
    a: int32 = 0
    b: float64 = 3.0
    c: int32 = 3

    write whether a is int32 **prints 'true'
    write whether a is NonZero **prints 'false'
    write whether a is NonZero32 **prints 'false'
    write whether b is int32 **prints 'false'
    write whether b is NonZero **prints 'true'
    write whether b is NonZero32 **prints 'false'
    write whether c is int32 **prints 'true'
    write whether c is NonZero **prints 'true'
    write whether c is NonZero32 **prints 'true'
ok
```

The [trait specifiers](trait_system.html) of the operands `A` and `B` do not carry over into the combined context, but they do apply on the operands as parts of the result context `c`.

```{.chakral caption="Example of the final specifier in a combined trait"}
A def:
    x = 0
ok
B def:
    final
    y = 0
ok
C def A & B

with output=console:
    d1 = (x = 0, y = 5)
    d2 = (x = 5, y = 0)
    write whether d1 is C **prints 'false'
    write whether d2 is C **prints 'true'
ok
```

## Context selection (|) operator

## Context choice (<>) operator