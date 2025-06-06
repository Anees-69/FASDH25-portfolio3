import pandas as pd
import plotly.express as px

# Load the topic model data
df = pd.read_csv("dataframes/topic-model/topic-model.csv")

# Create datetime column
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Remove unassigned topics
df = df[df["Topic"] != -1].copy()

# Remove common stop words
stop_words = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}
for col in ["topic_1", "topic_2", "topic_3", "topic_4"]:
    df[col] = df[col].apply(lambda word: "" if word in stop_words else word)

# Combine top keywords
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)

# Top 3 topics
top_topics = df["Topic"].value_counts().nlargest(3).index
df_top = df[df["Topic"].isin(top_topics)].copy()

# Bar chart: Article counts per topic
topic_counts = df["Topic"].value_counts().reset_index()
topic_counts.columns = ["Topic", "Count"]
fig1 = px.bar(
    topic_counts,
    x="Topic",
    y="Count",
    template="ggplot2",
    color="Topic",
    title="Number of Articles by Topic",
    text_auto=True
)
fig1.update_layout(title_font_size=18)
fig1.show()

# Line chart: Daily topic trend
daily = df_top.groupby(["date", "Topic_Label"]).size().reset_index(name="Count")
fig2 = px.line(
    daily,
    x="date",
    y="Count",
    color="Topic_Label",
    template="plotly_dark",
    title="Daily Trend of Top 3 Topics",
    markers=True
)
fig2.update_layout(title_font_size=18, legend_title_text="Topic")
fig2.show()

# Bar chart: Monthly trend
df_top["month_str"] = df_top["date"].dt.to_period("M").astype(str)
monthly = df_top.groupby(["month_str", "Topic_Label"]).size().reset_index(name="Count")
fig3 = px.bar(
    monthly,
    x="month_str",
    y="Count",
    color="Topic_Label",
    barmode="relative",
    title="Monthly Distribution of Top Topics",
    template="seaborn",
    text_auto=True
)
fig3.update_layout(xaxis_tickangle=45, title_font_size=18)
fig3.show()

# Top 3 keywords per topic
melted = df[["Topic_Label", "topic_1", "topic_2", "topic_3", "topic_4"]].melt(
    id_vars="Topic_Label", value_name="Keyword"
)
top_keywords = (
    melted.groupby(["Topic_Label", "Keyword"]).size()
    .reset_index(name="Freq")
    .sort_values(["Topic_Label", "Freq"], ascending=[True, False])
)
top3_kw_list = []
for label in top_keywords["Topic_Label"].unique():
    top3_kw = top_keywords[top_keywords["Topic_Label"] == label].head(3)
    top3_kw_list.append(top3_kw)
top3_kw_df = pd.concat(top3_kw_list)
top3_kw_df = top3_kw_df[top3_kw_df["Topic_Label"].isin(df_top["Topic_Label"].unique())]

# Horizontal bar: Top 3 keywords
fig4 = px.bar(
    top3_kw_df,
    x="Freq",
    y="Keyword",
    color="Topic_Label",
    orientation="h",
    facet_col="Topic_Label",
    facet_col_wrap=1,
    title="Top 3 Keywords per Topic",
    template="simple_white"
)
fig4.update_layout(title_font_size=18)
fig4.show()

# Articles by Year and Topic (Top 10)
df["year"] = pd.to_datetime(df["date"]).dt.year
grouped = df.groupby(["Topic_Label", "year"]).size().reset_index(name="Count")
top10_topics = grouped.groupby("Topic_Label")["Count"].sum().nlargest(10).index
grouped = grouped[grouped["Topic_Label"].isin(top10_topics)]

fig5 = px.bar(
    grouped,
    x='year',
    y='Count',
    color='Topic_Label',
    title='Articles by Year and Topic',
    template='plotly_white',
    barmode='group',
    text_auto=True
)
fig5.update_layout(title_font_size=18, xaxis_tickangle=0)
fig5.show()
