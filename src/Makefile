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
	$(ECHO) $(CXX) -c $(CXXFLAGS) $(INCLUDES) $<
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) $<

$(PROJECT): $(OBJECTS)
	$(ECHO) libtool -o $(PROJECT) -static $(OBJECTS)
	libtool -o $(PROJECT) -static $(OBJECTS)

clean :
	$(ECHO) rm *.o *.a
	rm *.o *.a
