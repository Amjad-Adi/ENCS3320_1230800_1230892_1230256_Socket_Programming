import random 

def generateQuesSequence (count) :
    numbers = []
    for i in range (1,count):
        numbers.append(i)
    random.shuffle(numbers) 
    return numbers

def quesList():
    questionList=[]
    try:
        quesFile=open("Question file.txt","r")
    except:
        print("There is no file")
        exit()
    fileInfo=quesFile.read()
    quesInfo=fileInfo.split("\n$\n")
    for question in quesInfo:
        questionList.append(question.split("\n#\n"))
    return questionList

def checkAnswers(questions,order,clientAnswer,n=5) :
    correctAnswer  = questions[order-1][-1].strip()
    return correctAnswer.lower() == clientAnswer.lower()

questions = quesList ()
orderList = generateQuesSequence(len(questions))
print(orderList)
score = 0 
for order in orderList:
    print(questions[order-1][0]+"\n")
    clinetAnswer = input("Your Answer : ")
    if checkAnswers(questions, order,clinetAnswer) :
        print ("Correct \n")
        score += 1 
    else :
        print ("Wrong \n")

print(f"Final Score: {score}/{len(questions)-1}")
