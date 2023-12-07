from itertools import groupby

CARDS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")


def _parse(data: list[str]) -> list[list[str, int]]:
    return [[line.split()[0], int(line.split()[1])] for line in data]


def _bubble_sort_equal_hands(hands: list[list[str | int]]):
    n = len(hands)
    swapped = False
    # Traverse through all array elements
    for i in range(n - 1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if hands[j][2] == hands[j + 1][2]:
                for (
                    c1,
                    c2,
                ) in zip(hands[j][0], hands[j + 1][0]):
                    if CARDS.index(c2) == CARDS.index(c1):
                        continue
                    if CARDS.index(c2) < CARDS.index(c1):
                        hands[j], hands[j + 1] = hands[j + 1], hands[j]
                        swapped = True
                        break
                    break
        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return


def _determine_hand_value(hand: str) -> int:
    grouped_cards = [len("".join(v)) for _, v in groupby("".join(sorted(hand)))]

    if 5 in grouped_cards:
        return 7
    if 4 in grouped_cards:
        return 6
    if 3 in grouped_cards:
        if 2 in grouped_cards:
            return 5
        return 4
    pairs = grouped_cards.count(2)
    if pairs == 2:
        return 3
    if pairs == 1:
        return 2
    return 1


def part1(_input: list[str]) -> int:
    hands = _parse(_input)
    for hand in hands:
        hand.append(_determine_hand_value(hand[0]))
    sorted_hands = sorted(hands, key=lambda h: h[2])
    _bubble_sort_equal_hands(sorted_hands)
    return sum(hand[1] * (sorted_hands.index(hand) + 1) for hand in sorted_hands)


def part2(_input: list[str]) -> int:
    ...


parts = (part1, part2)
