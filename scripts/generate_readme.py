import requests
import datetime

USERNAME = "8AdxLDYG0y"
GITHUB = "Shubhampandey7079"

# -------------------------------
# FETCH LEETCODE STATS (NEW API)
# -------------------------------
stats_url = f"https://alfa-leetcode-api.onrender.com/{USERNAME}"

try:
    res = requests.get(stats_url, timeout=10)
    data = res.json()

    total = data.get("totalSolved", 0)
    easy = data.get("easySolved", 0)
    medium = data.get("mediumSolved", 0)
    hard = data.get("hardSolved", 0)
    ranking = data.get("ranking", "N/A")

except:
    total, easy, medium, hard, ranking = 0, 0, 0, 0, "N/A"

# -------------------------------
# FETCH RECENT SUBMISSIONS
# -------------------------------
recent_url = "https://leetcode.com/graphql"

query = {
    "query": """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            title
            titleSlug
            difficulty
            lang
        }
    }
    """,
    "variables": {"username": USERNAME, "limit": 5}
}

headers = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com/",
    "User-Agent": "Mozilla/5.0"
}

recent_problems = []

try:
    res = requests.post(recent_url, json=query, headers=headers, timeout=10)
    data = res.json()
    recent = data.get("data", {}).get("recentAcSubmissionList", [])

    for p in recent:
        recent_problems.append({
            "title": p["title"],
            "link": f"https://leetcode.com/problems/{p['titleSlug']}/",
            "difficulty": p["difficulty"],
            "lang": p["lang"]
        })
except:
    recent_problems = []

# -------------------------------
# PROGRESS BAR
# -------------------------------
def bar(val, total_val, color_hex):
    p = int((val/total_val)*100) if total_val else 0
    return f"![{p}%](https://progress-bar.dev/{p}/?width=400&color={color_hex})"

# -------------------------------
# WRITE README
# -------------------------------
with open("README.md", "w", encoding="utf-8") as f:

    f.write(f"# Hi 👋 I'm Shubham Pandey\n\n")
    f.write(f"## 🚀 LeetCode Stats\n")
    f.write(f"- Total Solved: **{total}**\n")
    f.write(f"- Easy: {easy}\n")
    f.write(f"- Medium: {medium}\n")
    f.write(f"- Hard: {hard}\n")
    f.write(f"- Ranking: {ranking}\n\n")

    f.write("## 📊 Progress\n\n")
    f.write(f"- Easy   {bar(easy, 200, '2ECC71')}\n")
    f.write(f"- Medium {bar(medium, 500, 'F1C40F')}\n")
    f.write(f"- Hard   {bar(hard, 150, 'E74C3C')}\n\n")

    f.write("## 🕒 Recent Submissions\n\n")

    if recent_problems:
        for i, p in enumerate(recent_problems, 1):
            f.write(f"{i}. [{p['title']}]({p['link']}) - {p['difficulty']} ({p['lang']})\n")
    else:
        f.write("No recent submissions found\n")

    f.write("\n---\n")
    now = datetime.datetime.utcnow().strftime("%b %d, %Y %H:%M UTC")
    f.write(f"Last updated: {now}\n")

print("✅ README GENERATED")
