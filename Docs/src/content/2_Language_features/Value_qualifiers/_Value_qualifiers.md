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
| [Ownership](ownership.html). | owner, reference, constant | `own` `ref` `const` | owner (`own`) |
| [Data mutability](mutability.html) | mutable, immutable | `mutable` | immutable |
| [Volatility](volatility.html) | volatile, non volatile | `volatile` | non volatile |
| [Virtuality](virtuality.html) | virtual, non virtual | `virtual` | non virtual |
| [Static](static.html) | static, non static | `static` | non static |
| [Origin](origin.html) | unspecialized, specialized | `from ...` | unspecialized |
| [Leaving target](target.html) | not leaving, leaving | `leav to ...` | not leaving |

More details can be found on each property's chapter.