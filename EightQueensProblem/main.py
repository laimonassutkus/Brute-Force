import os.path as path


class Reader:
    path = ""

    def __init__(self, path):
        self.path = path

    def read_input(self):
        matrix = []

        # check if provided path points to a valid file
        if not path.isfile(self.path):
            raise EnvironmentError("File in provided path does not exit.")

        input_file = open(self.path, "r")
        lines = input_file.read().splitlines()
        matrix_size = lines.pop(0)

        try:
            matrix_size = int(matrix_size)
        except ValueError:
            raise ValueError("Matrix size specifier must be an integer.")

        if len(lines) != matrix_size:
            raise ValueError("The number of lines must be {}.".format(matrix_size))

        for line in lines:
            if len(line) != matrix_size:
                raise ValueError("The length of lines must be {}.".format(matrix_size))

            index = line.find("*")
            # for each row we place 0 if there is no queen and n (n>0) for a queens position
            # note that now the first position is not '0' but '1'
            # then n is inverted to indicate an immovable queen
            matrix.append(0 if index == -1 else -index - 1)

        input_file.close()
        return matrix


class Writer:
    path = ""

    def __init__(self, path):
        self.path = path

    def print_answer(self, matrix, title):
        output_file = open(self.path, "a")

        output_file.write(title)

        for value in matrix:
            output_file.write("\n")
            for row in range(len(matrix)):
                output_file.write("\tQ" if abs(value) == row + 1 else "\t-")

        output_file.write("\n")
        output_file.close()

    def reset_output_file(self):
        output_file = open(self.path, "w")
        output_file.close()


class Solver:
    path = ""
    matrix = []
    writer = None
    solution_number = 1

    # a magic variable to determine recursion direction
    begin = True

    def __init__(self, path, matrix):
        self.path = path
        self.matrix = matrix
        self.writer = Writer(path)
        self.writer.reset_output_file()

    def solve(self):
        # Note that first row or column is indexed with 1 but not 0
        self._place_queen(1)

    def _place_queen(self, row):
        self.begin = True
        column = 1
        while column <= len(self.matrix):

            if row > len(self.matrix):
                return

            # Skip row if there are any static queens
            if self.matrix[row - 1] < 0 and self.begin:
                self._place_queen(row + 1)

            # Skip row if there are any static queens
            if self.matrix[row - 1] < 0 and not self.begin:
                return

            if self.is_valid((row, column)):
                self.matrix[row - 1] = column
                if row == len(self.matrix):
                    self.writer.print_answer(self.matrix,
                                             "\n\n{} solution: {} {}".format("-" * 10, self.solution_number, "-" * 10))
                    self.solution_number += 1
                self._place_queen(row + 1)
                self.begin = False
            column += 1

    def is_valid(self, coordinates):
        index = 1
        while index <= len(self.matrix):
            if index <= coordinates[0] - 1 or self.matrix[index - 1] < 0:
                temp = abs(self.matrix[index - 1])
                if temp == coordinates[1]:
                    return False
                elif abs(temp - coordinates[1]) == abs(index - coordinates[0]):
                    return False
            index += 1
        return True


# read inputs from a file
reader = Reader("./input.txt")
m = reader.read_input()

# solve matrix
solver = Solver("./output.txt", m)
solver.solve()