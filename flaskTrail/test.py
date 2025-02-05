import threading

def print_numbers():
    for i in range(5):
        print(f"Thread {i}")

# Creating threads
threads = []
for _ in range(2):
    t = threading.Thread(target=print_numbers)
    t.start()
    threads.append(t)

# Waiting for threads to finish
for t in threads:
    t.join()
