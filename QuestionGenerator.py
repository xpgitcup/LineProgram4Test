from random import randint

class QuestionGenerator:
    vectorC = []
    matrixA = []
    vectorB = []
    goalType = True # 求最大
    sense = ["<=", "=", ">="]

    def createQuestion(self, numberOfDecision, numberOfSubject):
        for i in range(numberOfDecision):
            self.vectorC.append(randint(1, 10))

        for i in range(numberOfSubject):
            self.vectorB.append(randint(1,20))
            row = []
            for j in range(numberOfDecision):
                row.append(randint(0, 20))
            self.matrixA.append(row)
        print(self.vectorC)
        print(self.matrixA)
        print(self.vectorB)

        ofile = open("paper.dat", "wt")
        lines = []
        # 第一行
        vc = "MAX"
        for i in range(len(self.vectorC)):
            vc += " %3d" % (self.vectorC[i])
        vc += "\n"
        print("第一行", vc)
        lines.append(vc)

        # 约束矩阵
        for i in range(len(self.matrixA)):
            tmp = ""
            for j in range(len(self.matrixA[i])):
                tmp += " %3d" % (self.matrixA[i][j])
            k = 0 #randint(0,2)
            tmp += " %3s" % (self.sense[k])
            tmp += " %3d" % (self.vectorB[i])
            tmp += "\n"
            lines.append(tmp)
        ofile.writelines(lines)
        ofile.close()
        return
