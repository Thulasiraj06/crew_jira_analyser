#!/usr/bin/env python
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crew import JiraManagementCrew

def run():
    """
    Run the crew.
    """
    inputs = {"user_query": "Find and analyze critical bugs in the authentication module"}
    JiraManagementCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"user_query": "Find and analyze critical bugs in the authentication module"}
    try:
        JiraManagementCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        JiraManagementCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"user_query": "Find and analyze critical bugs in the authentication module"}
    try:
        JiraManagementCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        run()
    elif sys.argv[1] == "train" and len(sys.argv) >= 4:
        train()
    elif sys.argv[1] == "replay" and len(sys.argv) >= 3:
        replay()
    elif sys.argv[1] == "test" and len(sys.argv) >= 4:
        test()
    else:
        print("Invalid command or missing arguments.")
        print("Usage:")
        print("  python main.py                             # Run the crew")
        print("  python main.py train <iterations> <file>   # Train the crew")
        print("  python main.py replay <task_id>            # Replay from a task")
        print("  python main.py test <iterations> <model>   # Test the crew")