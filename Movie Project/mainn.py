#_________2.1 importing libraries :)___________#
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Jupyter settings
%matplotlib inline
sns.set(style="whitegrid")


#_________2.2 loading the data ________________#
df = pd.read_excel("data/TMDB_all_movies.xlsx", engine='openpyxl')
df.head()


#_________2.3 Overview of the dataset__________#
df.info()
df.describe()
df.columns
df.isnull().sum()


#_________3.1 Remove duplicates________________#
df.duplicated().sum()  # Check for duplicates
df = df.drop_duplicates()


#_________3.2 Handle missing values____________#
df.isnull().sum().sort_values(ascending=False) #here i check which columns are missing

# Drop rows with missing title or release date (essential for analysis)
df = df.dropna(subset=['title', 'release_date'])

# Fill optional columns
df['tagline'] = df['tagline'].fillna('No tagline')
df['overview'] = df['overview'].fillna('No overview')
df['runtime'] = df['runtime'].fillna(df['runtime'].median())


#_________3.3 Convert dates & extract year_____#
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year #created a new column extracted from the release_date


#_________3.4 Fix data types___________________#
#I want to ensure correct types for numeric fields
num_cols = ['vote_average', 'vote_count', 'revenue', 'runtime', 'budget',
            'popularity', 'imdb_rating', 'imdb_votes']

df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')


#________4.1 Movies released per year__________#
# Count number of movies released per year
movies_per_year = df['release_year'].value_counts().sort_index()

# Plot
plt.figure(figsize=(12, 6))
sns.lineplot(x=movies_per_year.index, y=movies_per_year.values, marker='o')
plt.title('Number of Movies Released per Year')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.show()

#________4.2 Most common movie genres__________#
from collections import Counter

genre_counts = Counter()

# Split genre strings and count occurrences
df['genres'].dropna().apply(lambda x: genre_counts.update(x.split(', ')))

# Convert the counts into a DataFrame
genre_df = pd.DataFrame.from_dict(genre_counts, orient='index', columns=['count'])
genre_df = genre_df.sort_values(by='count', ascending=False)

# Plot the top genres
plt.figure(figsize=(10, 6))
sns.barplot(x=genre_df['count'], y=genre_df.index)
plt.title('Most Common Movie Genres')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.tight_layout()
plt.show()


#________4.3 Top Rated Movies (Vote Average + Threshold)#
# Filter to only include movies with significant number of votes
top_rated = df[df['vote_count'] > 100].sort_values(by='vote_average', ascending=False).head(10)

# Display top 10 movies
top_rated[['title', 'vote_average', 'vote_count']]


#________4.4 Popularity vs Vote Count__________#
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='vote_count', y='popularity', alpha=0.5)
plt.title('Popularity vs Vote Count')
plt.xlabel('Vote Count')
plt.ylabel('Popularity')
plt.tight_layout()
plt.show()


#________4.5 Average runtime by genre__________#
# Create a list of (genre, runtime) pairs
genre_runtimes = []

for _, row in df[['genres', 'runtime']].dropna().iterrows():
    genres = row['genres'].split(', ')
    for genre in genres:
        genre_runtimes.append((genre, row['runtime']))

# Create DataFrame from the list
genre_runtime_df = pd.DataFrame(genre_runtimes, columns=['genre', 'runtime'])

# Compute average runtime per genre
avg_runtime = genre_runtime_df.groupby('genre')['runtime'].mean().sort_values(ascending=False)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_runtime.values, y=avg_runtime.index)
plt.title('Average Runtime by Genre')
plt.xlabel('Average Runtime (minutes)')
plt.ylabel('Genre')
plt.tight_layout()
plt.show()


#________5.1 Correlation between budget, revenue, popularity, and votes#
# Select numerical features of interest
corr_features = ['budget', 'revenue', 'popularity', 'vote_average', 'vote_count']

# Compute correlation matrix
corr_matrix = df[corr_features].corr()

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()


#________5.2 Most frequent directors and their average ratings#
# Count top 10 directors by number of movies
top_directors = df['director'].value_counts().head(10).index

# Filter dataset to only top directors
top_director_df = df[df['director'].isin(top_directors)]

# Group by director and compute average vote
director_ratings = top_director_df.groupby('director')['vote_average'].mean().sort_values(ascending=False)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=director_ratings.values, y=director_ratings.index)
plt.title('Top Directors by Average Rating')
plt.xlabel('Average Vote')
plt.ylabel('Director')
plt.tight_layout()
plt.show()


#________5.3 Most frequent actors/actresses____#
# Create a Counter for cast frequency
cast_counts = Counter()

#df['cast'].dropna().apply(lambda x: cast_counts.update(x.split(', ')[:5]))  # limit to top 5 cast members per movie
#^ this was The original code and it couldn't work because I discovered the cast column contains both string and integer values. 
# I had to modify the code to handle string values only, since the split method only works with strings.

# first i have to Safely handle non-string values and count top 5 cast members per movie
from collections import Counter

cast_counts = Counter()

df['cast'].dropna().apply(
    lambda x: cast_counts.update(str(x).split(', ')[:5])
)


# Convert to DataFrame
cast_df = pd.DataFrame(cast_counts.most_common(15), columns=['Actor', 'Appearances'])

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Appearances', y='Actor', data=cast_df)
plt.title('Most Frequent Actors/Actresses')
plt.tight_layout()
plt.show()



#_________5.4 Average movie rating by genre____#
# Create a list of (genre, vote_average) pairs
genre_votes = []

for _, row in df[['genres', 'vote_average']].dropna().iterrows():
    genres = row['genres'].split(', ')
    for genre in genres:
        genre_votes.append((genre, row['vote_average']))

# Convert to DataFrame
genre_rating_df = pd.DataFrame(genre_votes, columns=['genre', 'vote_average'])

# Compute average rating per genre
avg_genre_rating = genre_rating_df.groupby('genre')['vote_average'].mean().sort_values(ascending=False)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_genre_rating.values, y=avg_genre_rating.index)
plt.title('Average Movie Rating by Genre')
plt.xlabel('Average Rating')
plt.ylabel('Genre')
plt.tight_layout()
plt.show()


#________5.5 Revenue vs Budget (rturn on ivestment)#
# Filter to remove outliers
filtered_df = df[(df['budget'] > 1e6) & (df['revenue'] > 1e6)]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_df, x='budget', y='revenue', alpha=0.6)
plt.title('Revenue vs Budget')
plt.xlabel('Budget')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()


#___Bonus Step :) "Top Movies" Summary Table___#
top_movies_export = df[df['vote_count'] > 100].sort_values(by='vote_average', ascending=False).head(20)
top_movies_export = top_movies_export[['title', 'vote_average', 'genres', 'release_date', 'poster_path']]

# Save to JSON
top_movies_export.to_json('top_movies.json', orient='records', lines=True)


#________6.1 Overview of Missing Data ________#
# Calculate missing values count and percentage
missing_count = df.isnull().sum()
missing_percent = (missing_count / len(df)) * 100

# Combine into one dataframe
missing_df = pd.DataFrame({
    'Missing Count' : missing_count,
    'Missing %' : missing_percent 
}).sort_values(by='Missing %', ascending=False)

# show columns with missing data
missing_df[missing_df['Missing Count']>0]


#_______6.2 How many movies are missing poster images?#
# Count missing posters
missing_posters = df['poster_path'].isnull().sum()
total_movies = len(df)

print(f"Missing Posters: {missing_posters} out of {total_movies} ({(missing_posters / total_movies) * 100:.2f}%)")


#________6.3 movies with empty overviews (or very short descriptions)#
# Count how many movies have overviews missing or very short
missing_overviews = df['overview'].isnull().sum()

# I'm converting the 'overview' column to string type here.
# I hit an 'AttributeError' because some entries weren't strings (like datetime objects),
# and methods like `.strip()` only work on strings.
# This step makes sure everything in the column is treated as text, so I can safely perform string operations on it
df['overview'] = df['overview'].astype(str)
very_short_overviews = df['overview'].dropna().apply(lambda x: len(x.strip()) < 15).sum()

print(f"Missing Overviews: {missing_overviews}")
print(f"Very Short Overviews (<15 characters): {very_short_overviews}")


#________6.4 Movies with Missing or Unusually Short Runtimes#
# Check how many runtimes are missing or below 30 minutes
missing_runtime = df['runtime'].isnull().sum()
short_runtime = df['runtime'].dropna().apply(lambda x: x < 30).sum()

print(f"Missing Runtimes: {missing_runtime}")
print(f"Movies with Runtime < 30 min: {short_runtime}")


#________PHASE 7 - Feature Engineering_________#

# 1. Release Year (from release_date)
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year

# 2. Release Decade
df['release_decade'] = (df['release_year'] // 10) * 10

# 3. ROI (Return on Investment)
df['ROI'] = df.apply(
    lambda row: row['revenue'] / row['budget'] if row['budget'] > 0 else None,
    axis=1
)

# 4. Has Poster & Has Overview flags
df['has_poster'] = df['poster_path'].notna() & (df['poster_path'].str.strip() != "")
df['has_overview'] = df['overview'].notna() & (df['overview'].str.strip() != "")

# 5. Main Genre (first genre in the list)
df['main_genre'] = df['genres'].dropna().apply(lambda x: x.split(', ')[0] if isinstance(x, str) else None)

# 6. Cast Count
df['cast_count'] = df['cast'].apply(lambda x: len(str(x).split(', ')) if pd.notna(x) else 0)

# 7. Rating Category (High: ≥7, Medium: 5-6.9, Low: <5)
def categorize_rating(vote):
    if vote >= 7:
        return 'High'
    elif vote >= 5:
        return 'Medium'
    else:
        return 'Low'

df['rating_category'] = df['vote_average'].apply(categorize_rating)

#Check the new columna
df[['release_year', 'release_decade', 'ROI', 'has_poster', 'has_overview', 'main_genre', 'cast_count', 'rating_category']].head()


#________8.1 Select the relevant columns_______#
columns_to_export = [
    'id', 'title', 'release_date', 'vote_average', 'vote_count',
    'popularity', 'genres', 'overview', 'poster_path',
    'cast', 'director', 'runtime', 'original_language'
]

# Create a filtered DataFrame with selected columns and no major missing data
clean_export_df = df[columns_to_export].dropna(subset=['title', 'genres', 'poster_path', 'overview'])

# filter by popularity or vote count to reduce size for frontend use
clean_export_df = clean_export_df[clean_export_df['vote_count'] > 100]


#________8.2 Save as CSV and JSON______________#
# Save to CSV
clean_export_df.to_csv('tmdb_clean_export.csv', index=False)

# Save to JSON (records format = list of dicts)
clean_export_df.to_json('tmdb_clean_export.json', orient='records', lines=False)


#________9.1 Review key columns to keep________#
final_columns = [
    'id', 'title', 'release_date', 'release_year', 'genres',
    'vote_average', 'vote_count', 'popularity', 'runtime',
    'overview', 'tagline', 'poster_path', 'cast', 'director'
]

df_final = df[final_columns].dropna(subset=['title', 'genres', 'release_date', 'poster_path'])


#________9.2 Final checks (Duplicates, Missing)#
# Drop duplicates if any
df_final.drop_duplicates(subset='id', inplace=True)

# Check for any remaining missing values
print(df_final.isnull().sum())


#_________9.3 Save cleaned dataset to CSV______#
df_final.to_csv('cleaned_tmdb_movies.csv', index=False)

df_final.to_excel('cleaned_tmdb_movies.xlsx', index=False)

