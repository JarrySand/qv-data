import csv
import glob
from collections import defaultdict
from typing import Dict, List, Set
import os

def check_duplicates(csv_file: str) -> Dict[str, List[str]]:
    """Check for duplicate voter IDs in a CSV file."""
    voter_votes = defaultdict(list)  # voter_id -> list of vote_ids
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            voter_id = row['Voter ID']
            vote_id = row['Vote ID']
            voter_votes[voter_id].append(vote_id)
    
    # Find duplicates
    duplicates = {
        voter_id: vote_ids 
        for voter_id, vote_ids in voter_votes.items() 
        if len(vote_ids) > 1
    }
    
    return duplicates

def main():
    # Find all CSV files
    csv_files = glob.glob("data/election_*_raw_votes_*.csv")
    
    if not csv_files:
        print("No CSV files found!")
        return
    
    for csv_file in csv_files:
        print(f"\nChecking {csv_file}...")
        duplicates = check_duplicates(csv_file)
        
        if duplicates:
            print(f"Found {len(duplicates)} voters with duplicate votes:")
            for voter_id, vote_ids in duplicates.items():
                print(f"\nVoter ID: {voter_id}")
                print(f"Number of votes: {len(vote_ids)}")
                print("Vote IDs:")
                for vote_id in vote_ids:
                    print(f"  - {vote_id}")
        else:
            print("No duplicate votes found.")

if __name__ == "__main__":
    main() 