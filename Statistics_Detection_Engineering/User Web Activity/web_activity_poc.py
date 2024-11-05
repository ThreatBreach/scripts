import json
import random
import time
from threading import Thread
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker and create user agent and IP pools
fake = Faker()

user_agents = [fake.user_agent() for _ in range(10)]
ips = [fake.ipv4() for _ in range(10)]

common_directories = [
    "admin", "administrator", "login", "admin1", "admin2",
    "wp-admin", "dashboard", "manage", "config", "uploads",
    "includes", "files", "cgi-bin", "backup", "private",
    "webadmin", "secure", "system", "auth", "core"
]

def generate_complex_url():
    scheme = "https"  # e.g., http or https
    subdomain = fake.word()
    domain = fake.domain_name()
    # Randomly select 2 directories from the list
    selected_dirs = random.sample(common_directories, 2)

    # Build the path using the selected directories
    path = f"/{selected_dirs[0]}/{selected_dirs[1]}/"  # Join two words for the path
    url = f"{scheme}://{subdomain}.{domain}{path}"
    return url

# Function to generate log entries with bytes in and out, and an incremented timestamp
def generate_log(user_id, url, ip, user_agent, response_code, timestamp, non_existent_url=None):
    bytes_in = random.randint(100, 10000)  # Random bytes received
    bytes_out = random.randint(100, 10000)  # Random bytes sent
    log = {
        "user_id": user_id,
        "url": url,
        "ip": ip,
        "user_agent": user_agent,
        "response_code": response_code,
        "bytes_in": bytes_in,
        "bytes_out": bytes_out,
        "non_existent_url": non_existent_url,
        "timestamp": timestamp.strftime('%Y-%m-%dT%H:%M:%S')
    }
    return json.dumps(log)

# Function to simulate user activity
def simulate_user_activity(user_id, log_file, duration_minutes=60):
    ip = random.choice(ips)
    user_agent = random.choice(user_agents)
    end_time = time.time() + duration_minutes * 60

    # Initialize start date and increment time by controlled intervals
    current_time = datetime.now()

    while time.time() < end_time:
        if random.random() < 0.1:  # 10% chance to switch to anomalous behavior
            print(f"User {user_id} switching to anomalous behavior")
            simulate_anomalous_behavior(user_id, log_file, current_time)
        else:
            url = generate_complex_url()
            try:
                response_code = random.choice([200, 404, 500])  # Simulate possible response codes
                log_entry = generate_log(user_id, url, ip, user_agent, response_code, current_time)
                with open(log_file, 'a') as file:
                    file.write(log_entry + "\n")
            except Exception as e:
                print(f"User {user_id} encountered an error: {e}")

            # Increment the current time by seconds or minutes, and rarely by a day
            if random.random() < 0.8:  # 80% chance to increment by seconds or minutes
                current_time += timedelta(seconds=random.randint(10, 300))  # Increment by 10 to 300 seconds
            else:
                current_time += timedelta(days=1)  # Occasional increment by 1 day
        
        time.sleep(random.uniform(1, 5))

# Function to simulate anomalous behavior with date increment
def simulate_anomalous_behavior(user_id, log_file, start_time):
    ip = random.choice(ips)
    user_agent = random.choice(user_agents)
    
    current_time = start_time
    
    # Simulate high frequency of requests
    for _ in range(50):
        try:
            url = generate_complex_url()
            response_code = 200  # Assume all requests are successful
            log_entry = generate_log(user_id, url, ip, user_agent, response_code, current_time)
            with open(log_file, 'a') as file:
                file.write(log_entry + "\n")
        except Exception as e:
            print(f"Anomalous User {user_id} encountered an error: {e}")
        
        # Increment timestamp by a smaller random amount
        current_time += timedelta(seconds=random.randint(1, 5))
        time.sleep(random.uniform(0.1, 1))

    # Introduce some additional anomalies like accessing non-existent pages
    non_existent_url = generate_complex_url()
    try:
        response_code = 404
        log_entry = generate_log(user_id, non_existent_url, ip, user_agent, response_code, current_time, non_existent_url=non_existent_url)
        with open(log_file, 'a') as file:
            file.write(log_entry + "\n")
    except Exception as e:
        print(f"Anomalous User {user_id} encountered an error: {e}")

# Function to start the simulation
def start_simulation():
    num_users = 10
    log_file = 'web_activity_logs.json'

    threads = []
    for user_id in range(1, num_users + 1):
        print(f"Starting activity for User {user_id+round(random.random()*100)}")
        thread = Thread(target=simulate_user_activity, args=(user_id, log_file))
        threads.append(thread)
        thread.start()

    # Run for a specific period or until a condition is met
    time.sleep(3600)  # Example: Run simulation for 1 hour
    # Signal threads to stop

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("Starting simulation...")
    start_simulation()
    print("Simulation complete. Press Ctrl+C to stop.")
