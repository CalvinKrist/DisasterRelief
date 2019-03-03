#!/usr/bin/env bash

mkdir media_images
cd TweetScraper/Data/tweet
curl --max-redirs 100 https://$1 -L > ../../../output.txt