from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# The MINT attestation tool ships with the mint-attest SDK. Giving it to an agent
# lets the crew anchor a tamper-evident, on-chain record of its work on MINT Protocol.
# Docs: https://github.com/FoundryNet/mint-mcp  ·  pip install mint-attest
from verified_code_review.tools.mint_tool import make_mint_attest_tool


@CrewBase
class VerifiedCodeReviewCrew():
    """Reviews a code change, then anchors a tamper-evident attestation of the
    completed review on MINT Protocol (Solana)."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reviewer'],
            verbose=True,
        )

    @agent
    def review_attestor(self) -> Agent:
        # MintAttestTool reads MINT_API_KEY from the environment. `name` becomes the
        # crew's MINT actor identity; `default_work_type` is used if the agent omits one.
        return Agent(
            config=self.agents_config['review_attestor'],
            tools=[make_mint_attest_tool(name="verified-code-review-crew",
                                         work_type="code_review")],
            verbose=True,
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
        )

    @task
    def attest_task(self) -> Task:
        return Task(
            config=self.tasks_config['attest_task'],
            output_file='review_receipt.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Verified Code Review crew."""
        return Crew(
            agents=self.agents,   # created by the @agent decorators
            tasks=self.tasks,     # created by the @task decorators, run in order
            process=Process.sequential,
            verbose=True,
        )
