'''
Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

What would your total score be if everything goes exactly according to your strategy guide?
'''
ME_ROCK = 'X'
ME_PAPER = 'Y'
ME_SCISSORS = 'Z'
SHAPE_SCORES = {
    ME_ROCK: 1,  # Rock
    ME_PAPER: 2,  # Paper
    ME_SCISSORS: 3,  # Scissors
}

OPPONENT_ROCK = 'A'
OPPONENT_PAPER = 'B'
OPPONENT_SCISSORS = 'C'

WIN = 6
DRAW = 3
LOSE = 0
PART_1_MATCHUPS = {
    OPPONENT_ROCK: {
        ME_ROCK: DRAW,
        ME_PAPER: WIN,
        ME_SCISSORS: LOSE,
    },
    OPPONENT_PAPER: {
        ME_ROCK: LOSE,
        ME_PAPER: DRAW,
        ME_SCISSORS: WIN,
    },
    OPPONENT_SCISSORS: {
        ME_ROCK: WIN,
        ME_PAPER: LOSE,
        ME_SCISSORS: DRAW
    }
}

def score(round):
    round = round.split()
    opponent = round[0]
    me = round[1]
    return SHAPE_SCORES[me] + PART_1_MATCHUPS[opponent][me]

if __name__ == '__main__':
    with open('input.txt') as f:
        rounds = f.readlines()

    total_score = sum(map(lambda round: score(round), rounds))
    print(f'part 1 - total_score following strategy guide: {total_score}')