#! /usr/bin/python

from __future__ import division
import sys
from collections import defaultdict
import pprint

def count_freq(counts_file):
    c = defaultdict(int)
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
        c[word] += int(count)
    return c

if __name__ == "__main__":

    if len(sys.argv) != 2: # Expect exactly one argument: the counts file
        sys.exit(2)

    with open(sys.argv[1], "r") as counts_file:
        counts = count_freq(counts_file)

    with open(sys.argv[1], "r") as counts_file:
        for line in counts_file:
            line = line.strip()
            if not line: 
                print
                continue
            # Extract information from line.
            # Each line has the format
            # count WORDTAG tag word
            fields = line.split(" ")
            if fields[1] != "WORDTAG" or counts[fields[3]] >= 5:
                print line
                continue

            word = fields[3]
            if all(c.isupper() for c in word):
                rare_class = "_RARE_ALLCAPS_"
            elif any(c.isdigit() for c in word):
                rare_class = "_RARE_NUM_"
            elif word[-1].isupper():
                rare_class = "_RARE_LASTCAP_"
            else:
                rare_class = "_RARE_"

            print fields[0], fields[1], fields[2], rare_class
