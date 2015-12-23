import re
import math
import Util


keywords = ["fall","launch", "projectile", "particle kinematics"]
variables = ["v_o", "v_ox", "v_oy", "distance", "height", "time", "angle"]

def interpret(question, params, angleInWholeProblem, velocityInWholeProblem):
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
                v_o = Util.getNumber(words[wordIndex:])
            if(word == "height" or word == "from"):
                h = Util.getNumber(words[wordIndex:])
            if(word == "second" or word == "seconds"):
                try:
                    time = float(words[wordIndex-1])
                except:
                    num = -1
            if(word == "degree" or word == "degrees"):
                theta = float(words[wordIndex-1])
            if(word == "distance" or word == "travels"):
                distance = Util.getNumber(words[wordIndex:])
                
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

    if(theta != None and v_o != None):
        v_ox = v_o * math.cos(math.radians(theta))
        v_oy = v_o * math.sin(math.radians(theta))
    elif(not angleInWholeProblem):
        v_oy = v_o
        distance = 0
        v_ox = 0

    if(v_o == None and "velocity" not in solveFor and not velocityInWholeProblem):
        v_o = 0
        v_ox = 0
        v_oy = 0

    data = [v_o, v_ox, v_oy, distance, h, time, theta]
    
    #print(data)

    solveAll(data, solveFor)

def manualInput():
    data = []
    solveFor = []
    print("Please input all data in SI units. For any unknown values, type ? if you're looking to calculate that value, or - if it does not need to be solved for")
    for index, element in enumerate(variables):
        response = input("Value of " + str(element) + "?")
        try:
            data.append(float((response).split(" ")[0]))
        except:
            data.append(None)
            if("?" in response):
                solveFor.append(element)

    if("v_o" in x for x in solveFor):
        solveFor.append("velocity")

    solveAll(data, solveFor)
            

def solveAll(data, solveFor):
    for solveMe in solveFor:
        out = solve(data, solveMe)
        if(out != None):
            Util.formatOutput(out)

def solve(data, solveFor):

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
        if(v_o == None and distance != None and h != None):
            top = -9.8 * distance**2
            bottom = 2 * (h - distance * math.tan(math.radians(theta))) * (math.cos(math.radians(theta)))**2
            v_o = (top/bottom)**0.5
        if(h == None and v_oy != None and time != None):
            h = -1.0 * v_oy * time + .5*9.8*time**2.0
        if(time == None and v_oy != None and h != None):
            time = (1.0*v_oy + (v_oy**2 + 2*9.8*h)**0.5)/9.8
        if(distance == None and v_oy != None and h != None and v_ox != None):
            distance = (1.0*v_oy + (v_oy**2 + 2*9.8*h)**0.5)/9.8 * v_ox
        if(theta == None and v_ox != None and v_oy != None and "angle" in solveFor):
            theta = math.degrees(math.atan(v_oy/v_ox))
        if(theta != None and v_o != None and (v_ox == None or v_oy == None)):
            v_ox = v_o * math.cos(math.radians(theta))
            v_oy = v_o * math.sin(math.radians(theta))
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
            







