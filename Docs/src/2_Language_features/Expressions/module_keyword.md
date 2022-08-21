# module keyword

## Description
The `module` keyword is used to retrieve the whole context of a module. We can use it to access values from other modules. The module can be installed in the global module path, or be a sub-module of the module which the code is part of.

## Basic usage
The `module` keyword is most commonly used along with the `using` keyword described in the next chapter.

Write: `module MODULE_NAME`
`module MODULE_NAME` is a prefix expression, so to use it in a more complex expression, you have to surround it with parentheses. 

Example: `module MyMath`
Complex example: `sin (module MyMath)`
More useful example:
```
mySineFunc def sin(module MyMath)
amp = mySineFunc 30°
```
Harder to read but conscise example: `amp = (sin(module MyMath)) 30°`

## Submodules usage
You can also retrieve the submodules with the keyword.
Write: `module MODULE_NAME.SUBMODULE_NAME1.SUBMODULE_NAME2.<...>`

Example: `module MyEngine.Physics`