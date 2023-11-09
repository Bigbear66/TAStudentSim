import threading
import time
import random

SLEEP = 0
WAKEUP = 1

MAX_STUDENTS = 10
END_OF_PROGRAM = False
semaphore = SLEEP
waiting_list = []

mutex = threading.Lock()
ta_sleep_cond = threading.Condition(mutex)


def sleeping_ta():
    global semaphore, waiting_list
    while not END_OF_PROGRAM:
        with mutex:
            print("[TA] TA is in the office.")
            while semaphore == SLEEP:
                print("[TA] TA is sleeping.")
                ta_sleep_cond.wait()
            print("[TA] TA is awake.")
            if waiting_list:
                student_id = waiting_list.pop(0)
                print(f"[TA] TA is helping student {student_id}.")
            else:
                print("[TA] No students in the waiting list.")
            semaphore = SLEEP


def student(student_id):
    global semaphore, waiting_list
    with mutex:
        print(f"[Student {student_id}] Student is coming!")
        if semaphore == SLEEP:
            print("[Student] Waking up TA.")
            semaphore = WAKEUP
            ta_sleep_cond.notify()
        else:
            print("[Student] Waiting for TA's help.")
            waiting_list.append(student_id)
    # Simulating time taken by TA to assist
    time.sleep(random.randint(1, 5))


if __name__ == "__main__":
    ta_thread = threading.Thread(target=sleeping_ta)
    student_threads = []

    ta_thread.start()
    for student_id in range(1, MAX_STUDENTS + 1):
        student_thread = threading.Thread(target=student, args=(student_id,))
        student_threads.append(student_thread)
        student_thread.start()

    for student_thread in student_threads:
        student_thread.join()

    END_OF_PROGRAM = True
    with mutex:
        # Wake up TA in case it's sleeping
        ta_sleep_cond.notify()
    ta_thread.join()
