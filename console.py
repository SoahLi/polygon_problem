from driver import Driver
import psutil
my_driver = Driver()
my_driver.solve_puzzle()
# my_driver.node_information_at_highest_index(172)
memory_info = psutil.virtual_memory()

# Convert bytes to a more human-readable format (e.g., MB)
memory_usage = memory_info.used / (1024 ** 2)  # Divide by 1024^2 to get megabytes

print(f"Memory used: {memory_usage:.2f} MB")
# my_driver.node_information_at_highest_index(633)