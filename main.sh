#!/usr/bin/env bash
# pipeline for reddit-trend project

start=`date +%s`
echo pipeline init
while true;do echo -n ':( ';sleep 1;done &

# need to update path variables in codebase for .
python src/build_data.py
python src/build_target.py
python src/train_mdl.py
python src/build_signal.py

kill $!; trap 'kill $!' SIGTERM
echo
echo ':)'

end=`date +%s`
runtime=$((end-start))
printf "Total runtime: %d\n" $runtime
