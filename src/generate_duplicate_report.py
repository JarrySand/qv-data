import csv
import glob
from collections import defaultdict
from typing import Dict, List, Set
from datetime import datetime
import os

# Get the project root directory (parent of src)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_duplicates(csv_file: str) -> Dict[str, List[Dict]]:
    """Check for duplicate voter IDs in a CSV file and return detailed vote information."""
    voter_votes = defaultdict(list)  # voter_id -> list of vote details
    
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
    
    # Find duplicates
    duplicates = {
        voter_id: votes 
        for voter_id, votes in voter_votes.items() 
        if len(votes) > 1
    }
    
    return duplicates

def generate_markdown_report(duplicates: Dict[str, List[Dict]], election_name: str) -> str:
    """Generate markdown report for duplicate votes."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# 重複投票レポート: {election_name}
生成日時: {timestamp}

## 概要
- 重複投票者数: {len(duplicates)}人
- 総投票数: {sum(len(votes) for votes in duplicates.values())}票

## 重複投票の詳細
"""
    
    for voter_id, votes in duplicates.items():
        report += f"\n### 投票者ID: {voter_id}\n"
        report += f"投票回数: {len(votes)}回\n\n"
        
        for i, vote in enumerate(votes, 1):
            report += f"#### 投票 {i}\n"
            report += f"- 投票ID: {vote['vote_id']}\n"
            report += f"- TTL: {vote['ttl']}\n"
            report += "- 投票内容:\n"
            for candidate, vote_count in vote['votes'].items():
                if int(vote_count) > 0:  # 0票は表示しない
                    report += f"  - {candidate}: {vote_count}票\n"
            report += "\n"
    
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
        duplicates = check_duplicates(csv_file)
        
        if duplicates:
            # Extract election name from filename
            election_name = os.path.basename(csv_file).split('_')[1]
            
            # Generate report
            report = generate_markdown_report(duplicates, election_name)
            
            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = os.path.join(PROJECT_ROOT, "report", f"duplicate_votes_{election_name}_{timestamp}.md")
            os.makedirs(os.path.dirname(report_filename), exist_ok=True)
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {report_filename}")
        else:
            print(f"No duplicates found in {csv_file}")

if __name__ == "__main__":
    main() 