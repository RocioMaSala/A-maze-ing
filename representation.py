
bin_list = []

def representation (maze: list[list[int]]) -> None:
    for row in maze:
        for byte in row: # ahora tengo un laberinto binario. tengo que analizar cada byte para ver dónde poner la pared. 
            
        

def hexatodectobin(maze: list[list[str]]) -> None:
    for row in maze:
        bin_row = []
        for number in row:
            decimal_num = int(number, 16)
            bin_num = format(decimal_num, "04b")
            bin_row.append(bin_num)
        print(bin_row)
        bin_list.append(bin_row)

if __name__ == "__main__":
    hexatodectobin([["A", "F"], ["1", "6"]])
