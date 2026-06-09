#!/usr/bin/env python
import sys
import warnings

from verified_code_review.crew import VerifiedCodeReviewCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file runs the crew locally. Replace the inputs below with the change you
# want reviewed — `repo`, `pr`, and `code` are interpolated into the agents and tasks.

# A tiny example change with an obvious bug, so the reviewer has something to find.
EXAMPLE_CODE = '''\
def add(a, b):
    # Adds two numbers and returns the sum.
    return a - b
'''


def run():
    """Run the crew."""
    inputs = {
        'repo': 'acme/backend',
        'pr': '142',
        'code': EXAMPLE_CODE,
    }
    try:
        VerifiedCodeReviewCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """Train the crew for a given number of iterations."""
    inputs = {
        'repo': 'acme/backend',
        'pr': '142',
        'code': EXAMPLE_CODE,
    }
    try:
        VerifiedCodeReviewCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """Replay the crew execution from a specific task."""
    try:
        VerifiedCodeReviewCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """Test the crew execution and return the results."""
    inputs = {
        'repo': 'acme/backend',
        'pr': '142',
        'code': EXAMPLE_CODE,
    }
    try:
        VerifiedCodeReviewCrew().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
