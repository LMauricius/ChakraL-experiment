# module keyword

## Description
The `module` keyword is used to retrieve the whole context of a module. We can use it to access values from other modules. The module can be installed in the global module path, or be a sub-module of the module which the code is part of.

## Usage
The `module` keyword is most commonly used along with the `using` keyword described in the next chapter.

Use: `module MODULE_NAME`

Example: `module MyMath`
More useful example:
```
mySineFunc def sin(module Math)
amp = mySineFunc(30°)
```
More complex but conscise example: `amp = (sin(module Math))(30°)`

You can also retrieve the submodules with the keyword.
Use: `module MODULE_NAME.SUBMODULE_NAME1.SUBMODULE_NAME2.<...>`

Example: `module MyEngine.Physics`