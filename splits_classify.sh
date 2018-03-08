

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PATH="$PATH;./op-classifier/src/twitter-feature-extractor/tfx;./op-classifier/src/ml-classifier/src/"

# echo "Balanced"
# 
# echo "dev" # 89.0
# ./op-classifier/src/ml-classifier/scripts/classifier -t $DIR/balanced/train/features.json -m $DIR/balanced/train.model.json ./op-classifier/src/ml-classifier/src/ml2/libsvm_settings.txt balanced/dev/features.json
# 
# echo "test" # 89.6
# ./op-classifier/src/ml-classifier/scripts/classifier -t $DIR/balanced/train/features.json -m $DIR/balanced/train.model.json ./op-classifier/src/ml-classifier/src/ml2/libsvm_settings.txt balanced/test/features.json

echo "Full"

echo "dev"  # 94.8
./op-classifier/src/ml-classifier/scripts/classifier -t $DIR/full/train/features.json -m $DIR/full/train.model.json ./op-classifier/src/ml-classifier/src/ml2/libsvm_settings.txt full/dev/features.json

echo "test" # 94.8
./op-classifier/src/ml-classifier/scripts/classifier -t $DIR/full/train/features.json -m $DIR/full/train.model.json ./op-classifier/src/ml-classifier/src/ml2/libsvm_settings.txt full/test/features.json
