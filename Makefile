include Makefile.inc

DIRS	= src

all :
	$(ECHO) '==> Running python scripts ..'
	$(PYTHON) ./scripts/create_records.py
	$(ECHO) '==> done.'
	$(ECHO) '==> Checking subdirectories ..'
	-for d in $(DIRS); do ($(ECHO) '--> Looking into directory' $$d; cd $$d; $(MAKE) $(MFLAGS) ); done

clean :
	$(ECHO) cleaning up
	-for d in $(DIRS); do ($(ECHO) '--> Looking into directory' $$d; cd $$d; $(MAKE) clean ); done