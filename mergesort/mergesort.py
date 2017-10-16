import random
from collections import deque
def merge(left_list,right_list):
    merged,left,right=deque(),deque(left_list),deque(right_list)
    while left and right:
        merged.append(left.popleft() if left[0]<=right[0] else right.popleft())
    if left:
        merged.extend(left)
    elif right:
        merged.extend(right)
    return list(merged)

def mergeSort(unsorted_list):
    list_length=len(unsorted_list)
    if list_length<=1:
        return unsorted_list
    mid_position=int(list_length//2)
    left=mergeSort(unsorted_list[:mid_position])
    right=mergeSort(unsorted_list[mid_position:])
    return merge(left,right)

if __name__=='__main__':
    unsorted_list=random.sample(range(1000),100)
    print(unsorted_list)
    print(mergeSort(unsorted_list))
