import pandas as pd
import os

# Create sample data
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan', 'Fay'],
    'age': [30, 25, 35, 28, 40, 22],
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'San Diego'],
    'status': ['active', 'inactive', 'active', 'active', 'inactive', 'active']
}
df = pd.DataFrame(data)

# Get the path to the tests directory
tests_dir = os.path.dirname(__file__)
feather_path = os.path.join(tests_dir, 'sample.feather')

# Save as feather
df.to_feather(feather_path)
print(f'Created {feather_path}')
