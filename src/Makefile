include ../Makefile.inc

CXX   = g++
# -pedantic fails with: ISO C++ does not support 'long long'
#CXXFLAGS  = -Wall -pedantic
CXXFLAGS  = -g -Wall

PROJECT = libevlio.a
OBJECTS = FITSRecord.o
INCLUDES = -I. -I/Users/mraue/Stuff/unix/cfitsio

all: $(PROJECT)

.C.o:
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) $<

$(PROJECT): $(OBJECTS)
	libtool -o $(PROJECT) -static $(OBJECTS)

clean :
	rm $(OBJECTS) $(PROJECT)
