#! /bin/bash

#	-DDEBUG=n			Enable debugging level n
#	-DDEV_PKG=1			Development package configuration
#	-DBUILD_DOC=1		Man pages generated
#	-DBUILD_NNG=1		Enable building of NNG and the RMR NNG based libraries
#	-DIGNORE_LIBDIR=1	Installation of rmr libries is into /usr/local/lib and ignores
#						value in CMAKE_INSTALL_LIBDIR.
#						system preferred (typically /usr/local/lib64).
#	-DPRESERVE_PTYPE=1	Do not change the processor type when naming deb packages
#	-DPACK_EXTERNALS=1	Include external libraries used to build in the run-time package
#						(This makes some stand-alone unit testing of bindings possible, it
#						is not meant to be used for production package generation.)
#	-DGPROF=1			Enable profiling compile time flags
#	-DSKIP_EXTERNALS=1	Do not use NNG submodule when building; uee installed packages
#	-DMAN_PREFIX=<path>	Supply a path where man pages are installed (default: /usr/share/man)

rm -rf .build
sudo /usr/local/lib/librmr*.*
mkdir -p .build && cd .build || exit
# cmake ..
cmake .. -DDEBUG=1
make package
sudo make install
sudo ldconfig
