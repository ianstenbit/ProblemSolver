import Text

def formatOutput(result):
    output = ""
    for index, res in enumerate(result):
        if(index%2 == 0):
            output += str(res)[:5] + result[index+1] + ","
    output = output[:-1]
    print(output)
    Text.sendText(output)

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
