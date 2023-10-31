import math

def fake_percentage(x):
    if x < 0:
        return 0
    elif x < 10:
        # Linear increment to 50% in 10 seconds
        percentage = 5 * x
    elif x < 60:
        # Increment slower from 50% to 95% in the next 50 seconds
        percentage = 50 + 0.9 * (x - 10)
    else:
        # Asymptotically approach 99% after 60 seconds
        percentage = 95 + 4 * (1 - math.exp(-(x - 60) / 10))

    # Cap the percentage at 99%
    percentage = min(99, percentage)
    return round(percentage, 2)

# Run fake percentage 100 times and show which time is running
# ith: number%
for i in range(100):
    print(f"{i}th: {fake_percentage(i)}%")