#!/usr/bin/env bash

echo $1
curl --max-redirs 100 $1 -L > media_images/img$2.jpg