
class Board:
    def __init__(self, data):
        if isinstance(data, int):
            self.data = self.create_lights(data)
        elif isinstance(data, list):
            assert all([len(el) == len(data) for el in data]), "Not a square"
            self.data = data
        else:
            raise AssertionError("invalid board")

    def __repr__(self):
        str = f"Board({self.data})"
        return str

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.data])

    def print_lights(self, array, raw = True):
        dim = len(array)
        # create lens out of the dims
        lens = [dim]
        for i in range(dim - 1, 0, -1):
            lens.append(i)
            lens.insert(0, i)
        # create the printed matrix
        new = []
        for length in lens:
            new_row = []
            for ri in range(length):
                ri = length - ri - 1
                val = array[ri][0]
                if not raw:
                    val = "X" if val is not None else "0"
                new_row.append(val)
                del array[ri][0]
                if array[ri] == []:
                    del array[ri]
            new.append(new_row)

        return "\n".join([f"{(3 * ' ').join(row).center(4 * dim + 2)}" for row in new])


    def create_coords(self, dim):
        data = []
        for i in range(dim):
            row = []
            for j in range(dim):
                row.append(f"{i}.{j}")
            data.append(row)
        return data

    def create_lights(self, dim):
        data = []
        for i in range(dim):
            row = []
            for j in range(dim):
                row.append(f"{i}.{j}")
            data.append(row)
        return [["X" if (row + col) >= dim else "O" for col in range(dim)] for row in range(dim)]



if __name__ == "__main__":
    board = Board(8)
    print(board)