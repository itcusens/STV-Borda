import random

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

def count_votes(votes, candidates, no_seats):
    round_scores = []
    for no_seat in range(no_seats):
        round_score = {}
        copy_candidates = candidates.copy()
        if len(round_scores) > 0:
            last_round_score = round_scores[-1]
            worst_candidate = min(last_round_score.items(), key=lambda x: (x[1][1], x[1][0]))[0]
            copy_candidates.remove(worst_candidate)
        # Count the votes for each candidate
        for candidate in copy_candidates:
            total_score = 0
            no_firsts = 0
            for vote in votes:
                if vote[candidate] == len(candidates) - no_seat:
                    no_firsts += 1
                total_score += vote[candidate]
                
            candidate_score = (total_score, no_firsts)
            round_score[candidate] = candidate_score
        round_scores.append(round_score)
    return round_scores
            
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
    print(votes)
    print(round_scores[0])

if __name__ == "__main__":
    main()
