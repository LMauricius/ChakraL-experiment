cmake_minimum_required(VERSION 3.0)

project(ChakraL)

######################################
# User build configuration
######################################

# Build options
if (WIN32)
  set(CHAKRAL_STATIC_LIB false CACHE BOOL "Builds ChakraL as a static library instead of a DLL")
endif()


# =========================
# Global settings
# =========================

# Output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin")

# Determine the library type
if (CHAKRAL_STATIC_LIB)
  set(CHAKRAL_LIB_TYPE STATIC)
else()
  set(CHAKRAL_LIB_TYPE SHARED)
endif()

# Decide on filenames
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(OUTPUT_FILE_SUFFIX "_d")
else()
  set(OUTPUT_FILE_SUFFIX "")
endif()

set(CMAKE_CXX_STANDARD 20)

# =========================
# Add subdirectories
# =========================
add_subdirectory("./libChakraL")
add_subdirectory("./ChakraLC")
set(TARGET_LIST "libChakraL")

# =========================
# Install stuff
# =========================
message("${TARGET_LIST}")
install(
  TARGETS ${TARGET_LIST}
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
)
install(
  DIRECTORY ${PROJECT_SOURCE_DIR}/libChakraL/include/
  DESTINATION include/libChakraL
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
