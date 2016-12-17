from __future__ import print_function
import functools
import time

trace_logger = lambda x: print("[TRACE] %s" % x)
debug_logger = lambda x: print("[DEBUG] %s" % x)
info_logger = lambda x: print("[INFO] %s" % x)
warn_logger = lambda x: print("[WARN] %s" % x)
err_logger = lambda x: print("[ERROR] %s" % x)


class TimeOutError(RuntimeError):
    pass


def retry(max_retry=10, interval=5, catch_exception=Exception):
    def wrapper(func):
        @functools.wraps(func)
        def innerwrapper(*args, **kwargs):
            retry_time = 0
            while retry_time <= max_retry:
                try:
                    return func(*args, **kwargs)
                except catch_exception as e:
                    retry_time += 1
                    warn_logger("try '%s' raise an exception: '%s' " % (func.__name__, repr(e)))
                    time.sleep(interval)
                    warn_logger("retry '%s'  #%s" % (func.__name__, str(retry_time)))
            err_logger("Retry reached max retry time for '%s'. Last failed due to '%s'" % (func.__name__, repr(e)))
            raise e

        return innerwrapper

    return wrapper


def wait(break_condition=lambda: False, timeout=2700, check_interval=1):
    def wrapper(wait_true):
        wait_name = wait_true.__name__

        @functools.wraps(wait_true)
        def innerwrapper(*args, **kwargs):
            start_time = time.time()
            while not break_condition():
                if wait_true(*args, **kwargs):
                    info_logger("'%s' is True and stop waiting" % wait_name)
                    return 0
                else:
                    time.sleep(check_interval)
                    elapsed_time = time.time() - start_time
                    info_logger("wait elapsed time is %s" % str(elapsed_time))
                    if elapsed_time > timeout:
                        raise TimeOutError("Waiting function '%s' time out " % wait_name)
            raise RuntimeError(
                "Break condition '%s' triggered during waiting '%s' " % (break_condition.func_name, wait_name))

        return innerwrapper

    return wrapper


def time_stamp():
    pass


if __name__ == "__main__":
    pass
