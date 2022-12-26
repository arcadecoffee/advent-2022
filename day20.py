"""
Advent of Code 2022 Day 20
"""
import sys

from advent_tools import get_daily_input

DAY = 20

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
1
2
-3
3
-2
0
4
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


class Element:
    def __init__(self, value: int):
        self.value = value
        self.next = None
        self.prev = None


def find_answer(all_elements, zero):
    answer = 0
    n = zero
    for _ in range(3):
        for _ in range(1000 % len(all_elements)):
            n = n.next
        answer += n.value
    return answer


def load_elements(decryption_key: int = 1):
    all_elements: list[Element] = []
    zero = None
    for value in get_daily_input(DAY):
        curr_element = Element(int(value) * decryption_key)
        if curr_element.value == 0:
            zero = curr_element
        if all_elements:
            all_elements[-1].next = curr_element
            curr_element.prev = all_elements[-1]
        all_elements.append(curr_element)
    all_elements[-1].next = all_elements[0]
    all_elements[0].prev = all_elements[-1]
    return all_elements, zero


def mix(all_elements, passes: int = 1):
    for _ in range(passes):
        for e in all_elements:
            steps = e.value % (len(all_elements) - 1)
            if steps != 0:
                e.prev.next = e.next
                e.next.prev = e.prev

                new_prev = e.prev
                for _ in range(steps):
                    new_prev = new_prev.next

                e.prev = new_prev
                e.next = new_prev.next
                e.prev.next = e
                e.next.prev = e


def dump(all_elements):
    ce = all_elements[0]
    cv = []
    for i in range(len(all_elements)):
        cv.append(str(ce.value))
        ce = ce.next
    print(", ".join(cv))


def part_1() -> int:
    all_elements, zero = load_elements()
    mix(all_elements)
    answer = find_answer(all_elements, zero)
    return answer


def part_2() -> int:
    all_elements, zero = load_elements(decryption_key=811589153)
    mix(all_elements, passes=10)
    answer = find_answer(all_elements, zero)
    return answer


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()

"""
Part 1: 13522
"""