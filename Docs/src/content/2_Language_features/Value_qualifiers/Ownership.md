# Ownership
Data can have a single owner value, but many references. The ownership property of a value is modified by the `own`, `ref` and `const` keywords.

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
        **start of 'a' variable's lifespan
        a = starting **takes ownership from 'starting'

        sum: mutable = 0

        while a != 0:
            sum += a **adds entered number to the sum
            print sum
            a = read Integer **reads next number
        ok

        **ERROR: using an unitialized value ('a' could still own the data)
        **(Uncomment the line below to see the error)
        **write starting

        **end of 'a' variable's lifespan
    ok

    **OK: 'starting' has its ownership returned
    write starting

    **end of 'starting' variable's lifespan
ok  
```

Assigning a constant or a static value (such as a definition) to an owner value implicitly creates a copy of it instead of changing its ownership.

```{.chakral caption="Constant copy example"}
read, write with stream = console stl:

    PI def 3.141592

    p = PI

    write p **'p' can be used
    write PI **'PI' can still be used 

ok  
```

## Reference
References can be used to access data without taking its ownership. 

```{.chakral caption="Reference example"}
read, write with stream = console stl:

    a = read Integer
    b = read Integer
    greater: ref

    if a > b:
        greater = a
    else:
        greater = b
    ok

    **'greater' is assigned to the data of either 'a' or 'b',
    **but 'a' and 'b' can still be used as they retain their ownership
    write Str(greater)+" is greater between "+Str(a)+" and "+Str(b)

ok  
```

The references cannot be directly mutated. If the reference isn't mutable, you have to create a copy of it and assign it to a mutable owner value to use the data in a mutable way. If the reference is mutable, it can be borrowed by a mutable owner value.

If data is borrowed of an owner value that has possible references, all possible references to it will be uninitialized along with it during the borrowing process. If a reference's data is borrowed, any possible original owner of reference's data will be unitialized during the borrowing process, along with all other possible references to them.

## Constant
A *constant* is a special kind of owner value. It is also a 'main' value of its data, but it's ownership cannot be taken after being assigned with data, and it doesn't take ownership from a value during its assignment. Instead, assigning it with data of another *non-const* value implicitly creates a copy of it, just as assigning its data to another *owner* value. References can be assigned with constant value's data.

```{.chakral caption="Constant example"}
globalSettings: const = Config(Open.File."settings.json", Json ConfigFileType)
appSettings: const = globalSettings
currentSettings: ref = appSettings

**'globalSettings' and 'appSettings' are both initialized and valid
**'currentSettings' is assigned with 'appSettings''s data
```