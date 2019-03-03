#!/usr/bin/env bash

echo $1
curl --max-redirs 100 $1 -L > Image-Classification-Final-Suite/image-classification/scripts/media_images/img$2.jpg