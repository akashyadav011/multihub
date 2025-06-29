import requests
from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    try:
        crypto_response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1, "sparkline": "false"}
        )
        crypto_data = crypto_response.json() if crypto_response.status_code == 200 else []
    except Exception:
        crypto_data = []

    try:
        nasa_response = requests.get(
            "https://images-api.nasa.gov/search",
            params={"q": "space", "media_type": "image"}
        )
        nasa_json = nasa_response.json() if nasa_response.status_code == 200 else {}
        nasa_items = []
        if "collection" in nasa_json and "items" in nasa_json["collection"]:
            for item in nasa_json["collection"]["items"][:5]:
                data = item.get("data", [{}])[0]
                links = item.get("links", [{}])
                image = links[0].get("href") if links else ""
                nasa_items.append({
                    "title": data.get("title", "No Title"),
                    "description": data.get("description", "No Description"),
                    "date_created": data.get("date_created", "No Date"),
                    "image": image
                })
    except Exception:
        nasa_items = []

    try:
        joke_response = requests.get("https://v2.jokeapi.dev/joke/Any")
        joke_json = joke_response.json() if joke_response.status_code == 200 else {}
        if joke_json.get("type") == "single":
            joke = joke_json.get("joke", "No joke found")
        else:
            joke = "{} - {}".format(joke_json.get("setup", ""), joke_json.get("delivery", ""))
    except Exception:
        joke = "No joke available"

    try:
        quote_response = requests.get("https://zenquotes.io/api/random")
        quote_json = quote_response.json() if quote_response.status_code == 200 else []
        if quote_json:
            quote = {"text": quote_json[0].get("q", ""), "author": quote_json[0].get("a", "")}
        else:
            quote = {"text": "No quote available", "author": ""}
    except Exception:
        quote = {"text": "No quote available", "author": ""}
    
    context = {
        "crypto": crypto_data,
        "nasa": nasa_items,
        "joke": joke,
        "quote": quote,
    }
    return render(request, "dashboard/home.html", context)

def refresh_quote(request):
    try:
        quote_response = requests.get("https://zenquotes.io/api/random")
        quote_json = quote_response.json() if quote_response.status_code == 200 else []
        if quote_json:
            quote = {"text": quote_json[0].get("q", ""), "author": quote_json[0].get("a", "")}
        else:
            quote = {"text": "No quote available", "author": ""}
    except Exception:
        quote = {"text": "No quote available", "author": ""}
    return JsonResponse(quote)

def refresh_joke(request):
    try:
        joke_response = requests.get("https://v2.jokeapi.dev/joke/Any")
        joke_json = joke_response.json() if joke_response.status_code == 200 else {}
        if joke_json.get("type") == "single":
            joke = joke_json.get("joke", "No joke found")
        else:
            joke = "{} - {}".format(joke_json.get("setup", ""), joke_json.get("delivery", ""))
    except Exception:
        joke = "No joke available"
    return JsonResponse({"joke": joke})
