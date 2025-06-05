# Import required libraries
import pandas as pd
import plotly.express as px
import os


# Set the base directory path for the data files
base_path = r"C:\Users\HP\Downloads\FASDH25-portfolio3\data\dataframes\tfidf"


# The tf-idf CSV files to process
files = [
    "tfidf-over-0.3.csv",
    "tfidf-over-0.3-len100.csv",
    "tfidf-over-0.3-len200.csv"
]


# Load and process each file into DataFrame
dfs = []
for file in files:
    df = pd.read_csv(os.path.join(base_path, file))


    # Rename columns for consistency
    df.columns = [
        'article1', 'article2', 'cosine_similarity',
        'title1', 'year1', 'month1', 'day1',
        'title2', 'year2', 'month2', 'day2'
    ]


    # Add a column to track the source file
    df['source_file'] = file


    # Convert year, month, day columns to datetime format
    df['date1'] = pd.to_datetime(dict(year=df['year1'], month=df['month1'], day=df['day1']), errors='coerce')
    df['date2'] = pd.to_datetime(dict(year=df['year2'], month=df['month2'], day=df['day2']), errors='coerce')


    # Determine the earlier of the two dates for each article pair
    df['pair_date'] = df[['date1', 'date2']].min(axis=1)


    # Add processed DataFrame to the list
    dfs.append(df)


# Combine all DataFrames into a single one
combined_df = pd.concat(dfs, ignore_index=True)


# Remove rows with missing similarity scores or dates
combined_df.dropna(subset=['cosine_similarity', 'pair_date'], inplace=True)


# Extract the month for temporal trend analysis
combined_df['month'] = combined_df['pair_date'].dt.to_period('M')


# Display summary statistics for similarity scores
print("Summary statistics:\n", combined_df['cosine_similarity'].describe())


# Create Gepgi edge list for network visualization
edges = combined_df[['article1', 'article2', 'cosine_similarity']].copy()
edges.columns = ['Source', 'Target', 'Weight']


# Remove self-loops and filter by similarity threshold
edges = edges[edges['Source'] != edges['Target']]
edges = edges[edges['Weight'] >= 0.4]


# Export edges to CSV
edges.to_csv("edges.csv", index=False)
print("edges.csv created")


# Generate node list with unique article IDs
unique_articles = pd.unique(edges[['Source', 'Target']].values.ravel())
nodes = pd.DataFrame({'Id': unique_articles, 'Label': unique_articles})


# Export nodes to CSV
nodes.to_csv("nodes.csv", index=False)
print("nodes.csv created")


# Identify top 10 most similar article pairs (excluding self-comparisons)
top_similar = combined_df[combined_df['article1'] != combined_df['article2']]
top_similar = top_similar.sort_values(by='cosine_similarity', ascending=False).head(10)
print("Top 10 most similar article pairs:\n", top_similar[['title1', 'title2', 'cosine_similarity']])


# Plot histrogram of similarity scores by dataset
fig = px.histogram(
    combined_df,
    x="cosine_similarity",
    color="source_file",
    nbins=50,
    title="TF-IDF Cosine Similarity Distribution (All Files)",
    labels={"cosine_similarity": "Cosine Similarity Score", "source_file": "Source File"},
    barmode='overlay'
)
fig.update_layout(
    xaxis_title="Cosine Similarity",
    yaxis_title="Frequency",
    bargap=0.2
)
fig.write_html("tf-idf_similarity_distribution.html")
fig.show()


# Claculate average similarity per month for each dataset
monthly_similarity = combined_df.groupby(['month', 'source_file'])['cosine_similarity'].mean().reset_index()


# Convert period to string for plotting
monthly_similarity['month'] = monthly_similarity['month'].astype(str)


# Plot time series of average similarity by month and dataset
fig2 = px.line(
    monthly_similarity,
    x='month',
    y='cosine_similarity',
    color='source_file',
    title='Average TF-IDF Cosine Similarity Over Time',
    labels={'cosine_similarity': 'Average Similarity', 'month': 'Publication Month', 'source_file': 'Dataset'}
)
fig2.update_layout(
    xaxis_title='Month',
    yaxis_title='Average Cosine Similarity'
)
fig2.write_html("tf-idf_similarity_trend.html")
fig2.show()
