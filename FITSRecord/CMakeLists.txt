add_library(fitsrecord SHARED FITSRecord.cpp)
target_link_libraries (fitsrecord ${CFITSIO_LIBRARIES})
