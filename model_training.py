# ==========================================
# AI DDoS Detection Model Training Pipeline
# ==========================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# ------------------------------------------
# 1. Load Dataset
# ------------------------------------------

df = pd.read_csv("ddos_dataset.csv")

print("Original dataset:", df.shape)

# ------------------------------------------
# 2. Rename Columns (Correct Mapping)
# Your logs include TIMESTAMP as first column
# ------------------------------------------

df.columns = [
    "timestamp",     # col_0
    "version",       # col_1
    "account_id",    # col_2
    "interface_id",  # col_3
    "srcaddr",       # col_4
    "dstaddr",       # col_5
    "srcport",       # col_6
    "dstport",       # col_7
    "protocol",      # col_8
    "packets",       # col_9
    "bytes",         # col_10
    "start",         # col_11
    "end",           # col_12
    "action",        # col_13
    "log_status"     # col_14
]

# ------------------------------------------
# 3. Clean Invalid Values
# Replace "-" with 0
# ------------------------------------------

df = df.replace("-", 0)

# ------------------------------------------
# 4. Convert Numeric Fields Safely
# ------------------------------------------

numeric_cols = [
    "srcport","dstport",
    "protocol","packets","bytes"
]

for col in numeric_cols:
    df[col] = df[col].astype(int)

# Prevent divide-by-zero
df["packets"] = df["packets"].replace(0, 1)

# ------------------------------------------
# 5. Feature Engineering
# ------------------------------------------

df["byte_per_packet"] = df["bytes"] / df["packets"]

df["is_tcp"]  = (df["protocol"] == 6).astype(int)
df["is_udp"]  = (df["protocol"] == 17).astype(int)
df["is_icmp"] = (df["protocol"] == 1).astype(int)

# ------------------------------------------
# 6. Aggregate Traffic Per Source IP
# ------------------------------------------

agg_df = df.groupby("srcaddr").agg({
    "packets": "sum",
    "bytes": "sum",
    "byte_per_packet": "mean",
    "is_tcp": "sum",
    "is_udp": "sum",
    "is_icmp": "sum"
}).reset_index()

print("Aggregated dataset:", agg_df.shape)

# ------------------------------------------
# 7. Create Labels (Heuristic)
# ------------------------------------------
# Adjust threshold later if needed

agg_df["label"] = agg_df["packets"].apply(
    lambda x: 1 if x > 5000 else 0
)

print("\nLabel distribution:")
print(agg_df["label"].value_counts())

# ------------------------------------------
# 8. Prepare Features & Target
# ------------------------------------------

X = agg_df[
    ["packets","bytes","byte_per_packet",
     "is_tcp","is_udp","is_icmp"]
]

y = agg_df["label"]

# ------------------------------------------
# 9. Train/Test Split
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------------------------
# 10. Train Model
# ------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ------------------------------------------
# 11. Predictions & Evaluation
# ------------------------------------------

preds = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, preds))

print("Confusion Matrix:")
print(confusion_matrix(y_test, preds))

# ------------------------------------------
# 12. Save Model
# ------------------------------------------

joblib.dump(model, "ddos_model.pkl")

print("\nModel saved as ddos_model.pkl")
