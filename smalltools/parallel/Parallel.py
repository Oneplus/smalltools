#!/usr/bin/env python
from mpi4py import MPI
import logging

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
status = MPI.Status()
name = MPI.Get_processor_name()

FORMAT = "[%(levelname)5s] %(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT,
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(name)


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START')


def Parallel(func, tasks):
    '''
    A MPI wrapper for paralleling apply jobs to the function

    Parameters
    ----------
    func : Function object
        The function to apply job to
    tasks : list
        The list of jobs
    '''
    if rank == 0:
        # The master process
        task_index = 0
        num_workers = size - 1
        closed_workers = 0
        logger.info("Master starting with %d workers" % num_workers)
        while closed_workers < num_workers:
            data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            source = status.Get_source()
            tag = status.Get_tag()
            if tag == tags.READY:
                # Worker is ready, so send it a task
                if task_index < len(tasks):
                    comm.send(tasks[task_index], dest=source, tag=tags.START)
                    task_index += 1
                else:
                    comm.send(None, dest=source, tag=tags.EXIT)
            elif tag == tags.DONE:
                pass
            elif tag == tags.EXIT:
                logger.info("Worker %d exited." % source)
                closed_workers += 1
        logger.info("Master finishing")
    else:
        # The slave process
        #print("I am a worker with rank %d on %s." % (rank, name))
        while True:
            comm.send(None, dest=0, tag=tags.READY)
            task = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()

            if tag == tags.START:
                try:
                    # Execute the function on the task
                    func(task)
                    logger.info("SUCCESS: task is done")
                    comm.send(None, dest=0, tag=tags.DONE)
                except Exception, e:
                    success = False
                    print >> sys.stderr, e
                    comm.send(None, dest=0, tag=tags.DONE)
            elif tag == tags.EXIT:
                break
        comm.send(None, dest=0, tag=tags.EXIT)


def ParallelAndSyncWrite(func, tasks, fpo):
    '''
    A MPI wrapper for paralleling apply jobs to the function, collect the
    return value and write the result into file handle. This method is
    designed for a certain kind of tasks. In which the order is out of
    consideration.

    Parameters
    ----------
    func : Function object
        The function to apply job to
    tasks : list
        The list of jobs
    fpo : file object
        The output file handle
    '''
    if rank == 0:
        # The master process
        task_index = 0
        num_workers = size - 1
        closed_workers = 0
        logger.info("Master starting with %d workers" % num_workers)
        while closed_workers < num_workers:
            data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            source = status.Get_source()
            tag = status.Get_tag()
            if tag == tags.READY:
                # Worker is ready, so send it a task
                if task_index < len(tasks):
                    comm.send(tasks[task_index], dest=source, tag=tags.START)
                    task_index += 1
                else:
                    comm.send(None, dest=source, tag=tags.EXIT)
            elif tag == tags.DONE:
                print >> fpo, str(data)
            elif tag == tags.EXIT:
                logger.info("Worker %d exited." % source)
                closed_workers += 1
        logger.info("Master finishing")
    else:
        # The slave process
        #print("I am a worker with rank %d on %s." % (rank, name))
        while True:
            comm.send(None, dest=0, tag=tags.READY)
            task = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()

            if tag == tags.START:
                try:
                    # Execute the function on the task
                    result = func(task)
                    logger.info("SUCCESS: is done")
                    comm.send(result, dest=0, tag=tags.DONE)
                except Exception, e:
                    success = False
                    print >> sys.stderr, e
                    comm.send(None, dest=0, tag=tags.DONE)
            elif tag == tags.EXIT:
                break
        comm.send(None, dest=0, tag=tags.EXIT)
