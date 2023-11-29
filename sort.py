import numpy as np
import time

# sort.py 是一個 module


def bubble_sort(numbers):
    # 跑 n 輪
    for round in range(len(numbers)):
        for index in range(len(numbers[:-1 * (round + 1)])):
            if numbers[index] > numbers[index + 1]:
                numbers[index], numbers[index + 1] = \
                    numbers[index+1], numbers[index]
    return numbers


def selection_sort(numbers):
    num_len = len(numbers)
    for i in range(num_len):
        min_num_index = i  # 預設我目前的最小值索引值

        # 單個回合
        for j in range(i+1, num_len):
            if numbers[min_num_index] > numbers[j]:
                min_num_index = j  # 替代我找到最小值的索引值(index)

        numbers[i], numbers[min_num_index] = \
            numbers[min_num_index], numbers[i]  # 把最小值跟第i個調換
    return numbers


def merge(sorted_left_nums, sorted_right_nums):
    result = list()
    # 合完的條件是：左邊跟右邊都沒有剩下任何數字時完成
    # ~= 當左和右都還有東西時，繼續執行; 剩下還有的部分就直接接到後面去
    while len(sorted_left_nums) > 0 and \
            len(sorted_right_nums) > 0:
        if sorted_left_nums[0] < sorted_right_nums[0]:
            # 左邊第一位 < 右邊第一位
            result.append(sorted_left_nums[0])
            sorted_left_nums = sorted_left_nums[1:]
        else:
            # 左邊第一位 > 右邊第一位
            result.append(sorted_right_nums[0])
            sorted_right_nums = sorted_right_nums[1:]

    if len(sorted_left_nums) > 0:  # 左邊有剩
        result = result + sorted_left_nums
    else:
        result = result + sorted_right_nums

    return result


def merge_sort(numbers):
    # 例外狀況 & 終止條件
    if len(numbers) < 2:  # 長度不夠切分的時候，就不用排直接回傳
        return numbers

    # Divide
    mid_index = len(numbers)//2
    left_numbers = numbers[:mid_index]  # 0 ~ mid_index-1
    right_numbers = numbers[mid_index:]  # mid_index ~ 最後

    sorted_left_numbers = merge_sort(left_numbers)  # 取得排好的左半
    sorted_right_numbers = merge_sort(right_numbers)  # 取得排好的右半
    sorted_total_numbers = merge(sorted_left_numbers, sorted_right_numbers)

    return sorted_total_numbers


def quick_sort(numbers):
    # 遞迴程式，你會需要處理例外條件
    if len(numbers) < 2:
        return numbers

    pivot = numbers[0]
    left = list()
    right = list()

    for i in range(1, len(numbers)):
        if numbers[i] < pivot:
            left.append(numbers[i])
        else:
            right.append(numbers[i])

    # sort_algorithm(left) + [pivot] + sort_algorithm(right)
    answer = quick_sort(left) + [pivot] + quick_sort(right)
    return answer


def insertion_sort(numbers):
    result = list()
    # 每一輪
    for number in numbers:
        insert_index = -1
        for index in range(len(result)):
            if number > result[index]:
                insert_index = index + 1  # 插隊在最後比我小的result[index]的後面，而且後面平移

        if insert_index > 0:
            result = result[:insert_index] + [number] + result[insert_index:]
        else:
            result = [number] + result

    return result


# 當這個.py檔被直接執行的時候，這個 if 才會通過
# 如果這個.py是被當作module引入的話，底下的程式碼不會執行
if __name__ == '__main__':
    numbers = list(np.random.randint(1, 10000, size=10))
    answer = sorted(numbers)
    print("Random a int list, range from 1~10000, size:10")

    current_time = time.time_ns()
    sort_result = bubble_sort(numbers.copy())
    assert answer == sort_result
    finish_time = time.time_ns()
    print("Bubble Sort Result:", sort_result, finish_time-current_time)

    current_time = time.time_ns()
    sort_result = selection_sort(numbers.copy())
    assert answer == sort_result
    finish_time = time.time_ns()
    print("Selection Sort Result:", sort_result, finish_time-current_time)

    current_time = time.time_ns()
    sort_result = insertion_sort(numbers.copy())
    assert answer == sort_result
    finish_time = time.time_ns()
    print("Insertion Sort Result:", sort_result, finish_time-current_time)

    current_time = time.time_ns()
    sort_result = merge_sort(numbers.copy())
    assert answer == sort_result
    finish_time = time.time_ns()
    print("Merge Sort Result:", sort_result, finish_time-current_time)

    current_time = time.time_ns()
    sort_result = quick_sort(numbers.copy())
    assert answer == sort_result
    finish_time = time.time_ns()
    print("Quick Sort Result x:", sort_result, finish_time-current_time)

    current_time = time.perf_counter_ns()
    sort_result = quick_sort(numbers.copy())
    assert answer == sort_result
    finish_time = time.perf_counter_ns()
    print("Quick Sort Result:", sort_result, finish_time-current_time)
