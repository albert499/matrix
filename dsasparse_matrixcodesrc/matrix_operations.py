class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        self.numRows = 0
        self.numCols = 0
        self.elements = {}  # Dictionary to store {(row, col): value}
        
        if matrixFilePath:
            self._load_from_file(matrixFilePath)
        elif numRows is not None and numCols is not None:
            self.numRows = numRows
            self.numCols = numCols

    def _load_from_file(self, matrixFilePath):
        """Loads sparse matrix from a given file"""
        try:
            with open(matrixFilePath, 'r') as file:
                # Read matrix dimensions
                first_line = file.readline().strip()
                if first_line.startswith("rows="):
                    self.numRows = int(first_line.split('=')[1])
                else:
                    raise ValueError("Input file has wrong format")

                second_line = file.readline().strip()
                if second_line.startswith("cols="):
                    self.numCols = int(second_line.split('=')[1])
                else:
                    raise ValueError("Input file has wrong format")

                # Read matrix entries
                for line in file:
                    line = line.strip()
                    if line == "":
                        continue  # Ignore blank lines
                    
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")

                    try:
                        # Parse the (row, col, value) tuple
                        row, col, value = map(int, line[1:-1].split(','))
                        self.set_element(row, col, value)
                    except Exception:
                        raise ValueError("Input file has wrong format")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {matrixFilePath} not found")

    def get_element(self, row, col):
        """Returns the value at (row, col) or 0 if no value is set"""
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        """Sets the value at (row, col). If value is zero, removes the element."""
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def __add__(self, other):
        """Adds two sparse matrices"""
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition.")
        
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value + other.get_element(row, col))

        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, value)
        
        return result

    def __sub__(self, other):
        """Subtracts two sparse matrices"""
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction.")
        
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value - other.get_element(row, col))

        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.set_element(row, col, -value)

        return result

    def __mul__(self, other):
        """Multiplies two sparse matrices"""
        if self.numCols != other.numRows:
            raise ValueError("Matrices dimensions are incompatible for multiplication.")
        
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        
        for (row, col), value in self.elements.items():
            for other_col in range(other.numCols):
                product = value * other.get_element(col, other_col)
                if product != 0:
                    result.set_element(row, other_col, result.get_element(row, other_col) + product)
        
        return result

    def display(self):
        """Display the matrix in a sparse format"""
        print(f"Matrix ({self.numRows}x{self.numCols}):")
        for (row, col), value in self.elements.items():
            print(f"({row}, {col}, {value})")

def read_input_files():
    """Pre-populated file paths for the matrices"""
    matrix_file1 = "C:/Users/LENOVO/OneDrive/Desktop/matrix/dsasparse_matrixsample_inputs/matrixfile1.txt"
    matrix_file2 = "C:/Users/LENOVO/OneDrive/Desktop/matrix/dsasparse_matrixsample_inputs/matrixfile2.txt"

    matrix1 = SparseMatrix(matrix_file1)
    matrix2 = SparseMatrix(matrix_file2)
    
    return matrix1, matrix2

def main():
    try:
        # Load matrices from input files
        matrix1, matrix2 = read_input_files()

        # Prompt user to choose an operation
        operation = input("Choose an operation - Add (1), Subtract (2), Multiply (3): ").strip()

        if operation == '1':
            result = matrix1 + matrix2
            print("Result of addition:")
        elif operation == '2':
            result = matrix1 - matrix2
            print("Result of subtraction:")
        elif operation == '3':
            result = matrix1 * matrix2
            print("Result of multiplication:")
        else:
            print("Invalid operation")
            return
        
        result.display()
    
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

