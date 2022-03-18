#!/bin/bash
# WANT_JSON

addr=$(cat $1 | grep -Po '(?<="addr": ")(.*?)(?=")')
tls=$(cat $1 | grep -Po '(?<="tls": )(.*?)(?=,)')

if $tls; 
then
    status_code=$(curl -I https://www.$addr 2>/dev/null | head -n 1 | cut -d$' ' -f2)
else
    status_code=$(curl -I http://www.$addr 2>/dev/null | head -n 1 | cut -d$' ' -f2)
fi

if [ "$status_code" -eq "200" ]
then
    echo "{\"failed\": false, \"rc\": \"$status_code\", \"site_status\": \"Available\", \"msg\": \"\"}"
else
    echo "{\"failed\": true, \"site_status\": \"Not available\"}"
fi