cmake_minimum_required(VERSION 3.0.0)

# Files
file(
    GLOB_RECURSE
    SOURCES
    "./src/*.h"
    "./src/*.cpp"
)


######################################
# Setup target
######################################
add_executable(ChakraLC ${SOURCES})
set_target_properties(ChakraLC PROPERTIES OUTPUT_NAME "chakral${OUTPUT_FILE_SUFFIX}")
target_include_directories(ChakraLC PRIVATE "./include")

add_dependencies(ChakraLC libChakraL)
target_include_directories(ChakraLC PRIVATE "../libChakraL/include" "../libChakraL/ctre")
target_link_directories(ChakraLC PRIVATE "../bin" "../lib")
target_link_libraries(ChakraLC PUBLIC "ChakraL${OUTPUT_FILE_SUFFIX}")

# build config
if (CHAKRAL_STATIC_LIB)
	target_compile_definitions(ChakraLC PUBLIC CHAKRAL_STATIC_LIB)
endif()