import pandas as pd
import plotly.express as px

# Load the 2-gram dataset
file_path = 'C:/Users/laptop inn/Downloads/FASDH25-portfolio3/data/dataframes/n-grams/2-gram/2-gram-year.csv'
data = pd.read_csv(file_path)

# Define target bigrams (case-insensitive match)
focus_bigrams = ['un resolution', 'cease fire', 'peace process', 'human rights', 'media coverage']
focus_bigrams = [b.lower() for b in focus_bigrams]

# Convert bigram column to lowercase
data['2-gram'] = data['2-gram'].str.lower()

# Filter for selected bigrams only
filtered = data[data['2-gram'].isin(focus_bigrams)].copy()

# Compute total mentions per year for normalization
yearly_totals = filtered.groupby('year')['count-sum'].sum().rename('total_year_mentions')
filtered = filtered.merge(yearly_totals, on='year')
filtered['relative_freq'] = (filtered['count-sum'] / filtered['total_year_mentions']) * 100

# Rename columns for clarity
filtered.rename(columns={'2-gram': 'bigram', 'relative_freq': 'percentage'}, inplace=True)

# Create bar plot (grouped)
fig = px.bar(
    filtered,
    x='year',
    y='percentage',
    color='bigram',
    barmode='group',
    title='Relative Frequency of Selected 2-Grams by Year (%)',
    labels={'percentage': 'Share of Mentions (%)', 'year': 'Year'},
    color_discrete_sequence=px.colors.qualitative.Vivid  # Different color set
)

# Improve layout
fig.update_layout(
    xaxis=dict(dtick=1),
    font=dict(size=13),
    title_font=dict(size=20),
    legend_title='2-Gram Themes',
    plot_bgcolor='rgba(255,255,255,1)'
)

# Show and save
fig.show()
fig.write_html("2gram_normalized_grouped_bar.html")
print("Chart saved as 2gram_normalized_grouped_bar.html")
