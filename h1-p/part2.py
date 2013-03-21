#! /usr/bin/python

from __future__ import division
import sys
from collections import defaultdict
import pprint

def get_mle(counts_file):
    """
    """
    obs_counts = defaultdict(
        lambda : {
            "total_count": 0, 
            "word_counts": defaultdict(int) 
        }
    )
    bi_c = {} 
    q = {}
    for line in counts_file:
        line = line.strip()
        if not line: 
            continue

        # Extract information from line.
        # Each line has the format
        # count WORDTAG tag word
        fields = line.split(" ")
        if fields[1] == "WORDTAG":
            (count, count_type, tag, word) = fields
            count = int(count)
            obs_counts[tag]["total_count"] += count
            obs_counts[tag]["word_counts"][word] += count
        elif fields[1] == "2-GRAM":
            (count, count_type, u, v) = fields
            bi_c[(u, v)] = int(count)
        elif fields[1] == "3-GRAM":
            (count, count_type, u, v, w) = fields
            q[(u, v, w)] = int(count) / bi_c[(u, v)]

    e = {}
    for tag in obs_counts:
        e[tag] = {}
        for (word, count) in obs_counts[tag]["word_counts"].iteritems():
            e[tag][word] = count / obs_counts[tag]["total_count"]

    return (q, e)

def is_word_in_vocab(obs_counts, word):
    for tag in obs_counts:
        if word in obs_counts[tag]["word_counts"]:
            return True
    return False

def usage():
    print """
    python part1.py counts_file test_file > output_file
        Read in a gene tagged training input file and produce counts.
    """

class TrigramHMM(object):
    def __init__(self, q, e):
        self.q = q
        self.e = e
        self.all_states = set()

    def find_tags(self, words):
        tags = []
        for word in words:
            pass
        return tags

if __name__ == "__main__":

    if len(sys.argv) != 3: 
        usage()
        sys.exit(2)

    with open(sys.argv[1], "r") as counts_file:
        (q, e) = get_mle(counts_file)
        #pprint.pprint(q)
        #pprint.pprint(e)

    hmm = TrigramHMM(q, e)
    with open(sys.argv[2], "r") as test_file:
        words = []
        for line in test_file:
            word = line.strip()
            if word:
                words.append(word)
            else:
                words.append("STOP")
                print hmm.find_tags(words)
                words = []
