device=cpu
FELTOR_PATH=../feltor

#configure machine
include $(FELTOR_PATH)/config/default.mk
include $(FELTOR_PATH)/config/*.mk
include $(FELTOR_PATH)/config/devices/devices.mk
# use nlohmann/json because jsoncpp made problems
JSONLIB=-DDG_USE_JSONHPP

INCLUDE+=-I$(FELTOR_PATH)/inc/

# Here is some Makefile magic to build the targets that live in another directory
PRE=pyfeltor/dg/geo/
TARGETS= geometries polynomial solovev guenter circular flux mod toroidal utility
SUFFIX=$(shell python3-config --extension-suffix)
TARGETS_=$(addsuffix $(SUFFIX),$(TARGETS))
ALL=$(addprefix $(PRE),$(TARGETS_))

#$(info    TARGETS is $(TARGETS) )
#$(info    SUFFIX is $(SUFFIX) )
#$(info    ALL is $(ALL) )

all: $(ALL)

# the cpp file can have different name, the so file needs the name of the python module
$(PRE)%$(SUFFIX): $(PRE)%.cpp
	$(CC) $(OPT) $(CFLAGS) -shared -fPIC $$(python3 -m pybind11 --includes) $< -o $@ $(JSONLIB) $(INCLUDE) -g

install:
	python3 -m pip install -e .

.PHONY: clean

clean:
	rm -f $(ALL)
