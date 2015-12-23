import re
import math


projectileMotionKeywords = ["fall","launch", "projectile", "particle kinematics"]
projectileMotionVariables = ["v_o", "v_ox", "v_oy", "distance", "height", "time", "angle"]

def isQuestion(sentence):
    sentence = sentence.lower()
    return True if "what" in sentence or "find" in sentence or "calculate" in sentence or "how" in sentence else False

def isParameter(sentence):
    sentence = sentence.lower()
    return re.search(r"[0-9]", sentence) is not None


def interpretFreeFall(question, params, angleInWholeProblem):
    v_o = None
    h = None
    distance = None
    time = None
    theta = None
    v_ox = None
    v_oy = None
    
    for index, param in enumerate(params):
        param = param.lower()
        words = param.split(" ")
        for wordIndex, word in enumerate(words):
            if(word == "speed" or word == "velocity"):
                v_o = getNumber(words[wordIndex:])
            if(word == "height" or word == "from"):
                h = getNumber(words[wordIndex:])
            if(word == "second" or word == "seconds"):
                try:
                    time = float(words[wordIndex-1])
                except:
                    num = -1
            if(word == "degree" or word == "degrees"):
                theta = float(words[wordIndex-1])
            if(word == "distance" or word == "travels"):
                distance = getNumber(words[wordIndex:])
                
    #h = v_o*t + 1/2 * a*t^2
        
    solveFor = []
    if("long" in question or "time" in question):
        solveFor.append("time")
    if("height" in question or "high" in question or ("fall" in question and ("height" in question or "distance" in question))):
        solveFor.append("height")
    if("speed" in question or "velocity" in question):
        solveFor.append("velocity")
    if("angle" in question or "theta" in question):
        solveFor.append("angle")
    if("distance" in question or "go" in question or "travel" in question or "far" in question):
        solveFor.append("distance")

    if(theta != None):
        v_ox = v_o * math.cos(math.radians(theta))
        v_oy = v_o * math.sin(math.radians(theta))
    elif(not angleInWholeProblem):
        v_oy = v_o
        distance = 0
        v_ox = 0

    if(v_o == None and "velocity" not in solveFor):
        v_o = 0
        v_ox = 0
        v_oy = 0

    data = [v_o, v_ox, v_oy, distance, h, time, theta]
    
    print(data)

    for solve in solveFor:
        out = solveProjectileMotion(data, solve)
        if(out != None):
            formatOutput(out)

def manualInputProjectileMotion():
    data = []
    solveFor = []
    print("Please input all data in SI units. For any unknown values, type ? if you're looking to calculate that value, or - if it does not need to be solved for")
    for index, element in enumerate(projectileMotionVariables):
        response = input("Value of " + str(element) + "?")
        try:
            data.append(float((response).split(" ")[0]))
        except:
            data.append(None)
            if("?" in response):
                solveFor.append(element)

    if("v_o" in x for x in solveFor):
        solveFor.append("velocity")

    for solve in solveFor:
        out = solveProjectileMotion(data, solve)
        if(out != None):
            formatOutput(out)
            

def solveProjectileMotion(data, solveFor):

    countIncrements = 0
    v_oy = data[2]
    v_ox = data[1]
    v_o = data[0]
    distance = data[3]
    h = data[4]
    time = data[5]
    theta = data[6]

    while((v_oy == None or h == None or time == None or distance == None) and countIncrements <= 5):
        countIncrements += 1
        if(v_oy == None and h != None and time != None):
            v_oy = (h-.5*9.8*time**2.0)/time * -1.0
        if(v_ox == None and time != None and distance!= None):
            v_ox = distance / time
        if(h == None and v_oy != None and time != None):
            h = -1.0 * v_oy * time + .5*9.8*time**2.0
        if(time == None and v_oy != None and h != None):
            time = (1.0*v_oy + (v_oy**2 + 2*9.8*h)**0.5)/9.8
        if(distance == None and v_oy != None and h != None and v_ox != None):
            distance = (1.0*v_oy + (v_oy**2 + 2*9.8*h)**0.5)/9.8 * v_ox
        if(theta == None and v_ox != None and v_oy != None and "angle" in solveFor):
            theta = math.degrees(math.atan(v_oy/v_ox))
        if(v_ox == None and v_o != None and v_oy != None):
            v_ox = (v_o**2 - v_oy**2)**0.5
        if(v_oy == None and v_o != None and v_ox != None):
            v_oy = (v_o**2 - v_ox**2)**0.5
        data = [v_o, v_ox, v_oy, distance, h, time, theta]
        #print(data)


    if("velocity" in solveFor):
        return [v_ox, "m/s", v_oy,"m/s"]
    if("height" in solveFor):
        return [h, "m"]
    if("time" in solveFor):
        return [time, "s"]
    if("distance" in solveFor):
        return [distance, "m"]
    if("angle" in solveFor):
        return [theta, "degrees"]

    return None
            

def getNumber(words):
    for word in words:
        if(isNumber(word)):
            return float(word)
            

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
            
    if(("fall" in q for q in questions or hotword in p for hotword in projectileMotionKeywords for p in parameters) and "y" in input("Is this a Free Fall Problem? (Y/N)").lower()):
        for q in questions:
            interpretFreeFall(q, parameters, "angle" in problem or "theta" in problem)
            
    else:
        print("unrecognized problem type")

def formatOutput(result):
    output = ""
    for index, res in enumerate(result):
        if(index%2 == 0):
            output += str(res)[:5] + result[index+1] + ","
    output = output[:-1]
    print(output)
    
def manualInput():
    problemType = input("What kind of problem would you like to solve?")
    if(key in word for key in projectileMotionKeywords for word in problemType.split(" ")):
        manualInputProjectileMotion()

def main():
    while(True):
        problem = input("Enter Problem Here or type 'manual' for manual data input")
        if(problem == "end"):
            return
        elif("manual" in problem.lower()):
            manualInput()
        else:
            process(problem)

main()
