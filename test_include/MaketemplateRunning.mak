CXX ?= g++

FLAGS = -std=c++20 -D_GLIBCXX_DEBUG -D_LIBCPP_DEBUG -g -pipe -pthread -Wall -Wno-unused-function -Wno-unused-private-field -I$(TO_ROOT)/include/ -I$(TO_ROOT)/third-party/ $$(python3 -m pybind11 --includes) -DCATCH_CONFIG_MAIN

default: test

test-%: %.cpp ../third-party/Catch2/single_include/catch2/catch.hpp
	$(CXX) $(FLAGS) $< -o $@.out
	# execute test
	./$@.out

cov-%: %.cpp ../third-party/Catch2/single_include/catch2/catch.hpp
	$(CXX) $(FLAGS) $< -o $@.out
	#echo "running $@.out"
	# execute test
	./$@.out
	llvm-profdata merge default.profraw -o default.profdata
	llvm-cov show ./$@.out -instr-profile=default.profdata > coverage_$@.txt
	python $(TO_ROOT)/third-party/force-cover/fix_coverage.py coverage_$@.txt

# Test in debug mode without pointer tracker
test: $(addprefix test-, $(TEST_NAMES))
	rm -rf test*.out

# Test optimized version without debug features
opt: FLAGS := -std=c++20 -pipe -pthread -DNDEBUG -O3 -ffast-math -flto -march=native -Wno-unused-function -I$(TO_ROOT)/include/ -I$(TO_ROOT)/third-party/ $$(python3 -m pybind11 --includes) -DCATCH_CONFIG_MAIN
opt: $(addprefix test-, $(TEST_NAMES))
	rm -rf test*.out

# Test in debug mode with pointer tracking
fulldebug: FLAGS := -std=c++20 -pipe -pthread -g -Wall -Wno-unused-function -I$(TO_ROOT)/include/ -I$(TO_ROOT)/third-party/ $$(python3 -m pybind11 --includes) -pedantic -DEMP_TRACK_MEM -D_GLIBCXX_DEBUG -D_LIBCPP_DEBUG -Wnon-virtual-dtor -Wcast-align -Woverloaded-virtual -ftemplate-backtrace-limit=0 -DCATCH_CONFIG_MAIN # -Wmisleading-indentation
fulldebug: $(addprefix test-, $(TEST_NAMES))
	rm -rf test*.out

cranky: FLAGS := -std=c++20 -pipe -pthread -g -Wall -Wno-unused-function -I$(TO_ROOT)/include/ -I$(TO_ROOT)/third-party/ $$(python3 -m pybind11 --includes) -pedantic -DEMP_TRACK_MEM -D_GLIBCXX_DEBUG -D_LIBCPP_DEBUG -Wnon-virtual-dtor -Wcast-align -Woverloaded-virtual -Wconversion -Weffc++ -DCATCH_CONFIG_MAIN
cranky: $(addprefix test-, $(TEST_NAMES))
	rm -rf test*.out

$(TO_ROOT)/coverage_include:
	./$(TO_ROOT)/test_include/convert_for_tests.sh

../third-party/Catch2/single_include/catch2/catch.hpp:
	git submodule init
	git submodule update

coverage: FLAGS := -std=c++20 -pthread -g -Wall -Wno-unused-function -I$(TO_ROOT)/coverage_include/ -I$(TO_ROOT)/third-party/ $$(python3 -m pybind11 --includes) -DEMP_TRACK_MEM -Wnon-virtual-dtor -Wcast-align -Woverloaded-virtual -ftemplate-backtrace-limit=0 -fprofile-instr-generate -fcoverage-mapping -fno-inline -fno-elide-constructors -O0 -DCATCH_CONFIG_MAIN
coverage: $(TO_ROOT)/coverage_include $(addprefix cov-, $(TEST_NAMES))

clean:
	rm -f *.out
	rm -f *.o
	rm -f *.gcda
	rm -f *.gcno
	rm -f *.info
	rm -f *.gcov
	rm -f ./Coverage*
	rm -rf ./temp
