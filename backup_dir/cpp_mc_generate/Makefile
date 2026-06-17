TOP := ../../../../evtgennp_install

LIB := $(TOP)/lib
INC := $(TOP)/include

CXX := g++
CXXFLAGS := -I$(INC) `root-config --cflags`
LDFLAGS := `root-config --libs` -L$(LIB) -lEvtGen -Wl,-rpath,$(LIB)

TARGETS := run_kstarll run_bb_kstarll

all: $(TARGETS)

run_kstarll: kstarll_test.cc
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

run_bb_kstarll: bb_kstarll_test_update.cc
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f $(TARGETS)

.PHONY: all clean
