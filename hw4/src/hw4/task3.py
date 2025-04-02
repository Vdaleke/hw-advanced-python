import multiprocessing
import time
import codecs
from datetime import datetime
from multiprocessing.synchronize import Event
from multiprocessing import Queue


def process_a(queue_a_to_b, queue_main_to_a, stop_event):
    while not stop_event.is_set():
        try:
            msg = queue_main_to_a.get(timeout=1)
            processed_msg = msg.lower()
            queue_a_to_b.put(processed_msg)
            time.sleep(5)
        except:
            continue


def process_b(queue_a_to_b, queue_b_to_main, stop_event):
    while not stop_event.is_set():
        try:
            msg = queue_a_to_b.get(timeout=1)
            rot13_msg = codecs.encode(msg, "rot13")
            print(
                f"[{datetime.now().strftime("%H:%M:%S.%f")}] Process B: {rot13_msg}",
                flush=True,
            )
            queue_b_to_main.put(rot13_msg)
        except:
            continue


def main_process():
    queue_main_to_a = Queue()
    queue_a_to_b = Queue()
    queue_b_to_main = Queue()
    stop_event = multiprocessing.Event()

    p_a = multiprocessing.Process(
        target=process_a, args=(queue_a_to_b, queue_main_to_a, stop_event)
    )
    p_b = multiprocessing.Process(
        target=process_b, args=(queue_a_to_b, queue_b_to_main, stop_event)
    )

    p_a.start()
    p_b.start()

    try:
        while True:
            timestamp = datetime.now().time().strftime("%H:%M:%S.%f")
            print(
                f"[{timestamp}] Введите сообщение (или 'exit' для выхода): ",
                flush=True,
            )
            user_input = input()
            if user_input.lower() == "exit":
                break

            timestamp = datetime.now().time().strftime("%H:%M:%S.%f")
            print(
                f"[{timestamp}] Main -> A: {user_input}",
                flush=True,
            )
            queue_main_to_a.put(user_input)

            msg = queue_b_to_main.get()
            timestamp = datetime.now().time().strftime("%H:%M:%S.%f")
            print(
                f"[{timestamp}] Main received from B: {msg}",
                flush=True,
            )

    finally:
        stop_event.set()
        p_a.join()
        p_b.join()


if __name__ == "__main__":
    main_process()
