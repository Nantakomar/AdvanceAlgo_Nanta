import threading
import time


NUMBERS = [50, 100, 200]
ROUNDS = 10


def factorial(n):
    """
    Calculates the factorial of a given number using an iterative approach.
    Example: 5! = 5 x 4 x 3 x 2 x 1 = 120
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1

    for i in range(2, n + 1):
        result *= i

    return result


def factorial_worker(number, results, thread_times):
    """
    Worker function for each thread.
    Each thread calculates one factorial number and records its own start and end time.
    """
    start_time = time.perf_counter_ns()

    results[number] = factorial(number)

    end_time = time.perf_counter_ns()

    thread_times[number] = {
        "start": start_time,
        "end": end_time
    }


def run_multithreaded_round():
    """
    Runs one round of the multithreaded factorial experiment.
    Three separate threads are created:
    - one thread for 50!
    - one thread for 100!
    - one thread for 200!

    Total time is calculated using:
    End time of the thread that finished last - Start time of the thread that started first
    """
    results = {}
    thread_times = {}
    threads = []

    for number in NUMBERS:
        thread = threading.Thread(
            target=factorial_worker,
            args=(number, results, thread_times),
            name=f"Thread-{number}"
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    first_start_time = min(thread_data["start"] for thread_data in thread_times.values())
    last_end_time = max(thread_data["end"] for thread_data in thread_times.values())

    total_time = last_end_time - first_start_time

    return total_time, results


def run_non_threaded_round():
    """
    Runs one round of the non-threaded factorial experiment.
    The factorials are calculated one by one in sequence.
    """
    results = {}

    start_time = time.perf_counter_ns()

    for number in NUMBERS:
        results[number] = factorial(number)

    end_time = time.perf_counter_ns()

    total_time = end_time - start_time

    return total_time, results


def display_factorial_summary(results):
    """
    Displays a short summary to prove that factorial values were generated.
    Full factorial values are not printed because 200! is very long.
    """
    print("\nGenerated Factorial Result Summary:")
    for number in NUMBERS:
        factorial_value = results[number]
        digit_count = len(str(factorial_value))
        print(f"{number}! calculated successfully | Number of digits: {digit_count}")


def run_multithreaded_experiment():
    print("\n================ Multithreaded Factorial Experiment ================")
    print("Calculating 50!, 100!, and 200! using 3 separate threads")
    print("Time is measured in nanoseconds (ns)")
    print("--------------------------------------------------------------------")
    print("Round | Total Time Taken (ns)")
    print("--------------------------------------------------------------------")

    times = []
    sample_results = None

    for round_no in range(1, ROUNDS + 1):
        total_time, results = run_multithreaded_round()
        times.append(total_time)

        if round_no == 1:
            sample_results = results

        print(f"{round_no:<5} | {total_time}")

    average_time = sum(times) / len(times)

    print("--------------------------------------------------------------------")
    print(f"Average Time Taken: {average_time:.2f} ns")
    print("====================================================================")

    display_factorial_summary(sample_results)

    return times, average_time


def run_non_threaded_experiment():
    print("\n================ Non-Threaded Factorial Experiment =================")
    print("Calculating 50!, 100!, and 200! sequentially without multithreading")
    print("Time is measured in nanoseconds (ns)")
    print("--------------------------------------------------------------------")
    print("Round | Total Time Taken (ns)")
    print("--------------------------------------------------------------------")

    times = []
    sample_results = None

    for round_no in range(1, ROUNDS + 1):
        total_time, results = run_non_threaded_round()
        times.append(total_time)

        if round_no == 1:
            sample_results = results

        print(f"{round_no:<5} | {total_time}")

    average_time = sum(times) / len(times)

    print("--------------------------------------------------------------------")
    print(f"Average Time Taken: {average_time:.2f} ns")
    print("====================================================================")

    display_factorial_summary(sample_results)

    return times, average_time


def compare_experiments(threaded_average, non_threaded_average):
    print("\n================ Experiment Comparison ================")
    print(f"Average Multithreaded Time: {threaded_average:.2f} ns")
    print(f"Average Non-Threaded Time : {non_threaded_average:.2f} ns")

    difference = abs(threaded_average - non_threaded_average)

    if threaded_average < non_threaded_average:
        print(f"Multithreading was faster by {difference:.2f} ns in this experiment.")
    elif threaded_average > non_threaded_average:
        print(f"Non-threaded execution was faster by {difference:.2f} ns in this experiment.")
    else:
        print("Both methods took the same average time.")

    print("=======================================================")


def main():
    print("Question 3: Concurrent Process")
    print("Factorial calculation for 50!, 100!, and 200!")

    threaded_times, threaded_average = run_multithreaded_experiment()
    non_threaded_times, non_threaded_average = run_non_threaded_experiment()

    compare_experiments(threaded_average, non_threaded_average)


if __name__ == "__main__":
    main()