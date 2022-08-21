from threading import Thread
from typing import List, Callable, Any

threads: List[Thread] = []

def make_thread(join: bool=True) -> Callable:
    def __decorator__(func: Callable) -> Callable:
        def __wrapper__(*args, **kwargs) -> None:
            daemon: Callable = lambda: True if not join else False
            thread: Thread = Thread(
                target=func,
                args=args,
                kwargs=kwargs,
                daemon=daemon()
            )
            thread.start()
            if join:
                threads.append(thread)
                thread.join()
            else: threads.append(thread)
        return __wrapper__
    return __decorator__