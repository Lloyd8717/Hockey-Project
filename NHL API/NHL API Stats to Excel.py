import requests
import pandas as pd

# Function to fetch data for a given season
def fetch_data_for_season(season_id):
    base_url = "https://api.nhle.com/stats/rest/en/skater/summary"
    params = {
        "isAggregate": "false",
        "isGame": "false",
        "sort": '[{"property":"goals","direction":"DESC"},{"property":"playerId","direction":"ASC"}]',
        "cayenneExp": f"gameTypeId=2 and seasonId={season_id}",
        "start": 0,
        "limit": 100
    }
    
    all_results = []
    while True:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data for season {season_id}: {response.status_code}")
            break
        
        data = response.json()
        results = data.get('data', [])
        
        if not results:
            print(f"No data found for season {season_id}")
            break
        
        all_results.extend(results)
        
        if len(results) < params['limit']:
            break
        
        params['start'] += params['limit']
    
    return all_results

# Fetch seasons from 1918 to 2024
all_seasons_data = []
for year in range(1918, 2025):
    if year == 2004:  # Skip the 2004-2005 season
        continue
    
    season_id = f"{year}{year + 1}"
    print(f"Fetching data for season {season_id}...")
    season_data = fetch_data_for_season(season_id)
    if season_data:
        all_seasons_data.extend(season_data)
    else:
        print(f"No data collected for season {season_id}")

# Check if any data was fetched
if not all_seasons_data:
    print("No data was fetched for any of the specified seasons.")
else:
    # Convert the accumulated data to a DataFrame
    df = pd.DataFrame(all_seasons_data)

    # Reorder columns to have 'skaterFullName' as the first column
    df = df.reindex(columns=['skaterFullName'] + [col for col in df.columns if col != 'skaterFullName'])

    # Save to Excel
    excel_file = "nhl_player_stats_1918_to_2024.xlsx"
    df.to_excel(excel_file, index=False)

    print(f"Data saved to {excel_file}")

