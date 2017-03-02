#!/bin/sh

SwitchAudioSource -a |grep -q "NESSIE USB MIC"

if [ $? -eq 0 ]
then
  SwitchAudioSource -t output -s "BLUE NESSIE USB MIC" >/dev/null
  SwitchAudioSource -t input -s "BLUE NESSIE USB MIC" >/dev/null
fi
