Authour: Tejaswi
import pandas as pd
import numpy as np

# --- 1. Data Generation (Simulating Raw Student Data) ---
# In a real project, you would load data from a database, API, or files.
# Example: df = pd.read_csv('raw_student_data.csv')

print("--- Generating Sample Student Data ---")
data = {
    'StudentID': range(101, 150),
    'Gender': np.random.choice(['Male', 'Female'], 20),
    'Major': np.random.choice(['Computer Science', 'IT', 'Data Science', 'Engineering'], 20),
    'Semester': np.random.choice(['Fall 2023', 'Spring 2024', 'Fall 2024'], 20),
    'Midterm_Score': np.random.randint(50, 100, 20),
    'Final_Score': np.random.randint(55, 98, 20),
    'Attendance_Rate_Percent': np.random.randint(70, 100, 20),
    'Participation_Score': np.random.randint(1, 10, 20),
    'Project_Score': np.random.randint(60, 100, 20)
}
df = pd.DataFrame(data)

# Introduce some missing values for demonstration of cleaning
df.loc[[2, 5], 'Midterm_Score'] = np.nan
df.loc[[10, 15], 'Final_Score'] = np.nan
df.loc[7, 'Participation_Score'] = -5 # Invalid value

print("\n--- Raw Data Sample ---")
print(df.head())
print(f"\nShape of raw data: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")

# --- 2. Data Cleaning and Transformation ---
print("\n--- Cleaning and Transforming Data ---")

# Handle missing values: Fill missing scores with the mean score for their respective column
df['Midterm_Score'].fillna(df['Midterm_Score'].mean(), inplace=True)
df['Final_Score'].fillna(df['Final_Score'].mean(), inplace=True)
print("Missing scores imputed with column means.")

# Handle invalid values: Replace negative participation scores with 0
df['Participation_Score'] = np.where(df['Participation_Score'] < 0, 0, df['Participation_Score'])
print("Invalid participation scores (negative) corrected to 0.")

# Create a new calculated column: 'Overall_Score' (Weighted Average)
# Assuming weights: Midterm (30%), Final (40%), Project (20%), Participation (10%)
df['Overall_Score'] = (
    df['Midterm_Score'] * 0.30 +
    df['Final_Score'] * 0.40 +
    df['Project_Score'] * 0.20 +
    df['Participation_Score'] * 0.10
).round(2)
print("Calculated 'Overall_Score' column.")

# Categorize 'Overall_Score' into performance levels
def get_performance_level(score):
    if score >= 90:
        return 'Excellent'
    elif score >= 80:
        return 'Good'
    elif score >= 70:
        return 'Average'
    else:
        return 'Needs Improvement'

df['Performance_Level'] = df['Overall_Score'].apply(get_performance_level)
print("Categorized 'Overall_Score' into 'Performance_Level'.")

# Convert 'Semester' to a categorical type if needed for analysis/BI tool efficiency
df['Semester'] = df['Semester'].astype('category')

# --- 3. Basic Analysis (for initial insights before Power BI) ---
print("\n--- Basic Analysis Insights ---")

# Average scores by Major
avg_score_by_major = df.groupby('Major')['Overall_Score'].mean().reset_index()
print("\nAverage Overall Score by Major:")
print(avg_score_by_major)

# Count of students by Performance Level
performance_count = df['Performance_Level'].value_counts().reset_index()
performance_count.columns = ['Performance_Level', 'Student_Count']
print("\nStudent Count by Performance Level:")
print(performance_count)

# --- 4. Save Prepared Data ---
output_file = 'prepared_student_data.csv'
df.to_csv(output_file, index=False)
print(f"\nPrepared data saved to {output_file}")

print("\n--- Prepared Data Sample ---")
print(df.head())
print(f"\nShape of prepared data: {df.shape}")
