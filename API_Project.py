

## 📝 Problem & Solution Statement

###  Problem
Cricket fans often check live scores, but finding **relevant and up-to-date news** about the teams currently playing requires visiting multiple websites.
This makes it time-consuming to stay informed about both **match progress** and **related news updates** in one place.

### Solution
I want to help **cricket fans** to **see live matches and instantly access recent news about the teams playing**  
by combining:  
- **CricAPI** → provides real-time information about ongoing cricket matches (teams, venue, status).  
- **NewsAPI** → provides the latest news articles and headlines about those teams.  

By merging these two APIs, the program allows users to:  
1. **View current matches** with status updates.  
2. **Choose a team** they are interested in.  
3. **Get recent news headlines and links** for that team, without leaving the app.  

This creates a **one-stop tool** where fans can follow matches **and** stay updated with media coverage in real time.

The flowchart uses **CricAPI** and **NewsAPI** to solve the problem of connecting **live cricket matches** with **recent news updates**.

---

#### CricAPI (currentMatches)
- Provides **real-time cricket data**.  
- Returns a list of ongoing or upcoming matches, including:  
  - **Teams**  
  - **Venue**  
  - **Match status**  

---

#### List Live Matches
- The program displays the matches fetched from CricAPI.  
- This allows the user to see which games are **currently active**.  

---

####  User Chooses a Team
- The user selects **one of the teams** they are interested in.  
- This choice becomes the **search query** for NewsAPI.  

---

####  NewsAPI (everything endpoint)
- Takes the selected **team name** as input.  
- Searches for the **latest news articles** related to that team, such as:  
  - Match previews  
  - Interviews  
  - Recent performances  

---

#### Latest News Headlines (Output)
- The program outputs a short list of the **most recent headlines**.  
- Each result includes:  
  - **Title**  
  - **URL link** to the full article  

---
"""

import requests
# --- API Keys ---

CRICKET_API_KEY = "Add API KEY" #cric api
NEWS_API_KEY = "ADD API KEY"         # NewsAPI key

# API 1: Fetch live cricket matches from CricAPI

# Define the API endpoint for current matches
cricket_url = "https://api.cricapi.com/v1/currentMatches"

# Send a GET request to the CricAPI endpoint with API key and offset
# 'params' creates a query string like ?apikey=...&offset=0
resp = requests.get(cricket_url, params={"apikey": CRICKET_API_KEY, "offset": 0})

# ✅ Error handling: check if the request was successful (status code 200 means OK)
if resp.status_code != 200:
    print("⚠️ Error fetching cricket data.")  # Print warning if API request fails
    matches_data = []  # Use an empty list to avoid crashing later
else:
    # Parse the JSON response and extract the "data" field
    # If "data" is missing, default to an empty list
    matches_data = resp.json().get("data", [])

# ✅ Show the first 5 matches for demonstration
print("=== Live Cricket Matches ===")

# Loop through the first 20 matches, using enumerate to number them (1, 2, 3, …)
for i, match in enumerate(matches_data[:20], start=1):
    # Safely get the teams list (e.g., ["India", "Australia"])
    teams = match.get("teams", [])
    # Safely get the venue name (default: "Unknown Venue")
    venue = match.get("venue", "Unknown Venue")
    # Safely get the match status (default: "No status available")
    status = match.get("status", "No status available")

    # Only print the match if there are 2 valid teams
    if len(teams) == 2:
        print(f"{i}. {teams[0]} vs {teams[1]} — {venue} ({status})")

# Fetch cricket news for a test team using NewsAPI


# Define a test team name to search news for
test_team = "India"

# Define the NewsAPI endpoint for searching articles
news_url = "https://newsapi.org/v2/everything"

# Send a GET request to NewsAPI with query parameters
# q        → search query (here: "India cricket")
# apiKey   → required authentication key
# language → restrict results to English
# sortBy   → order by publish time ("publishedAt" = most recent first)
# pageSize → number of articles to fetch (here: 3)
news_resp = requests.get(news_url, params={
    "q": f"{test_team} cricket",
    "apiKey": NEWS_API_KEY,
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 3
})

# ✅ Error handling: if request fails, print warning and set articles = []
if news_resp.status_code != 200:
    print("⚠️ Error fetching news.")
    articles = []
else:
    # Parse the JSON response and extract the "articles" list
    # If "articles" is missing, default to an empty list
    articles = news_resp.json().get("articles", [])

# Print the headlines for the test team
print(f"\n📰 Latest news about {test_team}:")
if articles:
    # Loop through each article and print title + clickable URL
    for art in articles:
        print(f" - {art['title']} ({art['url']})")
else:
    # Fallback if no articles were found
    print("   No news found.")

# 🔗 Step 3: Merge both APIs


# Create an empty list to store all available teams
teams_list = []

# Print header for match listings
print("=== Live Cricket Matches ===")

# Loop through the first 5 matches and show details. We can definitely do more. I am using 5 because it's easy to show the output.
for i, match in enumerate(matches_data[:5], start=1):
    # Extract information safely with defaults if missing
    teams = match.get("teams", [])
    venue = match.get("venue", "Unknown Venue")
    status = match.get("status", "No status available")

    # Only show the match if there are 2 valid teams
    if len(teams) == 2:
        print(f"{i}. {teams[0]} vs {teams[1]} — {venue} ({status})")
        # Add both teams to a flat list for later selection
        teams_list.extend(teams)

# --- Step 4: Ask user which team they want news about ---
print("\nWhich team would you like news about?")
# Number each team option so the user can pick by index
for idx, team in enumerate(teams_list, start=1):
    print(f"{idx}. {team}")

# Take input from user
choice = input("\nEnter the number of the team you want news about: ")

# Validate the input (must be a valid integer and in range)
try:
    team_choice = teams_list[int(choice) - 1]
except (ValueError, IndexError):
    print("⚠️ Invalid choice.")
    team_choice = None

# If a valid team was selected, fetch news for it
if team_choice:
    news_url = "https://newsapi.org/v2/everything"
    news_resp = requests.get(news_url, params={
        "q": f"\"{team_choice}\" AND cricket",   # Build query using selected team and Cricket
        "apiKey": NEWS_API_KEY,          # API key for authentication
        "language": "en",                # Only English articles
        "sortBy": "publishedAt",         # Most recent first
        "pageSize": 5                    # Limit to top 5 headlines
    })

    # ✅ Error handling: check if NewsAPI request worked
    if news_resp.status_code != 200:
        print("⚠️ Error fetching news.")
    else:
        # Extract the list of articles
        articles = news_resp.json().get("articles", [])
        print(f"\n📰 Latest headlines for {team_choice}:")

        # Print the results if found
        if articles:
            for art in articles:
                print(f" - {art['title']} ({art['url']})")
        else:
            # If no articles returned
            print("   No recent news found.")
else:
    # If no valid team was selected
    print("⚠️ No team selected.")

