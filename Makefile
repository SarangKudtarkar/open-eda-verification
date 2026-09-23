SIM ?= icarus

TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(PWD)/src/arbiter.v

COCOTB_TOPLEVEL = arbiter

COCOTB_TEST_MODULES = tb.test_pyuvm

include $(shell cocotb-config --makefiles)/Makefile.sim

reference-model:
	g++ -std=c++17 -Wall -Wextra -O2 models/reference_model.cpp -o models/reference_model
