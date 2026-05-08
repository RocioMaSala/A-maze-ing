
bin_list = []


def representation(maze: list[list[int]]) -> None:
    for row in maze:
        line = ""
        for block in row:
            if block == "1111":
                line += "||"
            else:
                line += "no"
        print(line)


def hexatodectobin(maze: list[list[str]]) -> None:
    for row in maze:
        bin_row = []
        for number in row:
            decimal_num = int(number, 16)
            bin_num = format(decimal_num, "04b")
            bin_row.append(bin_num)
        bin_list.append(bin_row)
    print(bin_list)
    return bin_list


if __name__ == "__main__":
    representation(hexatodectobin([["1", "5"
    ""], ["1", "6"]]))
