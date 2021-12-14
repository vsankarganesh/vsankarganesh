import configparser

config = configparser.ConfigParser()
config.read('src/RuleBook.ini')
    
def getChangeToStatus(currStatus, prevStatus, ruleBookSection):    
    rule = config.get(ruleBookSection,currStatus)
    changeToStatus = None
    prevStatList = rule.split('|')        
    for prevStatCm in prevStatList:
                prvSt = prevStatCm.split(':')
                if prvSt[0].strip().lower() == prevStatus.lower():
                    changeToStatus = prvSt[1].strip()
    return changeToStatus 

def getPossiblePrevStats(currStatus, ruleBookSection): 
    prevStatusList = []
    ruleStmnt = config.get(ruleBookSection,currStatus)   
    ruleList = ruleStmnt.split('|')
    for eRule in ruleList:
        pvStL = eRule.split(':')
        prevStatusList.append(pvStL[0].strip())
    return prevStatusList
