echo "=================================================================="
echo "RUNNING 10 TRIALS - with DEBUG"

if [ $# -eq 1 ]
then
	echo "IGNORING BUGS $1"
	echo "=================================================================="
	./fuzzer --debug --trials 10 ./pstotext-linux-x86 -ignore $1 --fuzz-file postscript
else
	echo "=================================================================="
	./fuzzer --debug --trials 10 ./pstotext-linux-x86 --fuzz-file postscript
fi
echo "------------------------------------------------------------------"

