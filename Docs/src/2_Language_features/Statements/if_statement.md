# *if* statement

## Description
The *if* statement is used for conditional execution. The context is executed only if the condition is true. Optionally, an alternative context can be specified along with multiple alternative conditions.

## Usage
Write:
```
if CONDITION:
    CONTEXT_TO_EXECUTE
ok
```

With an alternative:
```
if CONDITION:
    CONTEXT_TO_EXECUTE
else
    ALTERNATIVE_CONTEXT_TO_EXECUTE
ok
```

With multiple conditions:
```
if CONDITION1:
    CONTEXT_TO_EXECUTE1
elif CONDITION2:
    CONTEXT_TO_EXECUTE2
elif CONDITION3:
    CONTEXT_TO_EXECUTE3
<...>
else
    ALTERNATIVE_CONTEXT_TO_EXECUTE
ok
```

## Examples

### Basic examples

```
if a < b:
    write "a is less than b"
elif a > b:
    write "a is greater than b"
else
    write "a is equal to b"
ok
```

```
if score > recordscore:
    recordscore = score
ok
```