echo "=================================================================="
echo "RUNNING 1000 TRIALS"

if [ $# -eq 1 ]
then
	echo "IGNORING BUGS $1"
	echo "=================================================================="
	./fuzzer --trials 1000 ./pstotext-linux-x86 -ignore $1 --fuzz-file postscript
else
	echo "=================================================================="
	./fuzzer --trials 1000 ./pstotext-linux-x86 --fuzz-file postscript
fi
echo "------------------------------------------------------------------"

