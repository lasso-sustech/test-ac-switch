SHELL:=/bin/sh

all:
	gcc -fpic --shared $(shell python3-config --includes) ext/sock_ext.c -o sock_ext.so
