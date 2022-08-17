# Value

## Definition
A value is a handle that can be used to access a context and modify functions that map from it. It consists of 3 components: the data, the required trait and the known trait.

## The data
The data is the context that the functions map from and that can be modified if the value isn't a constant.

## The required trait
The required trait of a value is the one that the data has to always satisfy. It is used to restrict the kinds of data that can be assigned to a value and keep the programmer's sanity. The required trait can be specified manually, or infered from another value whose data is assigned to it.

The required trait can be manually specified. For example we can specify variable value `a` to have a required type of `Positive Integer`:
```
a: Integer & Positive = 3
```

The required trait can also be automatically inferred during the first use of a value. In the example:
```
a = 3
```
... `a`'s required trait will be inferred to just be an `Integer`, as the integer literals' required trait is `Integer`.

## The known trait
The known trait is the more specific trait that the data always satisfies. It is used internally by the compiler for performance optimizations and hidden from the programmer. The known trait is implementation-specific, but always satisfies the required trait.

## The difference between data, the required trait and the known trait
The differences can be shown in the example of an integer literal `3`. The data is exactly `3`, its required trait is an `Integer`, but the known trait could be an `Unsigned Integer`. If we assign `3` to a newly declared variable value `a` without specifying a trait manually like this:

```
a = 3
```
... `a`'s required trait will also be an `Integer`, but the known trait could be an `Nonnegative & int32` (as the literal `3` can be stored as a 32-bit integer) unless it gets a `Negative Integer` assigned to it somewhere in code for example. If we have the following code snippet later:
```
a = -2
```
... `a`'s known trait couldn't be an `Unsigned & int32`, but perhaps only an `int32`. It's data would be `3` before its reassignment of `-2`.


## Similar structures in other languages
variable, constant, literal, pointer, temporary value, rvalue, lvalue