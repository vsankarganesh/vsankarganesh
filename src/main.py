import configparser
import jira
from status_util import getChangeToStatus, getPossiblePrevStats
from api_caller_cs import API_Caller

ruleSection = 'Nissan_CCS2_to_CCS2Ext'

config = configparser.ConfigParser()
config.read('src\RuleBook.ini')

Source_Jira_url=config.get(ruleSection, 'Source_Jira_url')
Source_user = config.get(ruleSection, 'Source_user')
Source_api_key = config.get(ruleSection, 'Source_api_key')

Source_Updated = config.get(ruleSection, 'Source_Updated')
Source_JQL_Filter = config.get(ruleSection, 'Source_JQL_Filter')+' AND '+ 'updated >= -' + Source_Updated

Destination_Jira_url = config.get(ruleSection, 'Destination_Jira_url')
Destination_user =config.get(ruleSection, 'Destination_user')
Destination_api_key = config.get(ruleSection, 'Destination_api_key')
Destination_project_key=config.get(ruleSection, 'Destination_project_key')

def setStatusTriggers(ruleBookSection):
    statAsStr = config.get(ruleBookSection,'StatusTrigger')
    tempStatList = statAsStr.split(',')
    for eSts in tempStatList:
         statusTriggerList.append(eSts.strip())
         
######################################################

src_API_caller = API_Caller(Source_Jira_url,Source_user,Source_api_key)
dest_API_caller = API_Caller(Destination_Jira_url,Destination_user,Destination_api_key)

statusTriggerList = []

setStatusTriggers(ruleSection)

for statusTrigger in statusTriggerList:  
    
    prevStatusList = getPossiblePrevStats(statusTrigger,ruleSection)
    #print(prevStatusList)
    for prevStatus in prevStatusList:
        query = Source_JQL_Filter + " AND (status in ('" + statusTrigger + "') AND status WAS in ('" + prevStatus + "'))"
        print(query)        
        rs = src_API_caller.searchJiraIssues(query)
        
        for issue in rs:
            #print ('ticket-no=', issue)
            # print ('IssueType=',issue.fields.issuetype.name)
            # print ('Status=',issue.fields.status.name)
            # print ('Summary=',issue.fields.summary)
            targetStatus = getChangeToStatus(statusTrigger,prevStatus,ruleSection)   
            
            if(targetStatus.startswith('@CreateNew')):    #check if value is already there
                
                print('Creating new ticket in target')
                fields={
                'project': {'key': Destination_project_key},
                'issuetype': {
                    "name": "Bug"
                },
                'summary': issue.fields.summary,
                }
                targetIssue = dest_API_caller.createIssue(fields)                
                issue_key=str(targetIssue)        
                src_API_caller.updateIssue(issue, 'customfield_11305', issue_key)
