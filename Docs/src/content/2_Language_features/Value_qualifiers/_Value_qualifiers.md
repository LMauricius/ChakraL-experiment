# Value qualifiers

## Introduction
Value qualifiers modify the way values can be accessed and used. Some prevent the user from changing the data when it's not desirable, while others allow the user to share a data context in multiple parts of the program. 

## Usage
The value qualifiers are written after the required trait of a member declaration. The required trait can still be ommited and automatically inferred, as value qualifiers are a separate concept from the required trait.
```{caption="Usage"}
MEMBER_NAME : REQUIRED_TRAIT VALUE_QUALIFIERS = STARTING_VALUE 
```

```{.chakral caption="Example"}
read, write with stream = console std:

    maxNumEntries: Int32 const = 100

    write "Enter how many numbers to add:"
    numEntries: Int32 const = Read Int32

    if numEntries > maxNumEntries:
        write(
            stream = errConsole std,
            "Can't add more than "+Str(maxNumEntries)+" entries!"
        )
    else:
        sum: Float64 mutable = 0.0

        repeat numEntries times:
            write "Enter a number:"
            a = read Float64
            sum += a
        ok

        write "The sum is " + Str(sum) + "!"
    ok

ok  
```

## Supported qualifiers
Below is a table of all properties that qualifiers modify, along with the qualifier keywords and default settings.

| Property  | States | Qualifier keywords | Default |
| --------- | ------ | ------------------ | ------- |
| [Ownership](ownership.html) | owner, reference, constant | `own`, `ref`, `const` | owner (`own`) |
| [Data mutability](mutability.html) | volatile, mutable, immutable, virtual | `volatile`, `immutable`, `mutable`, `virtual` | immutable |
| [Evaluation time](evaluation_time.html) | static, runtime | `static` | runtime |
| [Scope](scope.html) | broad, niche | `from (...)` | broad |
| [Target](target.html) | local, leaving | `leaving to (...)` | local |

More details can be found on each property's chapter.

A value with explicitly declared default qualifiers would be:  
```{.chakral}
x: immutable own = 1
```