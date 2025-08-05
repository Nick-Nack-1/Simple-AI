import time

# Start time
start_time = time.time()

# Print statement
for i in range(1000):
	print("Hello, World!")

# End time
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Print statement took {elapsed_time/1000} seconds")