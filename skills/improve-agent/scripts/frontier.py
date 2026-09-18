#!/usr/bin/env python3
"""Pick a parent from the frontier, weighted by how many fixtures each candidate leads on.

Reads a JSON file of {candidate_id: {fixture_id: median_score}} and prints the weights, then one
chosen parent. Weighting by fixtures led rather than by aggregate is deliberate: a candidate that
wins one hard fixture outright is worth extending, and the best average is usually the blandest
thing in the set.
"""
import json
import random
import sys


def leaders(frontier):
    best = {}                                   # fixture -> (score, [ids])
    for cid, scores in frontier.items():
        for fid, s in scores.items():
            if fid not in best or s > best[fid][0]:
                best[fid] = (s, [cid])
            elif s == best[fid][0]:
                best[fid][1].append(cid)
    weight = {}
    for s, ids in best.values():
        for cid in ids:
            weight[cid] = weight.get(cid, 0) + 1 / len(ids)
    return weight                               # candidates on the frontier, weighted by fixtures led


def pick_parent(frontier):
    w = leaders(frontier)
    return random.choices(list(w), weights=list(w.values()))[0]


if __name__ == "__main__":
    frontier = json.load(open(sys.argv[1]))
    for cid, w in sorted(leaders(frontier).items(), key=lambda kv: -kv[1]):
        print(f"{w:6.2f}  {cid}")
    print("parent:", pick_parent(frontier))
