# Mutability
Data mutability refers to whether data assigned to a value can itself be mutated, instead of reassigning the value with a different data. Several actions are considered data mutations:

- Reassigning its member values with new data
- Borrowing its data to another mutable value
- Mutating any of its member values.

Reassigning a value itself is **not** considered a mutation of its data.