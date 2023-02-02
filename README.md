# Sbox_implementation
================================================================================
          Before executing python code, install STP and cryptominisat solver
================================================================================
Before executing python code, install STP and cryptominisat solver

Install instructions
	For Debian-like platforms first install the prerequisites:

	apt-get install cmake g++ zlib1g-dev libboost-all-dev flex bison

Then install cryptominisat:
	git clone https://github.com/msoos/cryptominisat
	cd cryptominisat
	mkdir build && cd build
	cmake ..
	cmake --build .
	sudo cmake --install .
	command -v ldconfig && sudo ldconfig

Then install STP:

	git clone https://github.com/stp/stp.git
	cd stp && mkdir build && cd build
	cmake ..
	make
	sudo make install
