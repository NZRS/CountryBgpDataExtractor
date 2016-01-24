## Introduction

mrt2txt.sh has as pre-requisite bgpdump
(https://bitbucket.org/ripencc/bgpdump/wiki/Home).

For Mac OS X, you can
- hg clone https://bitbucket.org/ripencc/bgpdump
- cd bgpdump
- bash bootstrap.sh
- make install

## How to use

The included Makefile will take care of parsing the available BGP dumps
in MRT format into a plain text file that can be used for further
processing.

```
make extract
```
