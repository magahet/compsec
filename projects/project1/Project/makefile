all: sort.c
	gcc -g -fno-stack-protector -mpreferred-stack-boundary=2 sort.c -o sort
alt: sort.c
	gcc -g -fno-stack-protector sort.c -o sort
debug: sort
	gdb -q sort
find-sh: sort
	gdb -q sort < gdb-cmds/find-sh.gdb
find-offset: sort
	find-offset.sh
test: sort
	gdb -q sort < gdb-cmds/test-exploit.gdb
