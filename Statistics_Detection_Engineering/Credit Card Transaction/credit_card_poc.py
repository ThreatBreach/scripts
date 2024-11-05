import json
import random
from datetime import datetime, timedelta

# Function to generate a random transaction for a specific user
def generate_transaction(transaction_id, user_id, outlier=False):
    # Normal transaction values
    amount = random.uniform(5.0, 300.0)
    transaction_location = random.choice(["New York", "Los Angeles", "Chicago", "San Francisco", "Miami"])
    transaction_time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 24), minutes=random.randint(0, 59))

    # Introduce outliers
    if outlier:
        amount = random.uniform(1000.0, 10000.0)  # Unusually high amount
        transaction_location = random.choice(["Foreign City A", "Foreign City B", "Foreign City C"])  # Uncommon location
        transaction_time = datetime.now() - timedelta(days=random.randint(31, 90), hours=random.randint(0, 24), minutes=random.randint(0, 59))  # Unusual time

    transaction = {
        "transaction_id": f"TX{transaction_id:06d}",
        "user_id": f"USER{user_id:04d}",
        "amount": round(amount, 2),
        "transaction_location": transaction_location,
        "transaction_time": transaction_time.strftime("%Y-%m-%d %H:%M:%S"),
        "outlier": outlier
    }
    return transaction

# Generate transactions for multiple users with multiple transactions per day
def generate_user_transactions(user_id, transaction_start_id, num_transactions_per_user, outlier_ratio):
    transactions = []
    outlier_count = int(num_transactions_per_user * outlier_ratio)
    normal_count = num_transactions_per_user - outlier_count

    # Generate normal transactions for a user
    for i in range(normal_count):
        transaction = generate_transaction(transaction_start_id + i, user_id, outlier=False)
        transactions.append(transaction)

    # Generate outlier transactions for a user
    for i in range(outlier_count):
        transaction = generate_transaction(transaction_start_id + normal_count + i, user_id, outlier=True)
        transactions.append(transaction)

    # Sort transactions to simulate chronological order within the dataset
    transactions.sort(key=lambda x: x["transaction_time"])
    return transactions

# Generate dataset
def generate_dataset(num_users=50, num_transactions_per_user=20, outlier_ratio=0.05):
    dataset = []
    transaction_id = 0

    for user_id in range(1, num_users + 1):
        user_transactions = generate_user_transactions(user_id, transaction_id, num_transactions_per_user, outlier_ratio)
        dataset.extend(user_transactions)
        transaction_id += num_transactions_per_user

    # Shuffle dataset to mix users' transactions
    random.shuffle(dataset)
    return dataset

# Generate the data and save it to a JSON file
def save_to_json(filename="credit_card_transactions_logs.json", num_users=50, num_transactions_per_user=20, outlier_ratio=0.05):
    data = generate_dataset(num_users, num_transactions_per_user, outlier_ratio)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

# Run the function to generate and save the JSON data
save_to_json(num_users=50, num_transactions_per_user=20, outlier_ratio=0.05)
