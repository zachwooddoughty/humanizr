#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PATH="$PATH;./op-classifier/src/twitter-feature-extractor/tfx;./op-classifier/src/ml-classifier/src/"


for split in "train" "dev" "test"; do
# ./op-classifier/src/twitter-feature-extractor/bin/tfx $DIR/balanced/features.conf.json $DIR/balanced/${split}/ --debug;
echo $split
./op-classifier/src/twitter-feature-extractor/bin/tfx $DIR/full/features.conf.json $DIR/full/${split}/ --debug;
done
