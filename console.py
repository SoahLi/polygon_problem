from driver import Driver
import os, psutil
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

my_driver = Driver()
my_driver.solve_puzzle()
# my_driver.node_information_at_highest_index()

print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
