device=cpu
FELTOR_PATH=../feltor

#configure machine
include $(FELTOR_PATH)/config/default.mk
include $(FELTOR_PATH)/config/*.mk
include $(FELTOR_PATH)/config/devices/devices.mk
JSONLIB=-DDG_USE_JSONHPP

INCLUDE+=-I$(FELTOR_PATH)/inc/

PRE=pyfeltor/dg/geo

all: geometries polynomial solovev guenter circular flux mod toroidal utility

# the cpp file can have different name, the so file needs the name of the python module

%: $(PRE)/%.cpp
	$(CC) $(OPT) $(CFLAGS) -shared -fPIC $$(python3 -m pybind11 --includes) $< -o $(PRE)/$@$$(python3-config --extension-suffix) $(JSONLIB) $(INCLUDE) -g

install:
	python3 -m pip install -e .

.PHONY: clean

clean:
	rm -f $(PRE)/geometries/$$(python3-config --extension-suffix)
