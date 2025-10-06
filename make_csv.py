import pandas as pd

# Sample data
data = {
    "Sales": [100, 200, 150, 300,400],
    "Profit": [20, 50, 30, 70,90]
}

df = pd.DataFrame(data)
df.to_csv("test.csv", index=False)
print("✅ test.csv file created successfully!")
