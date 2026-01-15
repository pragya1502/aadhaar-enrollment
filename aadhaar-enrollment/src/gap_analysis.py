import pandas as pd

# Load SAMPLE safely
enrol = pd.read_csv("data/raw/enrolment.csv", nrows=5000)
demo = pd.read_csv("data/raw/demographic.csv", nrows=5000)

# Standardize columns
enrol.columns = enrol.columns.str.lower().str.replace(" ", "_")
demo.columns = demo.columns.str.lower().str.replace(" ", "_")

# Convert date
enrol["date"] = pd.to_datetime(enrol["date"])
demo["date"] = pd.to_datetime(demo["date"])

# 1️⃣ Aggregate PINCODE → DISTRICT (ENROLMENT)
enrol_dist = enrol.groupby(
    ["state", "district"]
)[["age_0_5", "age_5_17", "age_18_greater"]].sum().reset_index()

# 2️⃣ Aggregate PINCODE → DISTRICT (DEMOGRAPHIC)
demo_dist = demo.groupby(
    ["state", "district"]
)[["demo_age_5_17", "demo_age_17"]].sum().reset_index()

# 3️⃣ Merge both
merged = enrol_dist.merge(
    demo_dist,
    on=["state", "district"],
    how="left"
)

# 4️⃣ GAP calculation
merged["gap_5_17"] = merged["demo_age_5_17"] - merged["age_5_17"]
merged["gap_18_plus"] = merged["demo_age_17"] - merged["age_18_greater"]

# 5️⃣ Identify high gap districts
high_gap = merged.sort_values(
    by=["gap_5_17", "gap_18_plus"],
    ascending=False
)

print(high_gap.head(10))

high_gap.to_csv("data/processed/district_gap_analysis.csv", index=False)

#run this by changing path pragyaa

