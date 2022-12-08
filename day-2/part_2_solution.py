'''
The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

    In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
    In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
    In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.

Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
'''

OPPONENT_ROCK = 'A'
OPPONENT_PAPER = 'B'
OPPONENT_SCISSORS = 'C'

ROCK_SCORE = 1
PAPER_SCORE = 2
SCISSORS_SCORE = 3

SHOULD_LOSE = 'X'
SHOULD_DRAW = 'Y'
SHOULD_WIN = 'Z'

MY_OUTCOME_SCORE = {
    SHOULD_LOSE: 0,
    SHOULD_DRAW: 3,
    SHOULD_WIN: 6
}

MY_SHAPE_SCORE = {
    OPPONENT_ROCK: {
        SHOULD_LOSE: SCISSORS_SCORE,
        SHOULD_DRAW: ROCK_SCORE,
        SHOULD_WIN: PAPER_SCORE
    },
    OPPONENT_PAPER: {
        SHOULD_LOSE: ROCK_SCORE,
        SHOULD_DRAW: PAPER_SCORE,
        SHOULD_WIN: SCISSORS_SCORE
    },
    OPPONENT_SCISSORS: {
        SHOULD_LOSE: PAPER_SCORE,
        SHOULD_DRAW: SCISSORS_SCORE,
        SHOULD_WIN: ROCK_SCORE
    }
}

def score(round_line):
    round = round_line.split()
    opponent = round[0]
    outcome = round[1]
    shape_score = MY_SHAPE_SCORE[opponent][outcome]
    outcome_score = MY_OUTCOME_SCORE[outcome]
    return shape_score + outcome_score

if __name__ == '__main__':
    with open('input.txt') as f:
        round_lines = f.readlines()
    total_score = sum(map(lambda round_line: score(round_line), round_lines))
    print(f'part 2 total_score={total_score}')
