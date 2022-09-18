# File format

Here are described the file formats, folder structures and conventions used in ChakraL.

## File naming

The file names must start with a letter and can contain leters, digits and underscores. Double underscores are forbidden. If the file has multiple extensions (separated by multiple dots), all but the last extension will be ignored.

## File extensions

| File type | Extension |
| --------- | --------- |
| Source file | `ckr` |
| Module interface file | `ckri` |

### Source files
The source files are the ones containing the ChakraL code. They get compiled into a *binary file*, which can be either an *executable* or a *library*. Multiple source files can be used to compile a single binary file. If the binary we are compiling is a library meant to be used by other developers, the source files can also produce *module interface files* which simplify the loading of library symbols without showing the full source code to others.

## Text file format

The source files should always be saved using the `UTF-8` encoding. Other formats might not be recognized or read properly by the compiler. Most modern text editors use `UTF-8` by default.