import requests
import json
import csv
from typing import Dict, List
from datetime import datetime
import os

# Get the project root directory (parent of src)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fetch_election_data(election_id: str) -> Dict:
    """Fetch election data from the API."""
    url = f"https://api.qv.geek.sg/election/{election_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_json(data: Dict, filename: str):
    """Save data to JSON file."""
    full_path = os.path.join(PROJECT_ROOT, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_raw_votes_to_csv(data: Dict, filename: str):
    """Save raw voting data to CSV file."""
    full_path = os.path.join(PROJECT_ROOT, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    candidates = data['candidates']
    
    with open(full_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        header = ['Voter ID', 'Vote ID', 'Vote TTL']
        for candidate in candidates:
            header.append(f"Votes for: {candidate['title']}")
        writer.writerow(header)
        
        # Write data
        for vote in data['votes']:
            # Initialize row with voter info
            row = [vote['voter'], vote['id'], vote['ttl']]
            
            # Create a dictionary of votes for this voter
            vote_dict = {v['candidate']: v['vote'] for v in vote['votes']}
            
            # Add votes for each candidate
            for i in range(len(candidates)):
                row.append(vote_dict.get(i, 0))
            
            writer.writerow(row)

def process_votes(data: Dict) -> Dict:
    """Process the voting data and calculate totals."""
    candidates = data['candidates']
    votes = data['votes']
    
    # Initialize vote counts for each candidate
    vote_counts = {i: 0 for i in range(len(candidates))}
    
    # Count votes
    for vote in votes:
        for vote_detail in vote['votes']:
            candidate_idx = vote_detail['candidate']
            vote_value = vote_detail['vote']
            vote_counts[candidate_idx] += vote_value
    
    # Create results
    results = []
    for idx, candidate in enumerate(candidates):
        results.append({
            'title': candidate['title'],
            'description': candidate['description'],
            'total_votes': vote_counts[idx]
        })
    
    return {
        'election_id': data['id'],
        'election_name': data['config']['name'],
        'budget': data['config']['budget'],
        'results': results
    }

def main():
    election_ids = [
        'f3de17cf-af54-40e0-b460-d3c28d691df6',
        '0a9885d5-43b4-4b80-b69f-406092002a38'
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for election_id in election_ids:
        try:
            # Fetch raw data
            raw_data = fetch_election_data(election_id)
            
            # Save raw JSON
            json_filename = f"data/election_{election_id}_raw_{timestamp}.json"
            save_json(raw_data, json_filename)
            print(f"Raw data saved to {json_filename}")
            
            # Save raw votes to CSV
            csv_filename = f"data/election_{election_id}_raw_votes_{timestamp}.csv"
            save_raw_votes_to_csv(raw_data, csv_filename)
            print(f"Raw votes saved to {csv_filename}")
            
            # Process and save processed JSON
            processed_data = process_votes(raw_data)
            processed_json_filename = f"data/election_{election_id}_processed_{timestamp}.json"
            save_json(processed_data, processed_json_filename)
            print(f"Processed data saved to {processed_json_filename}")
            
            # Save CSV
            csv_filename = f"data/election_{election_id}_{timestamp}.csv"
            save_csv(processed_data, csv_filename)
            print(f"CSV data saved to {csv_filename}")
            
            # Print summary
            print(f"\nElection: {processed_data['election_name']}")
            print(f"Budget: {processed_data['budget']}")
            print("\nResults:")
            for result in processed_data['results']:
                print(f"- {result['title']}: {result['total_votes']} votes")
            
        except Exception as e:
            print(f"Error processing election {election_id}: {str(e)}")

if __name__ == "__main__":
    main() 