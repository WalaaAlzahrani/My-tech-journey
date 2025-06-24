# 🎬 TMDB Movie Data Analysis

Hi! This is one of the first data analysis projects I worked on as a beginner in Python and data.  
I used a real-world dataset from TMDB (The Movie Database) and tried to explore it from different angles — genres, ratings, popularity, revenue, and more. I also added some personal notes, mistakes, and lessons I picked up while doing it.

---

## 📦 Dataset

- 📍 Source: [TMDB Movies Daily Updates (Kaggle)](https://www.kaggle.com/datasets/alanvourch/tmdb-movies-daily-updates/data)
- 📁 Format: Excel (`.xlsx`)
- ⚠️ Not uploaded here because it's a large file.  
  If you're trying to run the code, just download it from Kaggle and place it inside the `data/` folder.

---

## 🚀 What I Tried to Do

- Load and explore a huge movie dataset (~935K movies)
- Clean it up (remove duplicates, handle missing values, fix formats)
- Ask simple but meaningful questions like:
  - Which genres are most common?
  - What years had the most movie releases?
  - Which directors or actors show up most?
  - How does budget relate to revenue or popularity?
- Visualize patterns with charts and plots
- Learn and apply feature engineering (ROI, main genre, etc.)
- Export clean versions of the dataset for future projects

---

## 🧰 Tools I Used

- **Python**
- **Pandas** and **NumPy** for data work
- **Seaborn** and **Matplotlib** for charts
- **Jupyter Notebook** in VSCode
- **Excel (openpyxl)** for loading `.xlsx` files

---

## 🔎 My Analysis Steps

This project went through different phases (I followed them like mini milestones):

1. **Setup + Imports**: Installed required packages and loaded the data (this part was tricky due to environment issues)
2. **Initial Inspection**: Looked at the columns, datatypes, missing values
3. **Cleaning**: Fixed column types, dropped unnecessary rows, filled missing stuff
4. **EDA (Exploratory Data Analysis)**:  
   - Movie counts per year  
   - Most common genres  
   - Top-rated movies  
   - Popularity vs vote count scatter plot  
   - Runtime by genre  
5. **Advanced Analysis**:  
   - Correlation heatmap  
   - Directors & actors ranking  
   - Ratings by genre  
   - Revenue vs budget (with ROI)  
6. **Missing Data Summary**: Posters, runtimes, overviews
7. **Feature Engineering**: Created new columns like `release_decade`, `ROI`, `cast_count`, and `rating_category`
8. **Exported Clean Data**: Saved cleaned versions to `.csv` and `.json`

---

## 📁 Files in This Project

- `mainn.py`: My full code (with notes, comments, and learning points)
- `README.md`: You're reading it!
- `data/TMDB_all_movies.xlsx`: Not included (download from Kaggle)
- `cleaned_tmdb_movies.csv`: Clean dataset I used for analysis. Not included also(you need to run the code to get it)
- `tmdb_clean_export.csv/json`: Filtered and app-ready version
- `top_movies.json`: Top 20 highly rated movies (by vote average)

---

## 💬 Notes & Mistakes I Made

- I had multiple Python versions installed, and at first Jupyter couldn’t find the right environment. Took me a while to figure that out.
- Some columns like `cast` and `overview` had mixed types (strings + others). I added checks or converted them before doing `.split()` or `.strip()`.
- I didn’t use any machine learning here — just focused on data understanding and cleaning.

---

## ✅ Status

This project is done ✅  
No web app yet — just focused on the data side for now.

---

## 📌 If You Want to Try It

1. Clone this repo
2. Download the dataset from Kaggle
3. Put it inside the `data/` folder
4. Run the `mainn.py` script or open it in a Jupyter notebook
5. You can explore or even build on top of it

---

## 📚 What I Learned

- How to clean and explore a large real-world dataset
- How to handle tricky missing data
- How to tell stories using visuals
- How to export and prepare data for future use
- That even small mistakes can teach you a lot!

---

Thanks for checking out my project 🙌  
Feel free to leave suggestions, feedback, or questions!
