
run:	all
	@echo "---\nC version:"
	./base64sha256
	@echo "---\nJava version:"
	CLASSPATH=. java Sha256Base64
	@echo "---\nPython version:"
	python3 ./hash.py

all: base64sha256 Sha256Base64.class

base64sha256: base64sha256.c
	gcc -o base64sha256 base64sha256.c -lssl -lcrypto


Sha256Base64.class: Sha256Base64.java
	javac Sha256Base64.java
