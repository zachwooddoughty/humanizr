"""
All this file has to do is load the conf file and see if it works properly.
If it does, then it will run the feature extraction based on the specified
parameters.
"""

import argparse
import datetime
import json
import logging

from tfx import confparse, extractor, utils, errors


"""
Handle the command-line args (the path to the conf file, and a debug flag)
"""

argparser = argparse.ArgumentParser(description='Extract features from Twitter users')

argparser.add_argument('conf_file',
                    help='path to the configuration file (JSON)')

argparser.add_argument('tweet_dir',
                    help='path to the directory storing all the tweets (one tweet JSON per file)')

argparser.add_argument('--debug',
                    action='store_true',
                    help='enable debug mode')

args = argparser.parse_args()


"""
If debug mode is on, set the logging mode to debug
"""
if args.debug:
    logging.basicConfig(level=logging.DEBUG)


"""
Make sure the conf file is valid
"""

try:
    conf = confparse.ConfParser()
    conf.load(args.conf_file)
except errors.ConfFileError as error:
    argparser.error("Invalid configuration file: %s" % error)


"""
Try to run everything
"""

# Save the start time (used to calculate total time taken in debug mode)
if args.debug:
    start_time = datetime.datetime.now()

try:
    extractor.FeatureExtractor(conf, args.tweet_dir)
except errors.ExtractionError as error:
    argparser.error("Runtime error: %s" % error)

# Print out the total time taken, if we're in debug mode
if args.debug:
    end_time = datetime.datetime.now()
    time_taken = utils.format_timedelta(end_time - start_time)
    logging.debug(time_taken)
