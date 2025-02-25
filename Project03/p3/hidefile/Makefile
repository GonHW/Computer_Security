all:	hidefile.so

hidefile.so:	hidefile.c
	gcc -shared -fPIC hidefile.c -o hidefile.so -ldl

clean:
	rm -f hidefile.so secret-1.txt secret-2.txt sec.txt sec1.txt

test:	all
	@ echo creating "sec.txt"; echo "this file is hidden" >sec.txt
	@ echo creating "sec1.txt"; echo "this file is hidden" >sec1.txt
	@ echo creating "secret-1.txt"; echo "this file is hidden" >secret-1.txt
	@ echo creating "secret-2.txt"; echo "this file is also hidden" >secret-2.txt
	@ echo "hiding secret-1"
	export HIDDEN=secret-1.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding secret-2"
	export HIDDEN=secret-2.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding nothing"
	unset HIDDEN
	LD_PRELOAD=$$PWD/hidefile.so; ls -l

	@ echo "hiding secret-1 and secret-2"
	export HIDDEN=secret-1.txt:secret-2.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding sec.txt and sec1.txt"
	export HIDDEN=sec.txt:sec1.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
	@ echo "hiding all files"
	export HIDDEN=secret-1.txt:secret-2.txt:test:hidefile.c:hidefile.so:Makefile:sec.txt:sec1.txt:Makefile.txt LD_PRELOAD=$$PWD/hidefile.so; ls -l
