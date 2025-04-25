import random
from typing import Tuple
import csv
# List of common first names and last names to generate random combinations
first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles',
               'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']


def generate_votes(candidates, no_voters):
    # Generate a list of random votes for each candidate
    votes = []
    for point in range(no_voters):
        dummy_candidates = candidates.copy()
        vote = {}
        while len(dummy_candidates) > 0:
            candidate = random.choice(dummy_candidates)
            vote[candidate] = len(dummy_candidates) - 1
            dummy_candidates.remove(candidate)
        votes.append(vote)
    return votes

# buses is a list of tuples (procent_of_voters, no_candidates for the bus)
# def generate_buses_and_random(candidates, no_voters, buses: list[Tuple[float, int]]):
#     votes = []
#     for bus in buses:
#         candidates_for_bus = random.sample(candidates, bus[1])
#         no_voters_for_bus = int(no_voters * bus[0])
#         voters_for_bus = random.sample(range(no_voters), no_voters_for_bus)
#         score = 30
#         for voter in voters_for_bus:
#             vote = {}

def count_votes(votes, candidates, no_seats):
    round_scores = []
    worst_candidates = []
    for no_round in range(len(candidates) - no_seats + 1):
        round_score = {}
        copy_candidates = candidates.copy()
        if len(round_scores) > 0:
            last_round_score = round_scores[-1]
            worst_candidate = min(last_round_score.items(), key=lambda x: (x[1][1], x[1][0]))[0]
            worst_candidates.append(worst_candidate)
        for worst_candidate in worst_candidates:
            copy_candidates.remove(worst_candidate)
        print(no_round, worst_candidates, copy_candidates)
        # Count the votes for each candidate
        for candidate in copy_candidates:
            total_score = 0
            no_firsts = 0
            for vote in votes:
                total_score += vote[candidate]
                
            for vote in votes:
                sorted_vote = sorted(vote.items(), key=lambda x: x[1], reverse=True)
                for first_candidate, _ in sorted_vote:
                    if first_candidate == candidate:
                        no_firsts += 1
                        break
                    elif first_candidate in worst_candidates:
                        continue
                    else:
                        break                    
        
            candidate_score = (total_score, no_firsts)
            round_score[candidate] = candidate_score
        round_scores.append(round_score)
    return round_scores

def from_list_to_table(votes_list, candidates):
    candidates_table = {}
    for candidate in candidates:
        candidates_table[candidate] = []
    for vote in votes_list:
        for candidate in candidates:
            candidates_table[candidate].append(len(candidates) - vote[candidate])
    return candidates_table
        
        
def to_csv(votes_list, candidates):
    candidates_table = from_list_to_table(votes_list, candidates)
    with open('votes.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Buletinul de vot:'] + list(range(1, len(votes_list) + 1)))
        for candidate in candidates:
            writer.writerow([candidate] + candidates_table[candidate])
    

def main():
    # Generate 31 unique random full names
    no_candidates = int(input("Enter the number of candidates: "))
    no_seats = int(input("Enter the number of seats: "))
    no_voters = int(input("Enter the number of voters: "))
    
    candidates = []
    while len(candidates) < no_candidates:
        first = random.choice(first_names)
        last = random.choice(last_names)
        full_name = f"{first} {last}"
        if full_name not in candidates:  # Ensure no duplicate names
            candidates.append(full_name)

    # Count the votes for each candidate
    votes = generate_votes(candidates, no_voters)

    # Count the votes for each candidate
    round_scores = count_votes(votes, candidates, no_seats)
    for vote in votes:
        print(vote)
    for i, round_score in enumerate(round_scores):
        print(f"Runda {i+1}:")
        for candidate, score in round_score.items():
            print(f"{candidate}: {score[0]} {score[1]}")
    to_csv(votes, candidates)

if __name__ == "__main__":
    main()
