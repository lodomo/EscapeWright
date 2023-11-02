import math

def calculate_loading_bar(secs, est_time=60):
    # Ensure inputs are valid to avoid division by zero or negative values
    if est_time <= 0 or secs < 0:
        return "Invalid input parameters"

    raw_ratio = secs / est_time
    
    if raw_ratio <= 0.5:
        # When the ratio is less than or equal to 50%, show real percentage
        return round(raw_ratio * 100)
    else:
        # When the ratio is greater than 50%, slow down the progression
        # Using a logarithmic function to slow down the progress
        return round(50 + (1 - 1 / (1 + (raw_ratio - 0.5) * 10)) * 50)

# Run fake percentage 100 times and show which time is running
# ith: number%
for i in range(100):
    print(f"{i:03}:{calculate_loading_bar(i, 30):03}%", end=' ')
    if i % 10 == 0:
        print()
print()