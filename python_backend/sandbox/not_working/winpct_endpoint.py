import requests
import json
import pandas as pd


def fetch_nba_win_probability(game_id="0021700807"):
    """
    Fetch win probability data from NBA stats API for a specific game

    Parameters:
    game_id (str): NBA Game ID

    Returns:
    dict: JSON response containing win probability data
    """

    # Define the endpoint URL
    url = f"https://stats.nba.com/stats/winprobabilitypbp?GameID={game_id}&RunType=each+second"

    # Set headers to mimic a browser request (NBA API often blocks requests without proper headers)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.nba.com",
        "Referer": "https://www.nba.com/",
    }

    try:
        # Make the request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Optional: Convert to DataFrame for easier analysis
        if data and "resultSets" in data:
            result_sets = data["resultSets"][0]
            headers = result_sets["headers"]
            rows = result_sets["rowSet"]
            df = pd.DataFrame(rows, columns=headers)
            print(f"Successfully fetched data with {len(df)} rows")

        return data

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON response")

    return None


# Example usage
if __name__ == "__main__":
    # Fetch data for game ID 0021700807
    win_prob_data = fetch_nba_win_probability("0022401152")

    breakpoint()
    # Save the data to a JSON file
    if win_prob_data:
        with open("nba_win_probability_data.json", "w") as f:
            json.dump(win_prob_data, f, indent=4)
        print("Data saved to nba_win_probability_data.json")
    else:
        print("Failed to retrieve data")
