#!/usr/bin/env python3

import sys
import requests
import os
import json
import re
URL=os.environ.get('PAINTSHOP_URL', "http://0.0.0.0:8080")

def squish_whitespace(str):
    return re.sub(r"\s+", ' ', str.strip())

def delete_whitespace(str):
    return re.sub(r"\s+", '', str)

def process_content(content):
    output = []
    testcases = int(content[0])
    content = content[1:]
    for c in range(testcases):
        number_of_colors = int(content[0])
        number_of_customers = int(content[1])
        demands = []
        for l in range(number_of_customers):
            demand = list(map(int, content[l+2].split()))
            demands.append(demand)
        params = { 'colors': number_of_colors,
                   'customers': number_of_customers,
                   'demands': demands }
        input_params = { 'input': delete_whitespace(json.dumps(params)) }
        solution = requests.get(URL + "/v1/", params=input_params).content.decode("utf-8")
        output.append("Case #{}: {}".format(c + 1, solution))

        demands_v2 = delete_whitespace(json.dumps(demands))
        params_v2 = { 'colors': number_of_colors,
                      'customers': number_of_customers,
                      'demands': demands_v2 }
        solution_v2 = requests.get(URL + "/v2/", params=params_v2).content.decode("utf-8")
        output.append("Case #{} (v2): {}".format(c + 1, squish_whitespace(solution_v2)))

        content = content[number_of_customers + 2:]
    return output

def main(input_file):
    with open(input_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for line in process_content(content):
        print(line)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    elif 'input.txt' in os.listdir('.'):
        main('input.txt')
    else:
        print("Where is my input? input.txt does not exist, Create one, or provide a filename as an argument")
