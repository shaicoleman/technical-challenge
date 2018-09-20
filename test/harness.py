#!/usr/bin/env python3
#usage: ./harness.py python3 batch_test.py
import os, sys

base_dir = os.path.dirname(sys.argv[0])

print(base_dir)
tests = { os.path.join(base_dir, "testcases", in_file): os.path.join(base_dir, "testcases", out_file) for in_file, out_file in [
    ("unit-tests.in.txt","unit-tests.out.txt")
    ]}


print(tests)

for i in tests:
    cmd = 'time bash -c "diff -w -b -B -u %s <(%s %s)"' % (tests[i], ' '.join(sys.argv[1:]), i)
    print("Input:", i)
    print(cmd)
    os.system(cmd)
