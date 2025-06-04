# explore_tfidf_cosine.py
import pandas as pd

# Load the full dataset
df = pd.read_csv("tfidf-over-0.3.csv")

# Preview the first few rows
print(df.head())

# Show basic stats
print(df["similarity"].describe())

# Try filtering: only article pairs with high similarity
high_sim_df = df[df["similarity"] > 0.3]
print(high_sim_df.head())

# Save the filtered version to a file
high_sim_df.to_csv("tfidf-over-0.3.csv", index=False)
