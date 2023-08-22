import requests
from flask import Flask, request, jsonify
import json
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(_name_)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()  # Raise an error for non-2xx responses
        data = response.json()
        return data.get("numbers", [])
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return []

def merge_sorted_lists(lists):
    result = []
    while any(lists):
        smallest = float("inf")
        smallest_list = None
        for i, lst in enumerate(lists):
            if lst and lst[0] < smallest:
                smallest = lst[0]
                smallest_list = i
        result.append(smallest)
        lists[smallest_list].pop(0)
    return result

@app.route("/numbers", methods=["GET"])
def get_numbers():
    urls = request.args.getlist("url")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers, url) for url in urls]
        results = [future.result() for future in futures]

    merged_numbers = merge_sorted_lists(results)
    response_data = {"numbers": merged_numbers}
    return jsonify(response_data)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=3000)
