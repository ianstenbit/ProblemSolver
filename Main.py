import re
import Projectiles



def main():
    while(True):
        problem = input("Enter Problem Here or type 'manual' for manual data input")
        if(problem == "end"):
            return
        elif("manual" in problem.lower()):
            manualInput()
        else:
            process(problem)

def isQuestion(sentence):
    sentence = sentence.lower()
    return True if "what" in sentence or "find" in sentence or "calculate" in sentence or "how" in sentence else False

def isParameter(sentence):
    sentence = sentence.lower()
    return re.search(r"[0-9]", sentence) is not None
    
def manualInput():
    problemType = input("What kind of problem would you like to solve?")
    if(key in word for key in Projectiles.keywords for word in problemType.split(" ")):
        Projectiles.manualInput()


def process(problem):
    #print(problem)
    sentences = re.split("[!?.] ", problem)
    #print(sentences)
    questions = []
    parameters = []
    for sentence in sentences:
        if(isQuestion(sentence)):
            quests = sentence.split("and")
            questions += quests 
        if(isParameter(sentence)):
            parameters.append(sentence)

    #print(questions)
    #print(parameters)
            
    if(("fall" in q for q in questions or hotword in p for hotword in projectileKeywords for p in parameters) and "y" in input("Is this a Free Fall Problem? (Y/N)").lower()):
        for q in questions:
            Projectiles.interpret(q, parameters, "angle" in problem or "theta" in problem, "velocity" in problem or "speed" in problem)
            
    else:
        print("unrecognized problem type")

main()
