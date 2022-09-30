# Trait system

## Purpose
The trait system is useful in several ways. It allows the programmer to limit themself and prevent errors caused by improper use of data. It simultaneously tells the compiler how we are going to use the data, which allows it to optimize the machine code for that specific usage, causing the resulting program to run faster. As the trait system is quite *explicit* (without necessarily being *verbose*), this also allows other programmers who read our code to know what we intended to do with the data.

## Satisfying the trait
If the context `c` satisfies the trait `t` we say that `c is t`{.chakral}. That satisfaction depends on `c` and `t`'s descriptions and specifiers. How the descriptions and specifiers are satisfied is described below.

## The specifiers
The specifiers change how the satisfaction is interpreted. They are useful to limit the contexts that satisfy the trait.

### final specifier
```{.chakral caption="Example of the difference between final and non-final traits"}
Killable def:
    health: Real = 100.0
ok

Dead def:
    final health: Real = 0.0
ok

p = Killable
with output = console:
    write p **prints '(health = 100.0)'
    write whether p is Killable **prints 'true'
    write whether p is Dead **prints 'false'
ok

health p -= 100.0
with output = console:
    write p **prints '(health = 0.0)'
    write whether p is Killable **prints 'true'
    write whether p is Dead **prints 'true'
ok
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