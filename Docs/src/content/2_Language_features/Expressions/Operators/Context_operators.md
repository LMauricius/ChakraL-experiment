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
```{.chakral}
C: virtual = A | B
```

Makes a selection between two operand contexts `A` and `B` as a result context `C`. `C` will have those descriptions that are part of both `A` and `B`. A context `d` satisfies the selection result trait `C` if and only if it satisfies at least one of the operands that are part of `C`. Because of that, `d` that is of trait `C` can be cast into at least one of its operands `A` or `B`.
```{.chakral}
XY def (x=1, y=2)
YZ def (y=2, z=3)
c: XY | YZ = (x=4, y=5) **assigns an XY value

with output=console:
    write y c **prints '5'
    **write x c **would be ERROR: selection c doesn't always have the member x

    ** how to access 'x':
    if c is XY: **yes
        using c as XY **cast from XY|YZ to XY
        write x c **prints '4'
```

The `new`{.chakral} operator isn't automatically defined for a selection since there is not universal default for which operands should be included in the copy. A selection is usually only useful as a required trait as it cannot be instantiated by default. It is however a `virtual`{.chakral} context, so it can be assigned to values that have a virtual specifier.
```{.chakral}
c = (x=1) | (y=2) **ERROR: cannot copy a selection into variable 'c'
d: virtual const = (x=1) | (y=2) **OK
```

## Context choice (<>) operator