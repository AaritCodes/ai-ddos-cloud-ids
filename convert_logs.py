import pandas as pd

file_path = "000000"   # extracted file

rows = []

with open(file_path, "r") as f:
    for line in f:
        if line.startswith("version"):
            continue
        rows.append(line.strip().split())

# 🔧 FIX — dynamic schema detection
num_cols = len(rows[0])
print("Detected columns:", num_cols)

columns = [f"col_{i}" for i in range(num_cols)]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("ddos_dataset.csv", index=False)

print("Dataset shape:", df.shape)
