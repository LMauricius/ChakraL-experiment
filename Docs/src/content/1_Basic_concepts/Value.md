# Value

## Definition
A value is a handle that can be used to access a context and modify functions that map from it. It consists of 2 components: the data, and the required trait.

## What are values?

The values can be named constants, variables that can be changed during the program's runtime, literals that are explicitly written in the code and used once etc. Here are few short examples that will be better explained later in the documentation:

`3.141592` is a numeric value, `"Hello world"` is a textual value.

```
a = b + c
```
...`a`, `b` and `c` are variable values

```
t = "Hello World!"
n = 3
```
...`"Hello World!"` and `3` are literal values, while `t` and `n` are variable values.

```
PI def 3.141592
```
...`PI` is a constant value defined to be equal to the literal value `3.141592`


## The data
The data is the context that can be used in functions, assigned to other values and that can be modified if the value isn't a constant.

## The trait
The trait of a value is the one that the data must satisfy. It is used to restrict the kinds of data that can be assigned to a value and keep the programmer's sanity. The trait can be specified manually, or inferred from another value whose data is assigned to it.

The trait can be manually specified. For example we can specify variable value `a` to have a trait of `Positive & Integer` (`&` combines multiple traits into one):
```
a: Integer & Positive = 3
```

The trait can also be automatically inferred during the first use of a value. In the example:
```
a = 3
```
... `a`'s trait will be inferred to be an `int32` (a 32-bit signed `Integer` trait), as the integer literals' trait is `int32`.

We chose 32-bit integers as the default because they are a good compromise between the range of numbers (-2_147_483_647 to 2_147_483_647) and the memory taken (4 bytes). Literals that are outside that range will be stored as the smallest native `Integer` type that fits them. For example:
```
a = 3 # 3 is int32, a is inferred to be int32
a = -60_000_000_000 # -60_000_000_000 is int64, a is still defined as int32
# the program raises an ERROR: 
# -60_000_000_000 cannot be cast to int32 as it is outside the range of int32
```

## Satisfying the trait
The data always satisfies the trait. If the trait is declared with an `explicit` keyword, it will only be satisfied if the data is actually declared to be that type; if not, it will also be satisfied if the data is similar to the trait (it has the same members, it is composed of the same sub-contexts). For more details see the chapter [Trait system](trait_system.html). 

An example of not satisfying the trait (we use assignment operator instead of change, because the change operator can implicitly convert values to the desired trait):
```chakral
a : int32 <- new 3 # assignment (<-) instead of change (=)
a <- new "Hello world" # ERROR: string is not an int32
```



## Similar ideas in other languages
variable, constant, literal, pointer, temporary value, rvalue, lvalue