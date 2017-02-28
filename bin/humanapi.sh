#!/bin/sh
 
HUMAN_API_ROOT_URL="https://api.humanapi.co/v1"
RESOURCE="$1"
#
# HUMAN_API_ACCESS_TOKEN needs to be set outside of this
# HUMAN_API_ACCESS_TOKEN=fdjkshkjshafkhjsdkfhjaskfhjaksdhjfkajsdhfkj
#
curl $HUMAN_API_ROOT_URL/$RESOURCE?access_token=$HUMAN_API_ACCESS_TOKEN 

