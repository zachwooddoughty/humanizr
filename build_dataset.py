import os
import argparse
import gzip
import json


RAW_DATA = "/export/b20/zach/genseq/datasets/humanizrNames/raw.json.gz"
BALANCED_SPLITS = "/export/b20/zach/demographer/data/humanizr/balanced"
FULL_SPLITS = "/export/b20/zach/demographer/data/humanizr/full"
ORGS = "/export/b20/zach/demographer/data/humanizr/all_orgs.txt"
INDS = "/export/b20/zach/demographer/data/humanizr/all_inds.txt"


def get_user(d):
  if 'user' in d:
    return d['user']
  else:
    return d


def build(setup='full', train_balance_ratio=1., outdir='.'):
  _lengths = []

  if setup == 'balanced':
    splits_dir = BALANCED_SPLITS
  elif setup == 'full':
    splits_dir = FULL_SPLITS
  else:
    raise ValueError("Unknown setup: {}".format(setup))
  suffix = ".{}.{}".format(setup, train_balance_ratio)

  names = ("train", "dev", "test")
  json_files = ['{}{}.json'.format(name, suffix) for name in names]
  if all(os.path.exists(os.path.join(outdir, fn)) for fn in json_files):
    resp = input("All dataset files exist. Overwrite? ")
    if not str(resp).lower().startswith("y"):
      print("Aborting")
      return
  elif any(os.path.exists(os.path.join(outdir, fn)) for fn in json_files):
    resp = input("Some dataset files exist. Overwrite? ")
    if not str(resp).lower().startswith("y"):
      print("Aborting")
      return

  splits = {}

  label_map = {}
  with open(ORGS) as inf:
    for line in inf:
      label_map[int(line.rstrip())] = "org"

  print("Dataset has {} orgs".format(len(label_map)))

  with open(INDS) as inf:
    for line in inf:
      if int(line.rstrip()) in label_map:
        raise ValueError("Doubly labeled id {}".format(line.rstrip()))
      label_map[int(line.rstrip())] = "ind"

  num_train_orgs = 0
  for split in names:
    splitfn = os.path.join(splits_dir, "{}.txt".format(split))
    with open(splitfn) as inf:
      for line in inf:
        userid = int(line.rstrip())
        # Skip train individuals for now
        if split != 'train':
          splits[userid] = split
        elif label_map.get(userid) == "org":
          splits[userid] = split
          num_train_orgs += 1

  print("added {} organizations to train set".format(num_train_orgs))

  # Now add in train individuals
  with open(os.path.join(splits_dir, "train.txt")) as inf:
    count = 0
    for line in inf:
      userid = int(line.rstrip())
      # Skip train individuals for now
      if label_map.get(userid) == "ind":
        splits[userid] = "train"
        count += 1
        if count > (num_train_orgs * train_balance_ratio):
          break

  print("added {} individuals to train set".format(count))

  if not os.path.exists(RAW_DATA):
    raise ValueError("need to download data")

  skipped = 0
  with gzip.open(RAW_DATA, "rt") as inf:
    # for i in range(1000):
    #   line = inf.readline()
    for line in inf:
      d = json.loads(line.rstrip())
      user = get_user(d)
      userid = user['id']
      split = splits.get(userid)
      label = label_map.get(userid)
      user['accounttype_'] = label

      if split is None or label is None:
        skipped += 1
        continue

      outfn = os.path.join(
          outdir, json_files[names.index(split)])
      with open(outfn, "a", encoding='utf8') as outf:
        outf.write("{}\n".format(json.dumps(user)))


def main():
  parser = argparse.ArgumentParser("build dataset for individual vs. organization")
  parser.add_argument("setup", type=str,
                      help="(full|balanced); balance of orgs and inds in dev and test sets")
  parser.add_argument("ratio", type=float,
                      help="How many individuals for every organization in training data")
  parser.add_argument("--outdir", type=str, default=".", help="Output directory (default cwd)")
  args = parser.parse_args()

  build(setup=args.setup, train_balance_ratio=args.ratio, outdir=args.outdir)


if __name__ == "__main__":
  main()
