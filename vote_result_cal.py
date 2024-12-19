import pandas as pd

df_Y6_8 = pd.read_csv("./data/raw/BI_results_Y6-8.csv")
df_Y9_12 = pd.read_csv("./data/raw/BI_results_Y9-12.csv")

# strip the email addresses
df_Y6_8["Timestamp"] = df_Y6_8["Timestamp"].str.split("@").str[0]
df_Y9_12["Timestamp"] = df_Y9_12["Timestamp"].str.split("@").str[0]

# write to new csv withourt the email addresses
df_Y6_8.to_csv("./data/processed/BI_results_no_emails_Y6-8.csv", index=False)
df_Y9_12.to_csv("./data/processed/BI_results    _no_emails_Y9-12.csv", index=False)

# subset voting categories
df_artwork_Y6_8 = df_Y6_8[["Timestamp"] + [col for col in df_Y6_8.columns if "Artwork" in col]]
df_poetry_Y6_8 = df_Y6_8[["Timestamp"] + [col for col in df_Y6_8.columns if "Poetry" in col]]
df_short_story_Y6_8 = df_Y6_8[["Timestamp"] + [col for col in df_Y6_8.columns if "Short Story" in col]]

df_artwork_Y9_12 = df_Y9_12[["Timestamp"] + [col for col in df_Y9_12.columns if "Artwork" in col]]
df_poetry_Y9_12 = df_Y9_12[["Timestamp"] + [col for col in df_Y9_12.columns if "Poetry" in col]]
df_short_story_Y9_12 = df_Y9_12[["Timestamp"] + [col for col in df_Y9_12.columns if "Short Story" in col]]


def ranked_voting(df, prefix):
    print(f"\nStarting Ranked Voting for {prefix}")
    results = {}
    vote_breakdowns = []
    candidates = [col for col in df.columns if prefix in col]
    print(f"Initial candidates: {candidates}")
    
    df = df.copy()
    
    rank_map = {'1st': 3, '2nd': 2, '3rd': 1}
    for col in candidates:
        df[col] = df[col].map(rank_map)
    
    candidate_points = df[candidates].sum().astype(int)
    vote_breakdowns.append(candidate_points.to_dict())
    
    winner = candidate_points.idxmax()
    results[prefix] = winner
    print(f"Winner found: {winner}")
    
    return results, vote_breakdowns


def print_results(results, vote_breakdowns, method, age_group):
    print(f"\n{'='*80}")
    print(f"{method} Results for {age_group}".center(80))
    print('='*80)
    
    for category in results:
        print(f"\n{category} Category")
        print('-'*40)
        print(f"Winner: {results[category]}")
        print("\nVote Breakdown:")
        
        for round_num, round_votes in enumerate(vote_breakdowns[category], 1):
            total_votes = sum(round_votes.values())
            if total_votes == 0:
                continue
            
            # Sort candidates by votes in descending order
            sorted_votes = sorted(round_votes.items(), key=lambda x: x[1], reverse=True)
            
            # Calculate max lengths for formatting
            max_candidate_len = max(len(str(candidate)) for candidate, _ in sorted_votes)
            max_votes_len = max(len(str(votes)) for _, votes in sorted_votes)
            
            # Print header if first round
            if round_num == 1:
                print(f"{'Candidate':<{max_candidate_len}}  {'Votes':>{max_votes_len}}  Percentage")
                print('-' * (max_candidate_len + max_votes_len + 15))
            
            # Print each candidate's results
            for candidate, votes in sorted_votes:
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                print(f"{candidate:<{max_candidate_len}}  {votes:>{max_votes_len}}  {percentage:>6.1f}%")

# Process and print results for Y6-8
ranked_results_Y6_8 = {
    "Artwork": ranked_voting(df_artwork_Y6_8, "Artwork"),
    "Poetry": ranked_voting(df_poetry_Y6_8, "Poetry"),
    "Short Story": ranked_voting(df_short_story_Y6_8, "Short Story")
}

# Separate results and vote breakdowns
ranked_results_dict_Y6_8 = {k: v[0][k] for k, v in ranked_results_Y6_8.items()}
ranked_breakdowns_Y6_8 = {k: v[1] for k, v in ranked_results_Y6_8.items()}

print_results(ranked_results_dict_Y6_8, ranked_breakdowns_Y6_8, "Ranked Voting", "Y6-8")

# Process and print results for Y9-12
ranked_results_Y9_12 = {
    "Artwork": ranked_voting(df_artwork_Y9_12, "Artwork"),
    "Poetry": ranked_voting(df_poetry_Y9_12, "Poetry"),
    "Short Story": ranked_voting(df_short_story_Y9_12, "Short Story")
}

# Separate results and vote breakdowns
ranked_results_dict_Y9_12 = {k: v[0][k] for k, v in ranked_results_Y9_12.items()}
ranked_breakdowns_Y9_12 = {k: v[1] for k, v in ranked_results_Y9_12.items()}

print_results(ranked_results_dict_Y9_12, ranked_breakdowns_Y9_12, "Ranked Voting", "Y9-12")

# Combine results and breakdowns
combined_results = {
    'Y6-8 Ranked': {
        'Results': ranked_results_dict_Y6_8,
        'Vote Breakdown': ranked_breakdowns_Y6_8
    },
    'Y9-12 Ranked': {
        'Results': ranked_results_dict_Y9_12,
        'Vote Breakdown': ranked_breakdowns_Y9_12
    }
}

# Save detailed results to txt with markdown syntax
with open("./data/final_results.md", "w") as f:
    for age_group, data in combined_results.items():
        f.write(f"# {age_group}\n\n")
        f.write("## Results\n\n")
        for category, winner in data['Results'].items():
            f.write(f"- {category}: {winner}\n")
        f.write("\n## Vote Breakdown\n\n")
        for category, rounds in data['Vote Breakdown'].items():
            f.write(f"### {category}\n\n")
            for round_num, votes in enumerate(rounds, 1):
                f.write(f"#### Round {round_num}\n\n")
                for candidate, vote_count in votes.items():
                    f.write(f"- {candidate}: {vote_count}\n")
                f.write("\n")
        f.write("\n")

# Print summary of winners
print("\n" + "="*80)
print("FINAL WINNERS SUMMARY".center(80))
print("="*80)

for age_group in ["Y6-8", "Y9-12"]:
    print(f"\n{age_group}")
    print("-" * len(age_group))
    
    # Ranked Winners
    ranked_results = combined_results[f'{age_group} Ranked']['Results']
    print("\nRanked Voting:")
    for category, winner in ranked_results.items():
        print(f"  {category:<12}: {winner}")
