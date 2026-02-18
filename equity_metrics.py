import pandas as pd 

'''
Filtering columns to identify relevant data.

INSTNM (Institution Name)
CIPDESC (Field of Study)
CREDDESC (Degree Level)

Primary Metrics:
EARN_MDN_5YR
EARN_PELL_WNE_MDN_5YR
EARN_NOPELL_WNE_MDN_5YR
EARN_MALE_WNE_MDN_5YR
EARN_NOMALE_WNE_MDN_5YR


'''
#filter to only load relevant columns to avoid memory issues
cols_to_use = [
    "INSTNM",
    "CIPDESC",
    "CREDDESC",
    "EARN_MDN_5YR",
    "EARN_PELL_WNE_MDN_5YR",
    "EARN_NOPELL_WNE_MDN_5YR",
    "EARN_MALE_WNE_MDN_5YR",
    "EARN_NOMALE_WNE_MDN_5YR"
]
df = pd.read_csv("/Users/ryleeeliou/Desktop/Most-Recent-Cohorts-Field-of-Study.csv", usecols=cols_to_use,low_memory=False)

#filter to include bachelor degrees only

df = df[df['CREDDESC'] == "Bachelor's Degree"]

#Convert earings metrics to numeric values 

cols = [
    'EARN_MDN_5YR',
    'EARN_PELL_WNE_MDN_5YR',
    'EARN_NOPELL_WNE_MDN_5YR',
    'EARN_MALE_WNE_MDN_5YR',
    'EARN_NOMALE_WNE_MDN_5YR'
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce') # blanks to NaN

# Drop rows with NaN values in any of the earnings columns
df = df.dropna(subset=cols)

#Equity metrics
df["pell_gap"] = df["EARN_NOPELL_WNE_MDN_5YR"] - df["EARN_PELL_WNE_MDN_5YR"]
df["gender_gap"] = df["EARN_MALE_WNE_MDN_5YR"] - df["EARN_NOMALE_WNE_MDN_5YR"]

print(df["CREDDESC"].unique())
print(df[["pell_gap", "gender_gap"]].describe()) #prints basic summary statistics
print(df.shape)

#Show what majors face the largest disparities through agreggated analysis 

major_avg = df.groupby("CIPDESC")[[
    "pell_gap",
    "gender_gap"
]].mean().reset_index()

print(major_avg.sort_values("pell_gap", ascending=False).head(10)) #top 10 majors with largest pell gap
print(major_avg.sort_values("gender_gap", ascending=False).head(10)) #top 10 majors with largest gender gap

#Filter out majors with small samples
major_counts = df.groupby("CIPDESC").size().reset_index(name="count")

major_avg = df.groupby("CIPDESC")[[
    "pell_gap",
    "gender_gap"
]].mean().reset_index()

major_avg = major_avg.merge(major_counts, on="CIPDESC")

major_avg = major_avg[major_avg["count"] > 10]
#saves cleaned data to export to tableau 
major_avg.to_csv("/Users/ryleeeliou/Desktop/cleaned_equity_major_analysis.csv", index=False)

