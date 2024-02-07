booked_days = [8, 9, 10, 11, 12, 13, 24, 25, 26]

day_costs = [
 ('Tuesday', 2100),
 ('Wednesday', 2100),
 ('Thursday', 2100),
 ('Friday', 2850),
 ('Saturday', 2850),
 ('Sunday', 2850),
 ('Monday', 2100),
]
week_days = len(day_costs)

print(sum(day_costs[(day - 1) % week_days][1] for day in booked_days))