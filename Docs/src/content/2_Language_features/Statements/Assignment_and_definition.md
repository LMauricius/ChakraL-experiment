# Assignment and definition

## Introduction
Assignments are used to change the data that is stored in a value. 

## Reassignment

To change the data stored in a member value the syntax is as follows:
```{caption="Usage"}
MEMBER_NAME = NEW_VALUE 
```

After the reassignment the member's data will be set to `NEW_VALUE`'s data.

Before assigning a member you have to declare it. More can be found on the [context page](context.html#Member_declaration)

The full declaration syntax is as follows:
```{caption="Usage"}
MEMBER_NAME : REQUIRED_TRAIT VALUE_QUALIFIERS = STARTING_VALUE 
```

## Overload reassignment
An existing member can be redeclared as an overload using the `<+>=` symbol:
```{caption="Definition declaration"}
OVERLOADED_MEMBER_NAME : REQUIRED_TRAIT VALUE_QUALIFIERS <+>= OVERLOAD_VALUE 
```

The member will be redeclared as an overloaded context of its old value(s) along with the new `OVERLOAD_VALUE` as its overloads.

## Definition

A definition is a shorthand for a member declaration with a `const`{.chakral}, `static`{.chakral} and optionally `virtual`{.chakral} value qualifiers. The syntax is as follows:
```{caption="Usage"}
MEMBER_NAME def STARTING_VALUE 
```

This is equal to writing:
```{caption="Definition declaration"}
MEMBER_NAME : const static virtual? = STARTING_VALUE 
```

## Overload definition
The overload reassignment and definitions can be combined with the `odef`{.chakral} keyword.
```{caption="Usage"}
MEMBER_NAME odef STARTING_VALUE 
```