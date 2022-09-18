# Language goals

ChakraL is developed with love towards both the programmer and the end-user. Here is the list of goals that the author believes will help make the language better.

## Semantics are important
The end-goal of the programmer should always be obvious. Writing code should be focused on telling the copmuter what you want to happen, instead of how, and the code shouldn't only make sense after reading thousands of lines. We are writing *programming* code, not cryptic gibberish. Common functionality especially shouldn't require writing hackish boilerplate code, but should be short and readable. 

## Keep things consistent
If an existing way of doing things can be extended with new functionality, it should be, instead of designing new features from the ground up. On the other hand, the language features shouldn't be bent backwards to incorporate radically different ideas. The language structures should convey meaning intuitive to most people, and shouldn't be used for unrelated things. For example, the brackets are *only* used to construct list literals.

## Interoperability with other languages
The language shouldn't require a huge ecosystem built specifically for it, but should be an interface to language-agnostic specifications. Existing libraries should be usable from the language and their API structure should be adapted while applying the ChakraL's coding practices if possible. This requires a well-defined ABI per each platform.

## Fast execution
The features must require the least overhead possible. Faster code shouldn't be gatekeeped as a harder or less safe skill, but there should still be ways to avoid slower constructs without breaking the higher priority goals. Accessibility and speed/power aren't mutually exclusive.

## Build advanced features from basic building blocks
The basic language features should be designed in such a way that they can be used in the most use-cases. This makes the language more abstract, while simultaneously easier to understand.

## Reduce the amount of work for the programmer
Even if you consider the programmer a wizard, their work and time aren't zero-cost. We don't expect the programmers to repeat work that can be done once and then shared. The amount of work needed should always be reduced at the lowest level possible without restricting what can be done with the language.

## 