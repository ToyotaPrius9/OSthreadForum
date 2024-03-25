# Harman [2602184220]


# Imports
import threading
import random

# Defines
LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000
buffer = []
lock = threading.Lock()
exit_event = threading.Event()

# Producer Function
def producer():
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            buffer.append(num)
            with open("all.txt", "a") as f:
                f.write(str(num) + '\n')
        if len(buffer) >= BUFFER_SIZE:
            exit_event.set()

# Customer Function
def customer(outfile, condition, parity):
    while not exit_event.is_set():
        with condition:
            while buffer and buffer[-1] % 2 != parity: 
                condition.wait()
            if buffer:
                num = buffer.pop()
                with open(outfile, "a") as f:
                    f.write(str(num) + '\n')
                condition.notify()

#Declare Conditions
odd_condition = threading.Condition(lock)
even_condition = threading.Condition(lock)

#Declare threads
producer_thread = threading.Thread(target=producer)
customer_odd_thread = threading.Thread(target=customer, args=("odd.txt", odd_condition, 0))
customer_even_thread = threading.Thread(target=customer, args=("even.txt", even_condition, 1))


#Start threads
producer_thread.start()
customer_odd_thread.start()
customer_even_thread.start()

#Join threads
producer_thread.join()
customer_odd_thread.join()
customer_even_thread.join()

#Exit
exit_event.clear()

#Print statement for check
print("end")
