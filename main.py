from LineProgramModel import LineProgramModel
from QuestionGenerator import QuestionGenerator

#这里是主程序
question = QuestionGenerator()
question.createQuestion(3,4)

model = LineProgramModel()

#filename = input("请输入数据文件名：")
#filename = "p.13.例3.dat"
#filename = "p.33.例8.dat"
#filename = "p.48.例10.dat"
filename = "paper.dat"
try:
    with open(filename) as sourceFile:
        dataLines = sourceFile.readlines()
        print(dataLines)
    model.initModel(dataLines)
    model.standardization()
    model.doIterate()
    print()
    model.getOptGoal()
    print("计算完成...")
except IOError:
    print("文件不存在...")
print("Bye...")