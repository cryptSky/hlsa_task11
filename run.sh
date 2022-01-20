#!/bin/bash

while IFS=, read -r name email
do
    emaill=`echo $email | sed 's/\\r//g'`
    #echo $emaill
    #echo "{\"name\": \"$name\",\"email\": \"$email\"}"
    JSON_STRING='{"name":"'"$name"'","email":"'"$emaill"'"}'
    #echo $JSON_STRING

    curl --request POST \
    --url http://localhost:8000/users \
    --header 'content-type: application/json' \
    --data $JSON_STRING

done < <(tail -n +2 feed.csv)