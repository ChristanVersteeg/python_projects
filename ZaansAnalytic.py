import pandas as pd

# Load the CSV file
file_path = 'csv-export-6(2).csv'
df = pd.read_csv(file_path)

# The specific activity to search for
target_activity = "Dwars & Co door Rico Hop en een échte Dwarsligger (op het podium - hoofdact)"

def calculate_activity_totals(df, activity_name):
    # 1. Clean 'Leerlingen' (removes the ':' from ':32' and converts to number)
    df['leerlingen_num'] = df['Leerlingen'].astype(str).str.extract('(\d+)').astype(float).fillna(0)
    
    # 2. Clean 'Aantal kinderen' (converts to number, handles empty cells)
    df['kinderen_num'] = pd.to_numeric(df['Aantal kinderen'], errors='coerce').fillna(0)
    
    # 3. Create a combined multiplier for the row
    df['total_multiplier'] = df['leerlingen_num'] + df['kinderen_num']
    
    # 4. Identify columns for the three rounds
    ronde_cols = [col for col in df.columns if 'Ronde' in col]
    
    # 5. Create a filter for rows where the activity appears in ANY of those rounds
    activity_filter = df[ronde_cols].apply(lambda x: x.str.contains(activity_name, na=False, regex=False)).any(axis=1)
    
    # 6. Apply the math: sum of (True entries * multiplier)
    total_participants = df.loc[activity_filter, 'total_multiplier'].sum()
    total_submissions = activity_filter.sum()
    
    return int(total_participants), total_submissions

# Execute and print results
participants, submissions = calculate_activity_totals(df, target_activity)

print(f"Results for: {target_activity}")
print(f"--------------------------------------------------")
print(f"Total calculated children/students: {participants}")
print(f"Total number of forms submitted:    {submissions}")