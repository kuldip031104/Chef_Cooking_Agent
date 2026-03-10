import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")


@tool
def fetch_recipe(dish: str):
    """Fetch recipe information from Spoonacular API."""

    try:
        url = "https://api.spoonacular.com/recipes/complexSearch"

        params = {
            "query": dish,
            "number": 1,
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("results"):
            recipe = data["results"][0]

            return {
                "title": recipe["title"],
                "id": recipe["id"]
            }

        return "Recipe not found"

    except Exception as e:
        return f"Error fetching recipe: {str(e)}"