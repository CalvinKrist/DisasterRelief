#!/usr/bin/env bash

mkdir Image-Classification-Final-Suite/image-classification/scripts/media_images
cd TweetScraper/Data/tweet
curl --max-redirs 100 https://$1 -L > ../../../output.txt