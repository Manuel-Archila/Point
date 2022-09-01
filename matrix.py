class M(object):
    def __init__(self, mat):
        self.mat = mat


    def __mul__(self, other):
        try:
            resultado = []
            for i in range(len(self.mat)):
                resultado.append([])
                for j in range(len(other.mat[0])):
                    resultado[i].append([])
                    rep = 0
                    for k in range(len(other.mat)):
                        rep += self.mat[i][k] * other.mat[k][j]
                    resultado[i][j] = rep
            return M(resultado)
        except:
            print("Error")
    