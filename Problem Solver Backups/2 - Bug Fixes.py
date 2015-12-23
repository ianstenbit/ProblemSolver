import re
import math

def isQuestion(sentence):
    sentence = sentence.lower()
    return True if "what" in sentence or "find" in sentence or "calculate" in sentence or "how" in sentence else False

def isParameter(sentence):
    sentence = sentence.lower()
    return re.search(r"[0-9]", sentence) is not None

def solve(question, params):
    #print("Solving the question " + question + " using parameters " + str(params))
    question = question.lower()
    if(("fall" in question or "fall" in p for p in params or "launch" in p for p in params) and "y" in input("Is this a Free Fall Problem? (Y/N)").lower()):
        #print("Solving as free fall problem!")
        result = solveFreeFall(question, params)
        print(result)
        output = ""
        for index, res in enumerate(result):
            if(index%2 == 0):
                output += str(res)[:5] + result[index+1] + ","
        output = output[:-1]
        print(output)
       # WHY U NO WORK? print(((str(res)[:5]) + res[index+1]) for index, res in enumerate(result) if index%2 == 0)

def solveFreeFall(question, params):
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
                time = float(words[wordIndex-1])
            if(word == "degree" or word == "degrees"):
                theta = float(words[wordIndex-1])
            if(word == "distance" or word == "travels"):
                distance = getNumber(words[wordIndex:])
                
    #h = v_o*t + 1/2 * a*t^2

    data = [v_o, v_ox, v_oy, distance, h, time, theta]
    #print(data)
        
    solveFor = []
    if("long" in question or "time" in question):
        solveFor.append("time")
    if("height" in question or ("fall" in question and ("height" in question or "distance" in question))):
        solveFor.append("height")
    if("speed" in question or "velocity" in question):
        solveFor.append("velocity")
    if("angle" in question or "theta" in question):
        solveFor.append("angle")
    if("distance" in question or "go" in question or "travel" in question):
        solveFor.append("distance")

    if(theta != None):
        v_ox = v_o * math.cos(math.radians(theta))
        v_oy = v_o * math.sin(math.radians(theta))
    elif("angle" not in solveFor):
        v_oy = v_o
        distance = 0
        v_ox = 0

    if(v_o == None and "velocity" not in solveFor):
        v_o = 0
        v_ox = 0
        v_oy = 0

    while(v_oy == None or h == None or time == None or distance == None):
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
        if(theta == None and v_ox != None and v_oy != None and "theta" in solveFor):
           theta = math.degrees(math.atan(v_oy/v_ox))
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
            questions.append(sentence)
        if(isParameter(sentence)):
            parameters.append(sentence)
    #print(questions)
    #print(parameters)
    for q in questions:
        solve(q, parameters)
            

def main():
    while(True):
        problem = input("Enter Problem Here")
        if(problem == "end"):
            return
        else:
            process(problem)

main()
