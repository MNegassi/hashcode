#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default="./domain.pddl")
    parser.add_argument("problem")
    args = parser.parse_args()

    print("Running translate.py ...")
    subprocess.check_call([
        "python3",
        "./fast_downward/builds/release32/bin/translate/translate.py",
        args.domain,
        args.problem
    ])

    subprocess.check_call([
        "./fast_downward/builds/release32/bin/downward",
        "output.sas"
    ])


if __name__ == "__main__":
    main()
