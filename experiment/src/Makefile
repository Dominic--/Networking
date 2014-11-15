CC = gcc
CARG = -Wall -O3 -std=c99 -lm

all: main

main:
	$(CC) $(CARG) off.c eigenvalue.c utils.c -o ../bin/off
	$(CC) $(CARG) abilene.c -o ../bin/abilene
clean:
	rm *.out
