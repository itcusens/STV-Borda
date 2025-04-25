import random
from typing import Tuple
import csv
from copy import deepcopy
# List of common first names and last names to generate random combinations
first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles',
               'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

def generate_votes(candidates, no_voters):
    votes = []
    for i in range(no_voters):
        vote = random.sample(candidates, len(candidates))
        votes.append(vote)
    return votes

def remove_worst_candidate(votes, round_score):
    worst_candidate = min(round_score.items(), key=lambda x: (x[1][0], x[1][1]))[0]
    print(worst_candidate)
    new_votes = []
    for vote in votes:
        vote.remove(worst_candidate)
        new_votes.append(vote)
    return new_votes, worst_candidate

def count_round_scores(votes, candidates, candidates_removed):
    candidates_votes = {}
    for candidate in candidates:
        if candidate not in candidates_removed:
            candidates_votes[candidate] = [0, 0]
    for vote in votes:
        for i, candidate in enumerate(vote):
            candidates_votes[candidate][0] += len(candidates) - i
            if i == 0:
                candidates_votes[candidate][1] += 1
    return candidates_votes
    
def count_votes(votes, candidates, no_seats):
    round_scores = []
    votes_history = []
    candidates_removed = []
    for i in range(no_seats):
        print(i, votes)
        votes_history.append(deepcopy(votes))
        round_score = count_round_scores(votes, candidates, candidates_removed)
        round_scores.append(round_score)
        print(round_score)
        votes, worst_candidate = remove_worst_candidate(votes, round_score)
        print(votes)
        candidates_removed.append(worst_candidate)
    return round_scores, votes_history, candidates_removed

def to_csv(round_scores, votes_history, candidates, candidates_removed):
    print(votes_history)
    with open('borda.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Buletinul de vot:'] + list(range(1, len(votes_history[0]) + 1)))
        for candidate in candidates:
            writer.writerow([candidate] + [votes_history[0][i].index(candidate) + 1 for i in range(len(votes_history[0]))])
        
    with open('borda_round_scores.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Candidat'] + ['Runda {}'.format(i+1) for i in range(len(round_scores))])
        round_scores_list = []
        for i, round_score in enumerate(round_scores):
            round_score_list = []
            for candidate in candidates:
                if candidate in round_score:
                    round_score_list.append((candidate, round_score[candidate][0], round_score[candidate][1]))
                else:
                    round_score_list.append((candidate, 0, 0))
            
            # Sort the round score list by score (descending) and then by number of first places (descending)
            round_score_list.sort(key=lambda x: (x[1], x[2]))
            round_score_list.reverse()
            round_scores_list.append(round_score_list)
        
        for candidate, _, _ in round_scores_list[0]:
            candidate_scores = []
            for round_score_list in round_scores_list:
                for candidate_name, score, firsts in round_score_list:
                    if candidate_name == candidate:
                        candidate_scores.append((score, firsts))
            writer.writerow([candidate] + candidate_scores)
                        
        
        
def main():
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
    
    votes = generate_votes(candidates, no_voters)
    
    round_scores, votes_history, candidates_removed = count_votes(votes, candidates, no_seats)
    print(candidates)
    to_csv(round_scores, votes_history, candidates, candidates_removed)
    

if __name__ == "__main__":
    main()
