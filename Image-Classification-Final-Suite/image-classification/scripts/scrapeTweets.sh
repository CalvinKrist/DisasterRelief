#!/usr/bin/env bash

cd ../../../TweetScraper
pwd
scrapy crawl TweetScraper -a query="(hurricane OR fire OR tornado OR flood OR landslide OR earthquake OR volcano OR typhoon OR disaster) news filter:images filter:verified" & sleep 30 ; kill $!
