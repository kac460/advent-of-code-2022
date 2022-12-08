with open('input.txt') as f:
    s = f.read()

reindeers_strings = s.split('\n\n')
reindeers_cal_strings = map(lambda reindeer_string: reindeer_string.split(), reindeers_strings)
highest_cals = [0, 0, 0]
for reindeer_cal_strings in reindeers_cal_strings:
    cals_sum = sum(map(lambda cal_string: int(cal_string), reindeer_cal_strings))
    if highest_cals[0] < cals_sum:
        highest_cals[2] = highest_cals[1]
        highest_cals[1] = highest_cals[0]
        highest_cals[0] = cals_sum
    elif highest_cals[1] < cals_sum:
        highest_cals[2] = highest_cals[1]
        highest_cals[1] = cals_sum
    elif highest_cals[2] < cals_sum:
        highest_cals[2] = cals_sum
print(highest_cals)
print(sum(highest_cals))