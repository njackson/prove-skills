#!/usr/bin/env python3
"""Permutation test for one arm against another, one score per fixture, same fixture order.

The arm labels are flipped WITHIN each fixture and never shuffled across fixtures. A hard fixture is
hard in both arms, and pooling them pretends chance is quieter than it is, which is how a four-point
nothing gets reported as a win.
"""
import argparse
import json
import random


def mean(xs):
    return sum(xs) / len(xs)


def clears_floor(baseline, candidate, alpha=0.05, trials=10_000):
    observed = mean(candidate) - mean(baseline)
    at_least = 0
    for _ in range(trials):
        b, c = [], []
        for x, y in zip(baseline, candidate):   # flip the arm label within each fixture
            if random.random() < 0.5:
                x, y = y, x
            b.append(x)
            c.append(y)
        if abs(mean(c) - mean(b)) >= abs(observed):
            at_least += 1
    p = at_least / trials
    return observed, p, p < alpha


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline")                 # JSON list of scores, one per fixture
    ap.add_argument("candidate")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--trials", type=int, default=10_000)
    a = ap.parse_args()
    observed, p, cleared = clears_floor(
        json.load(open(a.baseline)), json.load(open(a.candidate)), a.alpha, a.trials)
    print(f"observed {observed:+.3f}   p={p:.4f}   {'clears' if cleared else 'UNCONFIRMED'}")
