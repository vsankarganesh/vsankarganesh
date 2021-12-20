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

    def get_issue(self, issue_key):
        return self.jira.issue(issue_key)
    
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
    
    def get_all_attchments(self, issue):
        issue_key = self.jira.issue(issue.key)
        attachment_details_list = issue_key.fields.attachment       
        return attachment_details_list
    
    def add_attachment(self, issue, attachment):
        self.jira.add_attachment(issue, attachment)        
        
    def add_attachment(self, issue, attachment, filename):
        self.jira.add_attachment(issue=issue, attachment=attachment, filename=filename)
        
    def sync_all_attachments(self, dest_API_caller, src_issue, dest_issue):
        from io import BytesIO
        attachment_list = self.get_all_attchments(src_issue)
                                 
        for attachment in attachment_list:
            file_name = attachment.filename
            atmt = attachment.get()
            attachment_as_byte = BytesIO()
            attachment_as_byte.write(atmt)
            
            # checking if destination issue already have an attachment with same filename 
            dest_attachment_list = dest_API_caller.get_all_attchments(dest_issue)
            has_same_attachment = False            
            for dest_attachment in dest_attachment_list:
                #print(dest_attachment)
                dest_file_name = getattr(dest_attachment, 'filename')                
                if (file_name==dest_file_name): has_same_attachment = True
            #########################################################################    
            
                
            if (not has_same_attachment):
                try:
                    dest_API_caller.add_attachment(dest_issue, attachment_as_byte, file_name)
                except Exception as e: 
                    print(e)
    ## - END OF Function - sync_all_attachments
    
    
