import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("tfidf-over-0.3-len200.csv")

# Create a pivot table (matrix) for heatmap
heatmap_df = df.pivot(index="filename-1", columns="filename-2", values="similarity")

# Fill NaNs with 0 (no similarity)
heatmap_df = heatmap_df.fillna(0)

# Plot the heatmap
fig = px.imshow(heatmap_df,
                labels=dict(x="Target Article", y="Source Article", color="Cosine Similarity"),
                title="TF-IDF Cosine Similarity Heatmap (Articles > 200 words)",
                color_continuous_scale='Blues')

fig.update_layout(height=800, width=800)
fig.write_html("tf-idf-heatmap.html")
fig.show()
