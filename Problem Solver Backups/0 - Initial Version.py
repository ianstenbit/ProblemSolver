import re

def isQuestion(sentence):
    sentence = sentence.lower()
    return True if "what" in sentence or "find" in sentence or "calculate" in sentence or "how" in sentence else False

def isParameter(sentence):
    sentence = sentence.lower()
    return re.search(r"[0-9]", sentence) is not None

def solve(question, params):
    #print("Solving the question " + question + " using parameters " + str(params))
    question = question.lower()
    if(("fall" in question or "fall" in p for p in params) and "y" in input("Is this a Free Fall Problem? (Y/N)").lower()):
        #print("Solving as free fall problem!")
        result = solveFreeFall(question, params)
        print(str(result[0])[:6] + result[1])

def solveFreeFall(question, params):
    v_o = None
    h = None
    time = None
    for index, param in enumerate(params):
        param = param.lower()
        words = param.split(" ")
        for wordIndex, word in enumerate(words):
            if(word == "speed" or word == "velocity"):
                v_o = getNumber(words[wordIndex:])
            if(word == "height" or word == "distance"):
                h = getNumber(words[wordIndex:])
            if(word == "second" or word == "seconds"):
                time = float(words[wordIndex-1])
    data = [v_o, h, time]
    #print(data)
    #h = v_o*t + 1/2 * a*t^2
    if(v_o == None):
        v_o = (h-.5*9.8*time**2.0)/time * -1.0
        return [v_o,"m/s"]
    if(h == None):
        h = -1.0 * v_o * time + .5*9.8*time**2.0
        return [h, "m"]
    if(time == None):
        time = (1.0*v_o + (v_o**2 + 2*9.8*h)**0.5)/9.8
        return [time, "s"]
            

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
