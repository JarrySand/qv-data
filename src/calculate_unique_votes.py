import csv
import glob
from collections import defaultdict
from typing import Dict, List, Set
from datetime import datetime
import os

# Get the project root directory (parent of src)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def analyze_votes(csv_file: str) -> Dict:
    """Analyze votes in a CSV file and return statistics."""
    voter_votes = defaultdict(list)  # voter_id -> list of vote details
    total_votes = 0
    total_voters = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            voter_id = row['Voter ID']
            vote_details = {
                'vote_id': row['Vote ID'],
                'ttl': row['Vote TTL'],
                'votes': {k: v for k, v in row.items() if k.startswith('Votes for:')}
            }
            voter_votes[voter_id].append(vote_details)
            total_votes += 1
    
    # Count unique voters and duplicate votes
    unique_voters = len(voter_votes)
    duplicate_voters = sum(1 for votes in voter_votes.values() if len(votes) > 1)
    duplicate_votes = sum(len(votes) - 1 for votes in voter_votes.values() if len(votes) > 1)
    
    # Calculate votes after removing duplicates (keeping only the latest vote)
    unique_votes = 0
    for votes in voter_votes.values():
        if len(votes) > 1:
            # Sort by TTL (timestamp) in descending order and take the first one
            latest_vote = sorted(votes, key=lambda x: int(x['ttl']), reverse=True)[0]
            unique_votes += 1
        else:
            unique_votes += 1
    
    return {
        'total_votes': total_votes,
        'unique_voters': unique_voters,
        'duplicate_voters': duplicate_voters,
        'duplicate_votes': duplicate_votes,
        'unique_votes': unique_votes
    }

def generate_markdown_report(stats: Dict, election_name: str) -> str:
    """Generate markdown report for vote statistics."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# 投票統計レポート: {election_name}
生成日時: {timestamp}

## 投票統計
- 総投票数: {stats['total_votes']}票
- 重複を除いた投票数: {stats['unique_votes']}票
- 重複投票数: {stats['duplicate_votes']}票

## 投票者統計
- 総投票者数: {stats['unique_voters']}人
- 重複投票者数: {stats['duplicate_voters']}人

## 重複の影響
- 重複による投票数の増加率: {(stats['duplicate_votes'] / stats['unique_votes'] * 100):.1f}%
"""
    
    return report

def main():
    # Find all CSV files
    csv_pattern = os.path.join(PROJECT_ROOT, "data", "election_*_raw_votes_*.csv")
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print("No CSV files found!")
        return
    
    for csv_file in csv_files:
        print(f"Processing {csv_file}...")
        stats = analyze_votes(csv_file)
        
        # Extract election name from filename
        election_name = os.path.basename(csv_file).split('_')[1]
        
        # Generate report
        report = generate_markdown_report(stats, election_name)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = os.path.join(PROJECT_ROOT, "report", f"vote_statistics_{election_name}_{timestamp}.md")
        os.makedirs(os.path.dirname(report_filename), exist_ok=True)
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to {report_filename}")
        
        # Print summary
        print(f"\nSummary for {election_name}:")
        print(f"Total votes: {stats['total_votes']}")
        print(f"Unique votes (after removing duplicates): {stats['unique_votes']}")
        print(f"Duplicate votes: {stats['duplicate_votes']}")
        print(f"Total voters: {stats['unique_voters']}")
        print(f"Voters with duplicates: {stats['duplicate_voters']}")

if __name__ == "__main__":
    main() 