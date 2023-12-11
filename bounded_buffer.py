from collections import UserList
import threading
import logging
import time

class BoundedBuffer(UserList):
    size = 0
    write_sem = None
    read_sem = None

    def __init__(self, size: int, *args, **kwargs):
        self.size = size
        self.write_sem = threading.Semaphore(size)
        self.read_sem = threading.Semaphore(0)
        super(BoundedBuffer, self).__init__(*args, **kwargs)

    def push(self, item: None) -> None:
        self.write_sem.acquire()
        # logging.info(f"Acquired write semaphore; value = {self.write_sem._value}")
        rtn = super().append(item)
        if len(self.data) > self.size:
            raise RuntimeError("Buffer Overflow")
        self.read_sem.release()
        # logging.info(f"Released read semaphore; value = {self.read_sem._value}")
        return rtn
    
    def pop(self) -> None:
        self.read_sem.acquire()
        # logging.info(f"Acquired read semaphore; value = {self.read_sem._value}")
        rtn = super().pop(0)
        self.write_sem.release()
        # logging.info(f"Released write semaphore; value = {self.write_sem._value}")
        return rtn
    
class ProducerThread(threading.Thread):
    bb = None
    stop_thread = False
    push_val = 0

    def __init__(self, bb: BoundedBuffer, push_val: int = 0, *args, **kwargs):
        self.bb = bb
        self.push_val = push_val
        super(ProducerThread, self).__init__(target=self.func, *args, **kwargs)

    def func(self):
        while not self.stop_thread:
            time.sleep(1)
            bb.push(self.push_val)
            logging.info(f"{self.name} pushing: {self.push_val}")
        logging.info(f"{self.name} finished")

    # def stop(self):
    #     self.stop_thread = True

    def join(self):
        self.stop_thread = True
        rtn = super().join()
        return rtn

class ConsumerThread(threading.Thread):
    bb = None
    stop_thread = False

    def __init__(self, bb: BoundedBuffer, *args, **kwargs):
        self.bb = bb
        super(ConsumerThread, self).__init__(target=self.func, *args, **kwargs)

    def func(self):
        while not self.stop_thread:
            time.sleep(1)
            val = bb.pop()
            logging.info(f"{self.name} popping: {val}")
        logging.info(f"{self.name} finished")

    # def stop(self):
    #     self.stop_thread = True

    def join(self, *args):
        self.stop_thread = True
        rtn = super().join()
        return rtn
        
    
# def producer_func(val, bb: BoundedBuffer, thread_name: str = ""):
#     while True:
#         time.sleep(1)
#         bb.push(val)
#         logging.info(f"{thread_name} Pushing: {val}")

# def consumer_func(bb: BoundedBuffer, thread_name: str = ""):
#     while True:
#         time.sleep(1)
#         rtn = bb.pop()
#         logging.info(f"{thread_name} Popping: {rtn}")
    
if __name__ == "__main__":
    num_pro = 3
    num_con = 1
    bb_size = 10
    thread_list = []

    bb = BoundedBuffer(bb_size)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    for i in range(num_pro):
        t_name = f"pro_thread{i+1}"
        t = ProducerThread(name=t_name, push_val=i+1, bb=bb)
        thread_list.append(t)
        t.start()

    for i in range(num_con):
        t_name = f"con_thread{i+1}"
        t = ConsumerThread(name=t_name, bb=bb)
        thread_list.append(t)
        t.start()

    time.sleep(3)

    for index, thread in enumerate(thread_list):
        logging.info(f"Stopping thread {thread.name}")
        thread.join()
