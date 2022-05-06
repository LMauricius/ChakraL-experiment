cmake_minimum_required(VERSION 3.0.0)

######################################
# Cache variables
######################################

set(ParserType "lr" CACHE STRING "The parsing algorithm to use")
set_property(CACHE ParserType PROPERTY STRINGS "custom" "lr" "recursive")

if(ParserType STREQUAL "custom")
	set(ParserTypeSuffix "Custom")
elseif(ParserType STREQUAL "lr")
	set(ParserTypeSuffix "LR")
elseif(ParserType STREQUAL "recursive")
	set(ParserTypeSuffix "Recursive")
endif()

######################################
# Setup generator
######################################

find_package( PythonInterp 3.0 REQUIRED )

add_custom_command(
	OUTPUT
		${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralLexerAutogen.h
		${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralLexerAutogen.cpp
	COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/generators/generator.py
		--inlexer ${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/lexer.txt
		--outlexerh ${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralLexerAutogen.h
		--outlexercpp ${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralLexerAutogen.cpp
	DEPENDS
		${CMAKE_CURRENT_SOURCE_DIR}/generators/generator.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/genUtil.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/lexerGen.py
		${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/lexer.txt
	COMMENT "Generating lexer files"
)

add_custom_command(
	OUTPUT
		${CMAKE_CURRENT_SOURCE_DIR}/autosyntaxdef/operatorProductionsAutogen.txt
	COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/generators/generator.py
		--inoperators ${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/operatorTable.txt
		--outoperators ${CMAKE_CURRENT_SOURCE_DIR}/autosyntaxdef/operatorProductionsAutogen.txt
	DEPENDS
		${CMAKE_CURRENT_SOURCE_DIR}/generators/generator.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/genUtil.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/operatorProdGen.py
		${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/operatorTable.txt
	COMMENT "Generating operator table file"
)

add_custom_command(
	OUTPUT
		${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralParserAutogen.h
		${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralSemanticNodesAutogen.h
		${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralParserAutogen.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralSemanticNodesHybridgen.cpp
	COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/generators/generator.py
		--inlexer ${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/lexer.txt
		--insemanticnodes ${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/semanticNodes.txt
		--inparser ${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/parser.txt
		--inlexerh ${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralLexerAutogen.h
		--outparserh ${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralParserAutogen.h
		--outparsercpp ${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralParserAutogen.cpp
		--extraparserheaders ${CMAKE_CURRENT_SOURCE_DIR}/include/chakralParserPrereq${ParserTypeSuffix}.h ${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralSemanticNodesAutogen.h
		--outsemanticnodesh ${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralSemanticNodesAutogen.h
		--outsemanticnodescpp ${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralSemanticNodesHybridgen.cpp
		--extrasemanticnodesheaders ${CMAKE_CURRENT_SOURCE_DIR}/include/chakralParserPrereq${ParserTypeSuffix}.h
		--parsertype ${ParserType}
	DEPENDS
		${CMAKE_CURRENT_SOURCE_DIR}/generators/generator.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/genUtil.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/parserGenShared.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/parserGen${ParserTypeSuffix}.py
		${CMAKE_CURRENT_SOURCE_DIR}/generators/semanticMethodGen.py
		${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/parser.txt
		${CMAKE_CURRENT_SOURCE_DIR}/syntaxdef/semanticNodes.txt
		${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralLexerAutogen.h
		${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralLexerAutogen.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/autosyntaxdef/operatorProductionsAutogen.txt
	COMMENT "Generating parser files"
)

add_custom_target(
	generate ALL
	DEPENDS
		${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralLexerAutogen.h
		${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralLexerAutogen.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralParserAutogen.h
		${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralParserAutogen.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/autoinclude/chakralSemanticNodesAutogen.h
		${CMAKE_CURRENT_SOURCE_DIR}/autosrc/chakralSemanticNodesHybridgen.cpp
)

######################################
# Setup ctre
######################################

#add_subdirectory("./compile-time-regular-expressions")

######################################
# Setup target
######################################

# Files
file(
	GLOB_RECURSE
	SOURCES
	CONFIGURE_DEPENDS 
	"./include/*.h"
	"./autoinclude/*.h"
	"./src/*.cpp"
	"./autosrc/*.cpp"
)
file(
	GLOB
	HEADERS
	"./include/*"
	"./autoinclude/*.h"
)

add_library(libChakraL ${CHAKRAL_LIB_TYPE} ${SOURCES})
set_target_properties(libChakraL PROPERTIES OUTPUT_NAME "ChakraL${OUTPUT_FILE_SUFFIX}")
target_include_directories(libChakraL PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR}/ctre)
#target_include_directories(libChakraL PUBLIC "./include" "./compile-time-regular-expressions/include")
set_property(TARGET libChakraL PROPERTY CXX_STANDARD 20)
target_compile_definitions(libChakraL PRIVATE CHAKRAL_PARSER_TYPE_${ParserTypeSuffix})

add_dependencies(libChakraL generate)
#add_dependencies(libChakraL ctre)

# build config
if (CHAKRAL_STATIC_LIB)
	target_compile_definitions(libChakraL PUBLIC CHAKRAL_STATIC_LIB)
endif()
target_compile_definitions(libChakraL PRIVATE CHAKRAL_BUILD)