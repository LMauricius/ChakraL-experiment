# *with* statement

## Description

The *with* statement is used for shared argument insertion. It is a shortcut for preventing writing same expressions many times which reduces visual noise. Making the code look cleaner without making the behavior less explicit, it allows both the code writer and reader to spend mental energy on problem solving rather than understanding the code.

```{.chakral caption="Example"}
**this:
write(output=console, "Hello world!")
write(output=console, "How's it going?")

**has the same behavior to this:
write with output=console:
    write "Hello world!"
    write "How's it going?"
ok
```

## Usage
```{caption="Usage"}
FUNCTION1, FUNCTION2 <...> with DESCRIPTION1, DESCRIPTION2 <...>:
    CONTEXT_TO_EXECUTE
ok
```

## Behaviour
For each call of an affected function, the context composed of descriptions in the statement is combined (on the left side of an `&` operator) with the argument of the function call.

This:
```{.chakral}
write with output=console:
    write "Hello world!"
    write "How's it going?"
ok
```
...is same as:
```{.chakral}
write with output=console:
    write ("Hello world!")
    write ("How's it going?")
ok
```
...which is same as:
```{.chakral}
write (output=console) & ("Hello world!")
write (output=console) & ("How's it going?")
```
...which is same as:
```{.chakral}
write (output=console, "Hello world!")
write (output=console, "How's it going?")
```
...which is (due to implicit conversion of unnamed arguments) same as:
```{.chakral}
write (output=console, msg="Hello world!")
write (output=console, msg="How's it going?")
```