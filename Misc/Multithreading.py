import multiprocessing
from Classes.FileHandling import FileHandler, FileOperationRequest


# Function to execute a function across all possible threads on the current computer
def multifunction(func):
    # Create a number of processes to manage this insurmountable task
    processes = []
    print(str(multiprocessing.cpu_count()) + " threads detected.")
    for i in range(0, multiprocessing.cpu_count()):
        t = multiprocessing.Process(target=func)
        processes.append(t)
        t.start()
    for one_process in processes:
        one_process.join()


# Multiprocessing printer function
def multi_printer(msg, lock):
    # print("Asking for a print")
    lock.acquire()
    print(msg)
    lock.release()


# Multiprocessing file handler
def multi_file_operations(request, lock):
    if isinstance(request, FileOperationRequest):
        result = False
        lock.acquire()
        handle = FileHandler(filename=request.filename, check=request.check, remove=request.remove)
        if request.msg is not None:
            handle.add_line(request.msg)
        if request.check:
            result = handle.file_check()
        lock.release()
        return result
