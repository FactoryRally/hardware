#!/bin/bash

gameid=$(curl -X POST "http://localhost:5050/v1/games" -H "accept: */*" -H "Content-Type: application/json-patch+json" -d "{\"playerNamesVisible\":true,\"maxPlayers\":2,\"name\":\"string\",\"robotsPerPlayer\":1,\"fillWithBots\":true}") 
echo "$gameid"
gameid2=$(curl -X POST "http://localhost:5050/v1/games/$gameid/players" -H "accept: text/plain")
echo "$gameid2"

