import configparser
from status_util import *
from api_caller_cs import API_Caller
import pickle
import sys,os

ruleSection = 'Nissan_CCS2_to_CCS2Ext'

config = configparser.ConfigParser()
config.read('src\RuleBook.ini')

Source_Jira_url = config.get(ruleSection, 'Source_Jira_url')
Source_user = config.get(ruleSection, 'Source_user')
Source_api_key = config.get(ruleSection, 'Source_api_key')

Source_Updated = config.get(ruleSection, 'Source_Updated')
Source_JQL_Filter = config.get(ruleSection, 'Source_JQL_Filter')+' AND '+ 'updated >= -' + Source_Updated
#PROJECT=DUM AND (status in (Submitted) AND status was 'Issue To Be Documented') AND updated >= -24h
Destination_Jira_url = config.get(ruleSection, 'Destination_Jira_url')
Destination_user =config.get(ruleSection, 'Destination_user')
Destination_api_key = config.get(ruleSection, 'Destination_api_key')
Destination_project_key=config.get(ruleSection, 'Destination_project_key')
Destination_issue_type=config.get(ruleSection, 'Destination_issue_type')

Field_Mapping = config.get(ruleSection, 'Field_Mapping')

def setStatusTriggers(ruleBookSection):
    statAsStr = config.get(ruleBookSection,'StatusTrigger')
    tempStatList = statAsStr.split(',')
    for eSts in tempStatList:
        statusTriggerList.append(eSts.strip())
         
######################################################

src_API_caller = API_Caller(Source_Jira_url,Source_user,Source_api_key)
dest_API_caller = API_Caller(Destination_Jira_url,Destination_user,Destination_api_key)

#to Delete all issues
for iss in dest_API_caller.searchJiraIssues('PROJECT=DUMR'):
    dest_API_caller.delete_issue(iss)

statusTriggerList = []
setStatusTriggers(ruleSection)
for statusTrigger in statusTriggerList:  
    
    prevStatusList = getPossiblePrevStats(statusTrigger,ruleSection)
    #print(prevStatusList)
    for prevStatus in prevStatusList:
        query = Source_JQL_Filter + " AND (status in ('" + statusTrigger + "') AND status WAS in ('" + prevStatus + "'))"
        print(query)        
        src_issueList = src_API_caller.searchJiraIssues(query)
        
        for src_issue in src_issueList:
            targetStatus = getChangeToStatus(statusTrigger,prevStatus,ruleSection)   
            if(targetStatus.startswith('$CreateNew')):    
                tracking_field = targetStatus.split('@')[1].strip()               
                
                if (not src_API_caller.get_value_from_custom_field(src_issue, tracking_field)): #check if tracking id is not present
                    
                    fields=generate_fields_for_new_issue(src_API_caller, dest_API_caller, src_issue, Destination_project_key, Destination_issue_type, Field_Mapping)                
                    
                    print('Creating new ticket in target.....')
                    target_Issue = dest_API_caller.createIssue(fields)
                    tar_issue_key=str(target_Issue)
                    print('Issue created in target JIRA. ID: ', tar_issue_key)
                    src_API_caller.set_value_to_custom_field(src_issue, tracking_field, tar_issue_key)
                   
                    attachment_detail_list = src_API_caller.get_all_attchment_details(src_issue)
                    all_attachments = src_API_caller.get_all_attachments(attachment_detail_list)
                    print(attachment_detail_list)
                    print(all_attachments)
                    
                    def save_object(obj, filename):
                        
                        current_directory = os.getcwd()
                        final_directory = os.path.join(current_directory, r'src\\tempAttach')
                        if not os.path.exists(final_directory):
                            os.makedirs(final_directory)
                        
                        filename=final_directory+'\\' + filename
                        print('####')
                        #print(filename)
                        
                        with open(filename, 'wb') as outp:  # Overwrites any existing file.
                            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
                                
                    for attachment in all_attachments:
                        a = attachment.get()
                        file_name = 'sam.txt'
                        save_object(a, file_name)
                        
                        current_directory = os.getcwd()
                        final_directory = os.path.join(current_directory, r'src\\tempAttach')
                        file_name=final_directory+'\\' + file_name
                        print(file_name)
                        dest_API_caller.add_attachment(target_Issue, file_name)
