cmake_minimum_required(VERSION 3.4)
project(cspice C)

include(conanbuildinfo.cmake)
conan_basic_setup()

file(GLOB SRC_FILES ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/src/cspice/*.c)
add_library(cspice ${SRC_FILES})

if(WIN32)
  target_compile_definitions(cspice PRIVATE "_COMPLEX_DEFINED;MSDOS;OMIT_BLANK_CC;NON_ANSI_STDIO")
  set_target_properties(cspice PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
elseif(UNIX)
  target_compile_definitions(cspice PRIVATE "NON_UNIX_STDIO")
  target_compile_options(cspice PRIVATE -ansi)
endif()

# Behavior of implicitly defined functions changed in AppleClang 12
# https://developer.apple.com/documentation/xcode-release-notes/xcode-12-release-notes
if(CMAKE_C_COMPILER_ID STREQUAL "AppleClang" AND 
   CMAKE_C_COMPILER_VERSION VERSION_GREATER_EQUAL "12")
   target_compile_options(cspice PRIVATE -Wno-error=implicit-function-declaration)
endif()

install(
  TARGETS cspice
  EXPORT cspice
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)

file(GLOB INCLUDE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/include/*.h)
install(FILES ${INCLUDE_FILES} DESTINATION include)
