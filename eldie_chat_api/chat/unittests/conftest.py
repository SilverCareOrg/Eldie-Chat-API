import pytest
import time

def pytest_configure(config):
    config.start_time_configure = time.time()
    print("Test session configuration started at:", time.ctime(config.start_time_configure))

def pytest_unconfigure(config):
    end_time_configure = time.time()
    config.end_time_configure = end_time_configure  # Store end time for configuration
    elapsed_time_configure = end_time_configure - config.start_time_configure
    print("Test session configuration ended at:", time.ctime(end_time_configure))
    print("Elapsed time for configuration:", elapsed_time_configure, "seconds")

def pytest_sessionstart(session):
    session.start_time_execution = time.time()
    print("Test session execution started at:", time.ctime(session.start_time_execution))

def pytest_sessionfinish(session, exitstatus):
    end_time_execution = time.time()
    elapsed_time_execution = end_time_execution - session.start_time_execution
    print("Test session execution ended at:", time.ctime(end_time_execution))
    print("Elapsed time for execution:", elapsed_time_execution, "seconds")

    if hasattr(session.config, 'end_time_configure'):
        time_between_unconfigure_and_finish = end_time_execution - session.config.end_time_configure
        print("Time between unconfigure and session finish:", time_between_unconfigure_and_finish, "seconds")
