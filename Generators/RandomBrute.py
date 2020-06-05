import os.path
import random
import time
from datetime import datetime
from Classes.DBObjects.PrivateKey import PrivateKey
from multiprocessing import Process, Value, cpu_count, Lock
from Misc.Multithreading import multi_printer,  multi_file_operations
from Generators.DBChecker import db_check
from Classes.FileHandling import FileHandler, FileOperationRequest


# Function to create a fully random 256-bit binary sequence
def create_random_binary(length=256):
    # Initialize variables and seed random function.
    binary = 0b0
    random.seed()
    for i in range(0, length):
        bit = random.getrandbits(1)
        binary += bit*2**i
    return binary


# Function to create a random X-Digit Hex string.
def create_random_hex(length=64):
    hexdigits = "0123456789ABCDEF"
    random_digits = "".join([hexdigits[random.randint(0, 0xF)] for _ in range(length)])
    return random_digits


# Function that generates a random keypair and corresponding addresses
def random_keypair():
    pk = PrivateKey(private_key=create_random_hex(length=64))
    pk.generate_public_key()
    pk.public_key.generate_addresses()
    return pk


# Function to generate random bitcoin keypairs and analyze them, 5 at a time, in the database
def random_keypair_loop(kill_switch, benchmark, lock):
    keys = 0
    num_keys = 30
    winners = 0
    while kill_switch.value == 0:
        pk_list = []
        for i in range(0, num_keys):
            pk = random_keypair()
            keys += 1
            pk_list.append(pk)
        winners = winners + 1 if db_check(pk=pk_list, lock=lock) else winners
        time.sleep(0.02)
    # benchmark testing
    benchmark.value = benchmark.value + keys


# Function to execute a function across all possible cpu cores on the current computer
# DESKTOP SHOWS 500,000 keys checked per hour on 'ALL CORES', 0.02 SLEEP.
# LAPTOP SHOWS 3,000,000 keys checked per hour on ALL CORES, 0.02 SLEEP.
# SERVER SHOWS 5,500,000 keys checked per hour on ALL CORES, 0.02 SLEEP.
def multiprocess_brute():
    kill_switch = Value('i', 0)
    benchmark = Value('i', 0)
    lock = Lock()
    processes = []
    num_processes = cpu_count()//2
    # Begin benchmark timing
    start = datetime.now()
    # Log the living
    multi_file_operations(request=FileOperationRequest(filename="living"), lock=lock)
    for i in range(0, num_processes):
        t = Process(target=random_keypair_loop, args=(kill_switch, benchmark, lock))
        processes.append(t)
        t.start()
    # Stay alive until the kill signal
    while not multi_file_operations(request=FileOperationRequest(filename="die", check=True), lock=lock):
        time.sleep(5)
        # time.sleep(55)
        # multi_file_operations(request=FileOperationRequest(filename="die"), lock=lock)
    # If code is here, it is time to die
    kill_switch.value = 1
    multi_file_operations(request=FileOperationRequest(filename="living", remove=True), lock=lock)
    multi_file_operations(request=FileOperationRequest(filename="die", remove=True), lock=lock)
    # Join processes in reverse so that the IO queue is done last
    for process in processes:
        process.join()
    delta = datetime.now() - start
    # Compose death message
    message = "=====" + start.strftime("%Y-%m-%d %X") + "=====" + "\n" + \
              "Execution time: " + str(delta.total_seconds()) + " seconds.\n" + \
              str(benchmark.value) + " keys checked.\n" + \
              str((benchmark.value//delta.total_seconds())*3600) + " keys checked per hour.\n"
    multi_file_operations(request=FileOperationRequest(filename="benchmark.txt", msg=message), lock=lock)
