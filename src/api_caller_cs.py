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
    
    def updateIssue(self, issue, field_id, value ):
        issue = self.jira.issue(issue)        
        fieldStr={field_id:value}        
        issue.update(fields=fieldStr)
        
    def getValue(self, issue, field_id):
        issue = self.jira.issue(issue)
        customFieldValue = self.jira.fields.field_id.value
        return customFieldValue
        
