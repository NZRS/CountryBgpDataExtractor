COUNTRY=NZ
AS_PATH_FILE=data/prefix-aspath.txt.gz
AS_COUNTRY_FILE=data/AS-from-rir.json
PREFIX_FILE=data/networks-from-rir.json
SEL_ASPATH_FILE=data/country-aspath-selection.json

all: ${AS_PATH_FILE} ${AS_COUNTRY_FILE} ${PREFIX_FILE} ${SEL_ASPATH_FILE}

${AS_PATH_FILE}:
	cd BgpExtractor && make extract && cd ..

${AS_COUNTRY_FILE} ${PREFIX_FILE}: RIR/extract-country-data-from-delegation.py
	cd RIR && make COUNTRY=${COUNTRY} extract && cd ..

${SEL_ASPATH_FILE}: CountrySelection/select-prefixes-ASes.py ${AS_PATH_FILE} ${PREFIX_FILE} ${AS_COUNTRY_FILE}
	cd CountrySelection && python2 select-prefixes-ASes.py && cd ..

