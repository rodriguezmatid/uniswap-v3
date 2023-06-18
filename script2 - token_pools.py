import pandas as pd

# Load the CSV file into a DataFrame
csv_filename = 'pools-polygon.csv'
df = pd.read_csv(csv_filename)

# Filter the pools with the specific address in either Token 0 or Token 1
filtered_df_token0 = df[df['Token 0'] == '0xE5417Af564e4bFDA1c483642db72007871397896']
filtered_df_token1 = df[df['Token 1'] == '0xE5417Af564e4bFDA1c483642db72007871397896']

# Display the filtered pools
print(filtered_df_token0)
print(filtered_df_token1)

# Merge the filtered DataFrames
merged_df = pd.concat([filtered_df_token0, filtered_df_token1])

# Display the merged pools
print(merged_df)

# Save the DataFrame to a CSV file
output_filename = 'script2_results.csv'
merged_df.to_csv(output_filename, index=False)

print("The filtered DataFrame has been saved to the CSV file: ", output_filename)