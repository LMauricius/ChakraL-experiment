# Ownership
While the data context can have many references, it can only have a single owner value. It is modified by the `own` and `ref` keywords

## Owner
The owner can be seen as a 'main' variable of some data. When data is assigned to an owner value, the new owner *takes* the ownership from the old one. That makes the old value *uninitialized*, which means it can't be used in an expression until it gets assigned with new data.

```{.chakral caption="Ownership reassignment example"}
read, write with stream = console stl:

    a: own = 30
    write a **prints '30'

    b: own = a
    write b **prints '30'

    **ERROR: using an unitialized value
    **(Uncomment the line below to see the error)
    **write a

    a = 50
    **OK: 'a' has been assigned with new data
    write a **prints '50'

ok  
```

As *owner* is the default value qualifier, the `own`{.chakral} qualifier can be ommited.

```{.chakral caption="Default qualifiers example"}
a: own = 30
b = 30
**'a' and 'b' have the same qualifiers
```

```{.chakral caption="Ownership reassignment example (without manual qualifiers)"}
read, write with stream = console stl:

    a = 30
    write a **prints '30'

    b = a
    write b **prints '30'

    **ERROR: using an unitialized value
    **(Uncomment the line below to see the error)
    **write a

    a = 50
    **OK: 'a' has been assigned with new data
    write a **prints '50'

ok  
```

If the new owner value has a shorter lifespan than the old one, it will take the ownership only *temporarily*. Such temporary ownership is called *borrowing*. The data is borrowed until its new value's lifespan ends, and then its ownership gets returned to the first old owner who is still alive.

```{.chakral caption="Ownership borrowing example"}
read, write with stream = console stl:
    **The program reads a starting integer.
    **If the starting integer is positive, then it continues reading integers
    **until '0' is entered. It sums all integers and prints the sum after each
    **number is entered. After '0' is entered, it prints the starting number.

    **start of 'starting' variable's lifespan
    starting = read Integer
    write starting

    if starting > 0:
        **start of 'sum' variable's lifespan
        sum = starting **takes ownership from 'starting'

        a = read Integer
        while a != 0:
            sum += a **adds entered number to the sum
            print sum
            a = read Integer **reads next number
        ok

        **ERROR: using an unitialized value ('sum' could still own the data)
        **(Uncomment the line below to see the error)
        **write starting

        **end of 'sum' variable's lifespan
    ok

    **OK: 'starting' has its ownership returned
    write starting

    **end of 'starting' variable's lifespan
ok  
```