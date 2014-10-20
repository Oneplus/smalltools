import threading, Queue

class WorkerThread(threading.Thread):
    """ """
    def __init__(self, func, tasks_q, results_q):
        super(WorkerThread, self).__init__()
        self.func = func
        self.tasks_q = tasks_q
        self.results_q = results_q
        self.stoprequest = threading.Event()

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stoprequest.isSet():
            try:
                task = self.tasks_q.get(True, 0.05)
                result = self.func(task)
                self.result_q.put(result)
            except Queue.Empty:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)


def MultiThreaded(func, tasks):
    pass

def MultiThreadedSyncWrite(func, tasks, fpo):
    pass
