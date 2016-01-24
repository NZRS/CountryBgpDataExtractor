SOURCE_DIR?=${HOME}/git/BgpDataFinder
SOURCE_FILES_RIPE:=$(shell find ${SOURCE_DIR} -type f -name "bview.*.gz")
SOURCE_FILES_RV:=$(shell find ${SOURCE_DIR} -type f -name "rib.*.bz2")

extract: mrt2txt.sh
	./mrt2txt.sh ${SOURCE_FILES_RIPE} ${SOURCE_FILES_RV}
