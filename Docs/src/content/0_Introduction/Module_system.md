# Module system

## Modules
The ChakraL code is organized into objects called modules. The modules are a way to separate the code in meaningful units, just like a book is separated into chapters. For example, we can have a math module, a 3D graphics module and a physics engine module. In addition, finished modules can easily be distributed to other programmers without requiring them to copy-paste code into their projects. The code specifies which modules it uses, which makes its dependencies clearer.

## Module directory structure
Source files are organized in directories corresponding to modules. The module directories are located in one of the source locations specified to the compiler. The files inside a directory can be thought of as parts of one whole file describing a single module. It's useful to separate the module into several (many) files by its different functionalities to make editing the code easier.

If we have the following directory structure inside the source directory:
```
MathModule/
    BasicOperationsFile.ckr
    SetOperationsFile.ckr
PhysicsModule/
    ShapesFile.ckr
    ForcesFile.ckr
    SimulationManagementFile.ckr
```
The compiler will build 2 modules : `MathModule` and `PhysicsModule`.

## Compiled modules
Each module gets compiled into a *binary* file. The binary file can be an *executable*, or a *library* used by other binary files. The libraries are used to distribute existing functionalities to other developers and executables can be launched by users to perform tasks. In ChakraL, libraries come with *module interface files* which describe which functionalities the module has that are stored in the library. In the above scenario, we would have the following interface files after installing the modules on the developer's system:
```
MathModule/
    BasicOperationsFile.ckri
    SetOperationsFile.ckri
PhysicsModule/
    ShapesFile.ckri
    ForcesFile.ckri
    SimulationManagementFile.ckri
```
Additionally, we could have the following library files stored in the system's library directory:
```
MathModule.lib
PhysicsModule.lib
```

A module would work the same if all its interface files were converted into a single file, but they are separated to make reading them easier.