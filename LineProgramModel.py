import sys

class LineProgramModel:
    # 这里定义类的属性
    M = 1000
    vectorC = []
    vectorB = []
    matrixA = []
    baseVector = []
    goalType = True         # 求最大
    decisionVector = []
    constraintType = []     # 约束类型
    varIndex = []           # 变量索引
    # 约束个数
    numberOfsubject = 0
    # 决策变量个数
    numberOfdecision = 0
    # 方法名称
    method = ["普通单纯形法", "大M法", "两阶段法"]
    currentMethodIndex = 0

    # 初始化模型
    def initModel(self, dataLines):
        print("初始化模型：")

        # 首先计算约束数、变量数
        self.numberOfsubject = dataLines.__len__() - 1  # 约束数量 = 总数 - 1
        print("约束数：", self.numberOfsubject)

        # 首先切分字符串
        gstring = dataLines[0].split()
        self.numberOfdecision = gstring.__len__() - 1  # 决策变量个数 = 第一行的列数 - 1
        print("决策变量数：", self.numberOfdecision)

        # 解析目标函数
        if (gstring[0].upper() != "MAX"):
            self.goalType = False
        print("目标函数类型：", self.goalType)

        # 解析目标函数
        m = gstring.__len__()
        print(m)
        for j in range(1, gstring.__len__()):
            v = float(gstring[j])
            self.vectorC.append(v)
        print("目标函数：", self.vectorC)
        for k in range(0, self.vectorC.__len__()):
            self.varIndex.append("控制变量")

        # 解析约束矩阵 && 资源向量 && 约束类型
        for i in range(1, dataLines.__len__()): # 约束从第一行开始
            gstring = dataLines[i].split()
            print(gstring)

            # 解析约束矩阵的每一行
            row = []
            for j in range(0, self.numberOfdecision):
                v = float(gstring[j])
                row.append(v)
            self.matrixA.append(row)

            # 约束类型
            self.constraintType.append(gstring[self.numberOfdecision])

            # 资源向量
            v = float(gstring[self.numberOfdecision + 1])
            self.vectorB.append(v)

        self.displayModel("初始化模型:")
        return

    def displayModel(self, label):
        print()
        print(label)
        print("目标：", self.goalType)
        print("价值向量：", self.vectorC)
        print("约束矩阵：", self.matrixA)
        print("约束类型：", self.constraintType)
        print("资源向量：", self.vectorB)
        print("变量统计：", self.varIndex)
        print("基变量：", self.baseVector)
        print("---------------------------------------------------")

    # 增加变量，baseValue ==  True 是1， False 是 -1
    def addVariable(self, indexOfConstraint, baseValue):
        for i in range(self.matrixA.__len__()):
            if (i == indexOfConstraint):
                if (baseValue):
                    self.matrixA[i].append(1.0)
                else:
                    self.matrixA[i].append(-1.0)
            else:
                self.matrixA[i].append(0.0)
        print("增加了变量[%d]: " % indexOfConstraint, indexOfConstraint, "  ", self.matrixA)
        return

    # 增加松弛变量
    def addRelaxationVariable(self, indexOfConstraint):
        self.varIndex.append("松弛变量")
        self.addVariable(indexOfConstraint, True)
        return

    # 增加剩余变量、增加人工变量
    def addRemainingVariable(self, indexOfConstraint):
        self.varIndex.append("剩余变量")
        self.addVariable(indexOfConstraint, False)
        self.varIndex.append("人工变量")
        self.addVariable(indexOfConstraint, True)
        return

    # 增加剩余变量、增加人工变量
    def addRengongVariable(self, indexOfConstraint):
        self.varIndex.append("人工变量")
        self.addVariable(indexOfConstraint, True)
        return

    # 标准化
    def standardization(self):
        print("标准化...")
        varMap = {
            "<=": self.addRelaxationVariable,
            ">=": self.addRemainingVariable,
            "=" : self.addRengongVariable
        }
        # 增加松弛变量、剩余变量、人工变量
        for i in range(self.constraintType.__len__()):
            # print(self.constraintType[i])
            varMap[self.constraintType[i]](i)

        # 构造初始可行基
        self.baseVector.clear()
        for i in range(0, self.varIndex.__len__()):
            if ((self.varIndex[i] == "松弛变量") or (self.varIndex[i] == "人工变量")):
                self.baseVector.append(i)   # 登记该变量的索引

        # 方法选择
        if ("人工变量" in self.varIndex):
            #print("可选：", self.method)
            #self.currentMethodIndex = int(input("由于存在人工变量，请输入选择[1,2]："))
            self.currentMethodIndex = 1
        print("您选择了：", self.method[self.currentMethodIndex])
        methodMap = {
            0: self.normalSimplex,
            1: self.bigMSimplex,
            2: self.twoPhaseSimplex
        }

        methodMap[self.currentMethodIndex]()

        # 更新控制变量个数
        self.numberOfdecision = self.vectorC.__len__()

        self.displayModel("标准化：")
        return

    # 普通单纯形法
    def normalSimplex(self):
        for i in range(0, self.varIndex.__len__()):
            if (self.varIndex[i] != "控制变量"):
                self.vectorC.append(0)  # 扩展价值向量--与求解算法有关

    def expandVectorCByNone(self):
        return

    def expandVectorCByZero(self):
        self.vectorC.append(0)
        return

    def expandVectorCByM(self):
        self.vectorC.append(self.M)
        return

    # 大M单纯形法
    def bigMSimplex(self):
        vMap = {
            "控制变量": self.expandVectorCByNone,
            "松弛变量": self.expandVectorCByZero,
            "剩余变量": self.expandVectorCByZero,
            "人工变量": self.expandVectorCByM
        }
        for i in range(0, self.varIndex.__len__()):
            vMap[self.varIndex[i]]()

    # 两阶段法
    def twoPhaseSimplex(self):
        for i in range(0, self.varIndex.__len__()):
            if (self.varIndex[i] != "控制变量"):
                self.vectorC.append(0)  # 扩展价值向量--与求解算法有关

    # 计算检验数
    def calculateCheckNumber(self):
        checkNumber = []
        for i in range(0, self.numberOfdecision):
            checkNumber.append(0.0)

        for i in range(0, self.numberOfdecision):
            temp = 0
            for j in range(0, self.numberOfsubject):
                temp += self.vectorC[self.baseVector[j]] * self.matrixA[j][i]
            checkNumber[i] = self.vectorC[i] - temp
        print("检验数：", checkNumber)
        return checkNumber

    # 找到最优的检验数，确定换入变量
    def searchCheckNumber(self, checkNumber):
        if (self.goalType):
            optCheckNumber = max(checkNumber)
        else:
            optCheckNumber = min(checkNumber)
        optCheckNumberIndex = checkNumber.index(optCheckNumber)
        print("最优检验数：", optCheckNumber, "索引：", optCheckNumberIndex)
        return [optCheckNumberIndex, optCheckNumber]

    def calculateXita(self, maxCheckNumberIndex):
        vectorXita = []
        for i in range(0, self.numberOfsubject):
            if (self.matrixA[i][maxCheckNumberIndex] > 0):
                vectorXita.append(self.vectorB[i] / self.matrixA[i][maxCheckNumberIndex])
            else:
                vectorXita.append(None)
        print("西塔：", vectorXita)
        return vectorXita

    def searchXita(self, vectorXita):
        tempV = []
        for i in range(0, vectorXita.__len__()):
            if (vectorXita[i] != None):
                tempV.append(vectorXita[i])
            else:
                tempV.append(sys.maxsize)
        minXita = min(tempV)
        minXitaIndex = vectorXita.index(minXita)
        print("最小的西塔：", minXita, "索引：", minXitaIndex)
        return minXitaIndex

    def elimination(self, inIndex, outIndex):
        self.mainE = self.matrixA[outIndex][inIndex]
        #处理主元所在行
        for i in range(0, self.numberOfdecision):
            self.matrixA[outIndex][i] /= self.mainE
        #处理资源向量
        self.vectorB[outIndex] /= self.mainE

        for i in range(0, self.numberOfsubject):
            tempA = self.matrixA[i][inIndex]
            if (i != outIndex):
                for j in range(0, self.numberOfdecision):
                    self.matrixA[i][j] -= self.matrixA[outIndex][j] * tempA
                self.vectorB[i] -= self.vectorB[outIndex] * tempA
            print(self.matrixA[i])

        print("完成消元：")
        print("约束矩阵：", self.matrixA, "资源向量：", self.vectorB)

        self.baseVector[outIndex] = inIndex
        print("当前基变量；", self.baseVector)
        return

    # 计算目标函数值
    def getOptGoal(self):
        # 初始化控制变量
        self.decisionVector.clear()
        for i in range(0, self.varIndex.__len__()):
            self.decisionVector.append(0.0)
        # 登记求解结果
        for i in range(0, self.numberOfsubject):
            self.decisionVector[self.baseVector[i]] = self.vectorB[i]
        print("决策变量：", self.decisionVector)

        goal = 0
        for i in range(0, self.numberOfdecision):
            goal += self.decisionVector[i] * self.vectorC[i]
        print("目标函数值；", goal)

    def doIterate(self):
        ik = 0
        while True:
            # 函数调用
            self.getOptGoal()
            checkNumber = self.calculateCheckNumber()
            [optCheckNumberIndex, optCheckNumber] = self.searchCheckNumber(checkNumber)
            print("最优的检验数：%f" % optCheckNumber)
            if (optCheckNumber == 0.0):
                break
            vectorXita = self.calculateXita(optCheckNumberIndex)
            minXitaIndex = self.searchXita(vectorXita)
            self.elimination(optCheckNumberIndex, minXitaIndex)
            ik += 1

        print("计算完成！ 总计", ik, "步迭代.")
        return
