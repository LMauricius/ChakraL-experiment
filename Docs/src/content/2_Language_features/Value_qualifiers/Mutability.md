# Mutability
Data mutability refers to whether data assigned to a value can itself be mutated, instead of reassigning the value with a different data. Several actions are considered data mutations:

- Reassigning its member values with new data
- Borrowing its data to another mutable value
- Mutating any of its member values.

Reassigning a value itself is **not** considered a mutation of its data.

# Mutable
Mutable data is allowed to be mutated, although only by its owner. Mutations are useful when you want to change only a part of the data, or when you want to change borrowed data before returning its ownership. Such values' data can be borrowed by values qualified as either `mutable`, `volatile` or `immutable`.

Mutable data values are treated differently when used as function parameter members. Each parameter member that is qualified as `mutable` requires the function to have an equivalent `mutable` member of its return value. If the function's return value trait is ommited, the automatically inferred return value trait will have all neccesary `mutable` members automatically added. If the function only has its `mutable` parameters as the return trait, the `return`{.chakral} statement can be used without a value and `mutable` parameter members will be automatically added to it. In such case, the `return`{.chakral} statement can also be ommited at the end of a function.

# Immutable
Immutable data is, as the name implies, forbidden from being mutated. Such values' data can be borrowed only by other values qualified as `immutable`. This is the default for all values.

# Volatile
Volatile data refers to unstable values, that can be changed in non-obvious ways. It can be mutated, even if its owner's context is qualified as immutable. This is useful for data that depends on system processes, and data that is shared between multiple threads. Such values' data can be borrowed by values qualified as either `mutable`, `volatile` or `immutable`.

# Virtual
Virtual data is different from other data because it can only be referenced or borrowed by other values qualified as `virtual`. Virtual data can be incomplete, as its members can be uninitialized. If data is virtual, it cannot be copied.

As most functions take non-`virtual` data as arguments, `virtual` data is usually only useful as a 'prototype' that can be used to construct non-`virtual` data. This is done by *combining* some data with the `virtual` data, and ensuring the combined data *completes* each other (otherwise the result would have more initialized members than the original `virtual` data, but still be incomplete i.e. still `virtual`).

Most often, `virtual` data is used as trait. Traits can be used to test data (using the `is` operator), limit values (using required traits), as *prototypes* (to construct non-`virtual` data by operator `&`), or for casting to a new object (using the cast operator `.`).