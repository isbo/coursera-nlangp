#! /usr/bin/python

from __future__ import division
import sys
from collections import defaultdict
import pprint

"""
Count n-gram frequencies in a data file and write counts to
stdout. 
"""

def count_obs(counts_file):
    """
    """
    obs_counts = defaultdict(
        lambda : {
            "total_count": 0, 
            "word_counts": defaultdict(int) 
        }
    )
    for line in counts_file:
        line = line.strip()
        if not line: 
            continue

        # Extract information from line.
        # Each line has the format
        # count WORDTAG tag word
        fields = line.split(" ")
        if fields[1] != "WORDTAG":
            continue
        (count, count_type, tag, word) = fields
        count = int(count)
        obs_counts[tag]["total_count"] += count
        obs_counts[tag]["word_counts"][word] += count

    return obs_counts

def is_word_in_vocab(obs_counts, word):
    for tag in obs_counts:
        if word in obs_counts[tag]["word_counts"]:
            return True
    return False

def find_tag(obs_counts, word):
    max_p = 0 
    best_tag = None
    for tag in obs_counts:
        if not is_word_in_vocab(obs_counts, word):
            word = "_RARE_"
        p = obs_counts[tag]["word_counts"][word] / obs_counts[tag]["total_count"]
        #print word, p, tag, obs_counts[tag]["word_counts"][word], obs_counts[tag]["total_count"]
        if p > max_p:
            best_tag = tag
            max_p = p
    return best_tag

def usage():
    print """
    python part1.py counts_file test_file > output_file
        Read in a gene tagged training input file and produce counts.
    """

if __name__ == "__main__":

    if len(sys.argv) != 3: # Expect exactly one argument: the counts file
        usage()
        sys.exit(2)

    with open(sys.argv[1], "r") as counts_file:
        obs_counts = count_obs(counts_file)
        for k in obs_counts:
            #print k, obs_counts[k]['total_count'], obs_counts[k]['word_counts']['_RARE_']
            #pprint.pprint(obs_counts['O'], indent=3)
            #pprint.pprint(obs_counts['I-GENE'], indent=3)
            pass
            

    with open(sys.argv[2], "r") as test_file:
        for line in test_file:
            word = line.strip()
            if not word: 
                print
                continue
            tag = find_tag(obs_counts, word)
            print word, tag
