cmake_minimum_required  (VERSION 2.6)
project (evlio)
enable_testing()

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/CMakeModules/")

# Set this variable if you cfitsio is installed in a custom directory
set(CFITSIO_ROOT_DIR /Users/mraue/Stuff/unix/cfitsio)

find_package(CFITSIO REQUIRED)
include_directories(${CFITSIO_INCLUDE_DIRS})
set( EXTRA_LIBS ${EXTRA_LIBS} ${CFITSIO_LIBRARIES} ) 

add_subdirectory(FITSRecord)

# Create records include files, target will always be executed (ALL)
add_custom_target(
    createrecords
    ALL
    COMMAND mkdir ${PROJECT_BINARY_DIR}/records && python ${PROJECT_SOURCE_DIR}/scripts/create_records.py
    ${PROJECT_SOURCE_DIR}/templates -o ${PROJECT_BINARY_DIR}/records
    COMMENT "Running python scripts ..."
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
   )
