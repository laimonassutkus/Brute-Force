class Reader:
    path = ""

    def __init__(self, path):
        self.path = path

    def read_input(self):
        matrix = []
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
            matrix.append(0 if index == -1 else index + 1)  # re-invert back to negative case

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
                output_file.write("\tQ" if value == row + 1 else "\t-")

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

    def __init__(self, path, matrix):
        self.path = path
        self.matrix = matrix
        self.writer = Writer(path)
        self.writer.reset_output_file()

    def solve(self):
        # Note that first row or column is indexed with 1 but not 0
        self._place_queen(1)

    def _place_queen(self, row):
        column = 1
        while column <= len(self.matrix):
            if self.is_valid((row, column)):
                self.matrix[row - 1] = column
                if row == len(self.matrix):
                    self.writer.print_answer(self.matrix, "\n\n{} solution: {} {}".format("-" * 10, self.solution_number, "-" * 10))
                    self.solution_number += 1
                self._place_queen(row + 1)
            column += 1

    def is_valid(self, coordinates):
        index = 1
        while index <= coordinates[0] - 1:
            if self.matrix[index - 1] == coordinates[1]:
                return False
            elif abs(self.matrix[index - 1] - coordinates[1]) == abs(index - coordinates[0]):
                return False
            index += 1
        return True


# Read inputs from a file
reader = Reader("./input.txt")
m = reader.read_input()

solver = Solver("./output.txt", m)
#solver.solve()
print solver.is_valid((1,1))
'''
Some stuff to carry:

print "Coordiantes: {},{}, Is valid: {}.".format(row, column, Solver.is_valid((row, column), given_matrix))
'''
