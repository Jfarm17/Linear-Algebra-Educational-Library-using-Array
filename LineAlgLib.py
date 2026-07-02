from array import array

class Matrix:
    def __init__(self, rows):
        self.rows = [array('f', row) for row in rows]
        self.num_rows = len(self.rows)
        self.num_cols = len(self.rows[0]) if self.rows else 0
    def display(self):
        for row in self.rows:
            print(" ".join(str(x) for x in row))
    def get_col(self, j):
        return array('f', [row[j] for row in self.rows])
    def __add__(self, other):
        #Adding a matrix with another matrix 
        if self.num_rows != other.num_rows and self.num_cols != other.num_cols:
            raise ValueError("There is a shape mismatch")
        results_rows = []
        for i in range(self.num_rows):
            new_row = array('f')
            for j in range(self.num_cols):
                value = self.rows[i][j] + other.rows[i][j]
                new_row.append(value)
            results_rows.append(new_row)
        return Matrix(results_rows)

    def __matmul__(self, other):
        #Matrix multiplication
        if self.num_cols != other.num_rows: 
            raise ValueError("There is a shape mismatch for matrix multiplication")
        
        results_rows = []
        for i in range(self.num_rows):
            new_row = array('f')

            for j in range(other.num_cols):
                row = self.rows[i]
                col = other.get_col(j)
                value = 0.0 
                for k in range(len(col)):
                    value += row[k] * col[k]
                new_row.append(value)
            results_rows.append(new_row)
        return Matrix(results_rows)
    def dimensions(self):
        return self.num_rows, self.num_cols
    def transpose(self):
        transposed_matrix = []
        for j in range(len(self.rows[0])):
            column = array('f')
            #print(self.rows[0][j])
            for i in range(self.num_rows):
                column.append(self.rows[i][j])
            transposed_matrix.append(column)
        return Matrix(transposed_matrix)
    @staticmethod
    def zero_matrix(row_num, col_num):
        matrix_build = []
        if type(row_num) != int or type(col_num) != int:
            raise TypeError("Not an integer in terms of the amount of rows/columns in a matrix")
        for i in range(int(row_num)):
            array_add = array('f')
            for j in range(col_num):
                array_add.append(0)
            matrix_build.append(array_add)
        return Matrix(matrix_build)
    @staticmethod
    def identity_matrix(row_num, col_num):
        if type(row_num) != int or type(col_num) != int:
            raise TypeError("Not an integer in terms of the amount of rows/columns in a matrix")
        if row_num != col_num:
            raise ValueError("Row and column size mismatch")
        matrix_build = []
        for i in range(row_num):
            array_add = array('f')
            for j in range(col_num):
                if i == j:
                    array_add.append(1.0)
                else:
                    array_add.append(0)
            matrix_build.append(array_add)
        return Matrix(matrix_build)



class Vector(Matrix):
    def __init__(self, values):
        self.values = array('f', values)
    def _operation(self, other, operation):
        '''This is a helper function utilized to determine operations between vectors for an array in a matrix and follow the logic ruleset needed for mathematical 
        vector operations'''
        if type(self) != type(other) and type(self) != array:
            raise TypeError("Objects must be of the same type. Column vector or Row vector")
        else: 
            if len(self.values) != len(other.values):
                raise ValueError("The length of the vector must be the same")
            else:
                return_arr = array('f')
                for i in range(len(self.values)):
                    return_arr.append(operation(self.values[i], other.values[i]))
                return type(self)(return_arr)

    def __add__(self, other):
        return self._operation(other, lambda a, b: a + b)
    def __sub__(self, other):
        return self._operation(other, lambda a, b: a - b)
    def __mul__(self, scalar):
        #Scalar multiplication 
        if type(scalar) != float and type(scalar) != int:
            raise TypeError("This is scalar multiplication and needs a integer or float to scale a vector")
        else:
            return_arr = array('f')
            for i in range(len(self.values)):
                return_arr.append(self.values[i] * scalar)
            return type(self)(return_arr)
    def __matmul__(self, vector):
        #Vector Multiplication
        if type(self.values) != type(vector.values) and type(vector.values) != array:
            raise TypeError("The types are mismatched or the vectors are not arrays")
        else:
            if len(self.values) != len(vector.values):
                raise ValueError("The length of these vectors are not the same")
            else: 
                return_arr = array('f')
                for i in range(len(self.values)):
                    return_arr.append(self.values[i] * vector.values[i])
                return type(self)(return_arr)
    def dot(self, vector):
        if type(self.values) != type(vector.values) and type(vector.values) != array:
            raise TypeError("The types are mismatched or the vectors are not arrays")
        if len(self.values) != len(vector.values):
                raise ValueError("The length of these vectors are not the same")
        return_arr = array('f')
        for i in range(len(self.values)):
            return_arr.append(self.values[i] * vector.values[i])
        value = 0.0
        for item in return_arr:
            value += item 
        return value

class Column(Vector):
    pass
    def __matmul__(self, other):
        if type(self) == type(other):
            raise TypeError("Type error. Column vector cannot multiply against itself")
        if type(self.values) != type(other.values) and type(other.values) == array:
            raise TypeError("Need a row vector in conjunction with a column vector")
        if len(self.values) != len(other.values):
            raise ValueError("Shape mismatch")
        matrix_build = []
        for i in range(len(self.values)):  
            add_array = array('f') 
            for j in range(len(other.values)):
                add_array.append(self.values[i] * other.values[j])
            matrix_build.append(add_array)
        return Matrix(matrix_build)

class Row(Vector):
    pass 
    def __matmul__(self, other):
            if type(self) == type(other):
                raise TypeError("Type error. Row vector cannot multiply against itself")
            else:
                if type(self.values) != type(other.values) and type(other.values) == array:
                    raise TypeError("Need a row vector in conjunction with a column vector")
                if len(self.values) != len(other.values):
                    raise ValueError("Shape mismatch")
                matrix_build = []
                for i in range(len(self.values)):  
                    add_array = array('f') 
                    for j in range(len(other.values)):
                        add_array.append(self.values[i] * other.values[j])
                    matrix_build.append(add_array)
                return Matrix(matrix_build)


c = Column([1, 2, 3])
c2 = Column([1, 3, 5])
r = Row([2, 3, 4])
r2 = Row([3, 4, 5])
#print(c.values)
#print(r.values)

v3 = c - c2
print(type(v3.values))

scal = c * 2.3
print(scal.values)

dot_prod = c.dot(c2)
print('Dot Prod', dot_prod)

A = Matrix([
    [1, 2, 3],
    [4, 5, 6]
    ])

B = Matrix([
    [7, 8],
    [9, 10],
    [11, 12]
])

C = A @ B

B = Matrix([
    [7, 8, 9],
    [10, 11, 12]
])
D = A + B

print(C.display())
print(D.display())
print(type(D.dimensions()))
#print(A)
#print(A.display())
#A = [[2,3,5], [5, 6,7], [8, 4,10]]


print(B.display())
print('\n\nTransposed Matrix:\n ')
print(B.transpose().display())

vect_matrix = c2 @ r 
print(vect_matrix)
print(vect_matrix.display())

#vect_mex_2 = c2 @ c
print(type(r))
print(type(r2))
vect_mex_2 = r2 @ c
print(vect_mex_2.display())

z = Matrix.zero_matrix(3, 4)
print(z.display())



#Identity Matrix Test 
t = Matrix.identity_matrix(5, 5)
print(t.display())
print(t.dimensions())
print(type(t))
