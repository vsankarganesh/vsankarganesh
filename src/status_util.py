import configparser
import pickle

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

def generate_fields_for_new_issue(srcAPICaller, dest_API_caller, issue, Destination_project_key, Destination_issue_type, field_mapping):
    
    fields={
        'project': {'key': Destination_project_key},
        'issuetype': {
            "name": Destination_issue_type
        },
        #'summary': issue.fields.summary,
    }
    fieldMapLst = field_mapping.split('|')
    
    for fieldMap in fieldMapLst:
        fieldStr = fieldMap.split(':')
        src_field = fieldStr[0].strip()     
        dest_field = fieldStr[1].strip()
        
        try:
            fields[dest_field] = getattr(issue.fields, src_field)
        except:
            #print('###    Exception while trying to add ', src_field)            
            src_field_id=srcAPICaller.get_custom_field_id(src_field)
            destn_field_id=dest_API_caller.get_custom_field_id(dest_field)
            #print('Trying with ID. id is : ', destn_field_id + '  ' + getattr(issue.fields, src_field_id))
            fields[destn_field_id] = getattr(issue.fields, src_field_id)
    print('-----Printing Generated Fields for creating issue-----')
    print(fields)
    return fields


