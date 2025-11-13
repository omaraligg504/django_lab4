import pandas as pd

# Load your CSV file
df = pd.read_csv('data/movies.csv')

# Find all rows that have duplicate movieId values (including the first occurrence)
dupes = df[df['movieId'].duplicated(keep=False)]

print(f"Total rows involved in duplicates: {len(dupes)}")

# Optional: Show the actual duplicates
print(dupes.head(20))  # show first 20 duplicate rows
