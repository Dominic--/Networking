CC = gcc
CARG = -Wall -O3 -std=c99 -lm

all: main

main:
	$(CC) $(CARG) off_by_connectivity.c eigenvalue.c utils.c -o ../bin/off_by_connectivity
	$(CC) $(CARG) off_by_power.c eigenvalue.c utils.c power.c -o ../bin/off_by_power
	$(CC) $(CARG) abilene.c -o ../bin/abilene
	$(CC) $(CARG) test_connectivity.c utils.c -o test
clean:
	rm *.out
