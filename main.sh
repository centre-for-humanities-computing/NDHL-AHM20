#!/usr/bin/env bash
# pipeline for reddit-trend project

start=`date +%s`
echo pipeline init
while true;do echo -n ':( ';sleep 1;done &

python

kill $!; trap 'kill $!' SIGTERM
echo
echo ':)'

end=`date +%s`
runtime=$((end-start))
printf "Total runtime: %d\n" $runtime
