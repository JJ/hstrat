SHELL := /bin/bash

default: test

test-%: %
	$(MAKE) test -C $<

opt-%: %
	$(MAKE) opt -C $<

fulldebug-%: %
	$(MAKE) fulldebug -C $<

cranky-%: %
	$(MAKE) cranky -C $<

clean-%: %
	$(MAKE) clean -C $<

cov-%: % $(TO_ROOT)/coverage_include
	$(MAKE) coverage -C $<

$(TO_ROOT)/coverage_include:
	cd $(TO_ROOT)/test_include && ./convert_for_tests.sh

# Test in debug mode without pointer tracker
test: $(addprefix test-, $(TARGET_NAMES))

opt: $(addprefix opt-, $(TARGET_NAMES))

fulldebug: $(addprefix fulldebug-, $(TARGET_NAMES))

cranky: $(addprefix cranky-, $(TARGET_NAMES))

coverage: $(addprefix cov-, $(TARGET_NAMES))

clean: $(addprefix clean-, $(TARGET_NAMES))
	rm -f *.out
	rm -f *.o
	rm -f *.gcda
	rm -f *.gcno
	rm -f *.info
	rm -f *.gcov
	rm -f ./Coverage*
	rm -rf ./temp
