from typing import Any, Dict, Optional
from jira import JIRA

class API_Caller:
    
    def __init__(self, url, user, api_key) -> None:
        self.url=url+'rest/api/2/'
        self.jira_url=url 
        self.user=user
        self.api_key=api_key        
        self.jira = JIRA(server=self.jira_url, basic_auth=(self.user, self.api_key))
    
    def get_user(self):
        return self.user    
        
    def searchJiraIssues(self, query):       
        issues = []
        i = 0
        chunk_size = 100
        while True:
            chunk = self.jira.search_issues(query, startAt=i, maxResults=chunk_size)
            i += chunk_size
            issues += chunk.iterable
            if i >= chunk.total:
                break
        return issues
    
    def createIssue(self, fields):   
        return self.jira.create_issue(fields)
    
    def delete_issue(self, issue):
        issue=self.jira.issue(issue)
        issue.delete()
    
    def updateIssue(self, issue, field_id, value):
        issue = self.jira.issue(issue)        
        fieldStr={field_id:value}        
        issue.update(fields=fieldStr)
                
    def get_all_fields(self):
        # Fetch all fields
        allfields=self.jira.fields()
        return allfields
                              
    def get_value_from_custom_field(self, issue, custom_field):
        # Fetch all fields
        allfields=self.jira.fields()
        # Make a map from field name -> field id
        nameMap = {field['name']:field['id'] for field in allfields}
        # Now look up custom fields by name using the map
        return getattr(issue.fields, nameMap[custom_field])
    
    def get_custom_field_id(self, custom_field):
        # Fetch all fields
        allfields=self.jira.fields()
        # Make a map from field name -> field id
        nameMap = {field['name']:field['id'] for field in allfields}
        return nameMap[custom_field]
    
    def set_value_to_custom_field(self, issue, custom_field, value):
        cust_field_id = self.get_custom_field_id(custom_field)
        self.updateIssue(issue, cust_field_id, value)
    
    def get_all_attchment_details(self, issue):
        issue_key = self.jira.issue(issue.key)
        attachment_details_list = issue_key.fields.attachment
        #print (attachment_details_list)
        return attachment_details_list
    
    def get_all_attachments(self, all_attachment_details):
        attachments = []
        for attachment in all_attachment_details:
            id= getattr(attachment, 'id')
            filename= getattr(attachment, 'filename')  
            attachments.append(self.jira.attachment(id))
        return attachments
    
    def add_attachment(self, issue, attachment):
        self.jira.add_attachment(issue, attachment)
        #self.jira.add_attachment(issue=issue, attachment=path_to_attachment)
