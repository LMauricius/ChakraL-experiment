# Trait system

## Purpose
The trait system is useful in several ways. It allows the programmer to limit themself and prevent errors caused by improper use of data. It simultaneously tells the compiler how we are going to use the data, which allows it to optimize the machine code for that specific usage, causing the resulting program to run faster. As the trait system is quite *explicit* (without necessarily being *verbose*), this also allows other programmers who read our code to know what we intended to do with the data.

## Satisfying the trait
If the context `c` satisfies the trait `t` we say that `c is t`{.chakral}. That satisfaction depends on `c` and `t`'s descriptions and specifiers. How the descriptions and specifiers are satisfied is described below.

## Trait specifiers
Trait specifiers change how the satisfaction is interpreted in addition to the descriptions. They can be used as descriptions or like prefix functions.

```{.chakral caption="Example of a final trait specifier"}
** like description of a block context:
A def:
    final
    a = 1
ok
** like description of an expression context:
B def (final, b = 2)

** like a prefix function:
C def final (c = 3)
```

### final specifier
If the trait `t` has a `final`{.chakral} specifier, then it will only be satisfied if `c` is either equal to `t` or hasn't been changed since being created as a copy of `t`. If a final trait `t` is used as a required trait of value `v`, `v` cannot be changed, just like if `v` was a constant value. Unlike constant values, a final value cannot be overriden by another value. Using a final value in an operation that could change or override it is forbidden, even if `v`'s data wouldn't be changed by the operation (i.e. `v` would still satisfy its required trait *after* the operation).

A final trait `t` can be used as a required trait for value `v` only if `v` is a constant value. Note that `final`{.chakral} is a trait specifier while `const`{.chakral} is a value specifier.

```{.chakral caption="Example of the difference between final and non-final traits"}
** A context is Killable if it has a Real value health and Integer value lives
** (no matter those values' data)
Killable def:
    health = 100.0 **100.0 is the starting value for copies
    lives = 1 **1 is the starting value for copies
ok

** A context is Dead if its health and lives are equal to 0
Dead def:
    final
    health = 0.0
    lives = 0
ok

p = Killable
with output = console:
    write p **prints '(health = 100.0, lives = 1)'
    write whether p is Killable **prints 'true'
    write whether p is Dead **prints 'false'
ok

health p -= 100.0
lives p -= 1
with output = console:
    write p **prints '(health = 0.0, lives = 0)'
    write whether p is Killable **prints 'true'
    write whether p is Dead **prints 'true'
ok
```

```{.chakral caption="Example of the difference between a definition and a final valued member"}
Player def:
    health: Real = 100.0  **member variable
    strength def 0.0      **member definition
    weaponName def "none" **member definition
ok

Swordsman def:
    !Player               **includes Player trait
    strength def 120.0    **member redefinition
    weaponName def final "sword" **
ok

p1 = Player & (
    strength def 100.0,
    weaponName def "sword"
)
p2 = Player & (
    strength def 120.0,
    weaponName def "lance"
)
with output = console:
    write p1 **prints '(health=100.0, strength=100.0, weaponName="sword")'
    write whether p1 is Player **prints 'true'
    write whether p1 is Swordsman **prints 'true'
    write p2 **prints '(health=100.0, strength=120.0, weaponName="lance")'
    write whether p2 is Player **prints 'true'
    write whether p2 is Swordsman **prints 'false'
ok
```

```{.chakral caption="Limitations of const and final values"}
ConstZeroOwner def:
    number: const = 0
ok
FinalZeroOwner def:
    final
    number = 0
ok

a = ConstZeroOwner
b = FinalZeroOwner

number a = 100 **ERROR - can't change const value
number b = 100 **ERROR - can't change final value
c = a & (number: const = 100) **OK - can override const value
d = b & (final, number = 100) **ERROR - can't override final value
```

### explicit specifier
If the trait `t` has an `explicit`{.chakral} specifier, then it will only be satisfied if `c` was created as a copy of `t`. This requires the code that creates the context to epxlicitly want us to use `c` as `t`. If a value's trait is manually specified to be `t`, and we try to assign it a context `c2` that is not `t`, `c2` will be *cast* (reinterpreted, if possible) to `t`.

```{.chakral caption="Example of the difference between explicit and non-explicit traits"}
Player def:
    explicit
    lives = 3
    score = 0
ok

PlayerLike def:
    lives = 3
    score = 0
ok

p1 = Player **copies the constant 'Player' into a non-constant context
p2 = (lives = 3, score = 0)
p3: Player = (lives = 3, score = 0)
 
with output = console:
    write whether p1 is Player **prints 'true'
    write whether p2 is Player **prints 'false'
    write whether p3 is Player **prints 'true'
    write whether p1 is PlayerLike **prints 'true'
    write whether p2 is PlayerLike **prints 'true'
    write whether p3 is PlayerLike **prints 'true'
ok
```