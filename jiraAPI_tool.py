from crewai.tools import BaseTool
from typing import Optional
from jira import JIRA
import os

class JiraAPITool(BaseTool):
    """Tool for interacting with Jira API"""
    
    name: str = "JiraAPITool"
    description: str = "Tool for fetching and interacting with Jira issues"
    
    def __init__(self):
        super().__init__()
        # Initialize Jira client
        print(os.environ.get('JIRA_SERVER'))
        self.jira = JIRA(
            server=os.environ.get('JIRA_SERVER'),
            basic_auth=(os.environ.get('JIRA_USERNAME'), os.environ.get('JIRA_API_TOKEN'))
        )
    
    def _run(self, query: str) -> str:
        """Run the Jira API tool with the given query"""
        try:
            # Parse the query and extract parameters
            # This is a simple example that assumes the query is a JQL query
            issues = self.jira.search_issues(query, maxResults=100)
            
            # Format the results as a list of dictionaries
            results = []
            for issue in issues:
                results.append({
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'status': issue.fields.status.name,
                    'priority': issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'Unassigned',
                    'assignee': issue.fields.assignee.displayName if hasattr(issue.fields, 'assignee') and issue.fields.assignee else 'Unassigned',
                    'created': issue.fields.created,
                    'updated': issue.fields.updated
                })
            
            return results
        except Exception as e:
            return f"Error accessing Jira API: {str(e)}"