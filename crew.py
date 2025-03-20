from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool
from jira import JIRA
import os

class JiraAPITool(BaseTool):
    """Tool for interacting with Jira API"""
    
    name: str = "JiraAPITool"
    description: str = "Tool for fetching and interacting with Jira issues"
    
    def __init__(self):
        super().__init__()
        # Initialize Jira client using environment variables
        self.jira = JIRA(
            server=os.environ.get('JIRA_SERVER'),
            basic_auth=(os.environ.get('JIRA_USERNAME'), os.environ.get('JIRA_API_TOKEN'))
        )
    
    def _run(self, query: str) -> str:
        """Run the Jira API tool with the given query"""
        try:
            # Assume the query is a JQL query
            issues = self.jira.search_issues(query, maxResults=100)
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

@CrewBase
class JiraManagementCrew:
    """Jira Management crew for handling Jira-related tasks"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def jira_issue_fetcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_issue_fetcher_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @agent
    def jira_issue_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_issue_analyzer_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @agent
    def jira_dependency_tracker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_dependency_tracker_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @agent
    def jira_task_auto_assigner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_task_auto_assigner_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @agent
    def jira_issue_escalator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_issue_escalator_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @agent
    def jira_backlog_refiner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_backlog_refiner_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @agent
    def jira_sprint_optimizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_sprint_optimizer_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @agent
    def jira_report_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["jira_report_generator_agent"],
            verbose=True,
            model="gpt 4o mini",
        )

    @task
    def fetch_jira_issues_task(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_jira_issues_task"],
            agent=self.jira_issue_fetcher_agent(),
            tool=JiraAPITool()  # Integrates the custom Jira API tool
        )

    @task
    def analyze_jira_issues_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_jira_issues_task"],
            agent=self.jira_issue_analyzer_agent(),
        )

    @task
    def identify_jira_dependencies_task(self) -> Task:
        return Task(
            config=self.tasks_config["identify_jira_dependencies_task"],
            agent=self.jira_dependency_tracker_agent(),
        )

    @task
    def assign_jira_issues_task(self) -> Task:
        return Task(
            config=self.tasks_config["assign_jira_issues_task"],
            agent=self.jira_task_auto_assigner_agent(),
        )

    @task
    def escalate_jira_issues_task(self) -> Task:
        return Task(
            config=self.tasks_config["escalate_jira_issues_task"],
            agent=self.jira_issue_escalator_agent(),
        )

    @task
    def refine_jira_backlog_task(self) -> Task:
        return Task(
            config=self.tasks_config["refine_jira_backlog_task"],
            agent=self.jira_backlog_refiner_agent(),
        )

    @task
    def optimize_jira_sprint_task(self) -> Task:
        return Task(
            config=self.tasks_config["optimize_jira_sprint_task"],
            agent=self.jira_sprint_optimizer_agent(),
        )

    @task
    def generate_jira_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_jira_report_task"],
            output_file="jira_report.md",
            agent=self.jira_report_generator_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Jira Management crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
