import os
import json
import gzip
import time

all_tweets = "/export/b20/zach/libs/humanizr/tweets/humanizr-2018-03-01-scrape.json.gz"
balanced_splits = "/export/b20/zach/demographer/data/humanizr/hum_balanced"
full_splits = "/export/b20/zach/demographer/data/humanizr/hum_full"


def load_splits(setup):
  if setup == 'balanced':
    splits_dir = balanced_splits
  elif setup == 'full':
    splits_dir = full_splits
  else:
    raise ValueError("unknown setup: {}".format(setup))

  d = {}
  for split in ["train", "dev", "test"]:
    with open(os.path.join(splits_dir, "{}.txt".format(split))) as inf:
      for line in inf:
        d[int(line.rstrip())] = split

  return d


def build(setup):
  print("building {} setup".format(setup))
  outfns = {split: None for split in ('train', 'dev', 'test')}
  for split in outfns.keys():
    if not os.path.exists(os.path.join(setup, split)):
      os.mkdir(os.path.join(setup, split))
    json_fn = os.path.join(setup, split, "{}.json".format(split))
    outfns[split] = json_fn
    if os.path.exists(json_fn):
      query = "{} exists; Overwrite? ".format(json_fn)
      if str(input(query)).lower().startswith("y"):
        with open(json_fn, 'w'):
          pass

  splits = load_splits(setup)
  total = 4.7e6
  count = 0
  start = time.time()
  with gzip.open(all_tweets, "rt") as inf:
    # for i in range(1000):
    #   line = inf.readline()
    for line in inf:
      count += 1
      if count % 1e5 == 0:
        sec_per_tweet = (time.time() - start) / count
        hours_till_done = sec_per_tweet * (total - count) / 3600
        print("At {:3.1f}M tweets; Should finish in {:.2f} hours".format(
            count / 1e6, hours_till_done))
      tweet = json.loads(line.strip())
      userid = tweet.get("user", {}).get("id")
      if userid is None:
        continue
      split = splits.get(userid)
      if split:
        with open(outfns[split], "a") as outf:
          outf.write("{}\n".format(json.dumps(tweet)))

if __name__ == "__main__":
  build("balanced")
