with open('input.txt') as f:
    s = f.read()
reindeers_strings = s.split('\n\n')
reindeers_cal_strings = map(lambda reindeer_string: reindeer_string.split(), reindeers_strings)
max_cals = 0
for reindeer_cal_strings in reindeers_cal_strings:
    cals_sum = sum(map(lambda cal_string: int(cal_string), reindeer_cal_strings))
    if cals_sum > max_cals: 
        max_cals = cals_sum
print(max_cals)
