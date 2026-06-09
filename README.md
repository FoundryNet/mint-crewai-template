# Verified Code Review Crew

A [CrewAI](https://crewai.com) crew that **reviews a code change and then proves the
work was done** — by anchoring a tamper-evident, on-chain attestation of the completed
review on [MINT Protocol](https://github.com/FoundryNet/mint-mcp) (Solana).

Most code-review automations produce a review and then forget it. This crew produces a
review *and a verifiable receipt*: a permanent, portable record that this agent did this
work, which anyone — a human, another agent, a CI gate — can independently verify.

## What it does

Two agents run in sequence:

1. **Senior Code Reviewer** — reviews the supplied change for correctness, security,
   readability, and test coverage, and returns a markdown review ending in a verdict
   (`APPROVE` / `APPROVE_WITH_COMMENTS` / `REQUEST_CHANGES`).
2. **Work Attestation Clerk** — takes the finished review and calls the **`mint_attest`**
   tool (from the [`mint-attest`](https://pypi.org/project/mint-attest/) SDK) to anchor it
   on MINT as a `code_review` work record, then returns the `attestation_id` and a public
   verify URL. The receipt is written to `review_receipt.md`.

```
code change ──▶ Code Reviewer ──▶ review + verdict ──▶ Attestation Clerk ──▶ on-chain receipt
```

## Example use cases

- Gate a merge on a *verifiable* AI review, not just a comment that can be edited away.
- Build a portable track record for a review agent so other agents can `mint_verify` it
  before trusting its output.
- Produce an auditable, tamper-evident log of every automated review for compliance.

## Setup

Requires Python `>=3.10,<3.13`.

```bash
# 1. Install dependencies (this also installs mint-attest)
pip install mint-attest      # the MINT SDK + the mint_attest CrewAI tool
crewai install               # installs this crew's dependencies from pyproject.toml

# 2. Configure secrets
cp .env.example .env
#   then edit .env and set:
#     MINT_API_KEY   — your MINT key (free at https://foundrynet.io/signup)
#     OPENAI_API_KEY — or any other LiteLLM-supported model key
```

> Without `MINT_API_KEY`, the review still runs — the attestation step simply reports
> that it was skipped, rather than failing the crew.

## Run

```bash
crewai run
```

Out of the box this reviews a tiny example change (an `add()` function that subtracts) so
you can see the full flow end to end. The review is printed, and the attestation receipt
is written to `review_receipt.md`.

To review your own change, edit the `inputs` in
[`src/verified_code_review/main.py`](src/verified_code_review/main.py):

```python
inputs = {
    'repo': 'your-org/your-repo',
    'pr': '123',
    'code': '<the diff or code snippet to review>',
}
```

### Example output (receipt)

```
Attested on MINT. attestation_id=att_9f3c… verify=https://explorer.solana.com/tx/…
```

Browse live identities, attestations, and trust scores in the
[MINT Explorer](https://mint-explorer.vercel.app).

## How the MINT tool is wired

The attestation agent is given `MintAttestTool` in
[`src/verified_code_review/crew.py`](src/verified_code_review/crew.py):

```python
from mint_attest.crewai import MintAttestTool

@agent
def review_attestor(self) -> Agent:
    return Agent(
        config=self.agents_config['review_attestor'],
        tools=[MintAttestTool(name="verified-code-review-crew",
                              default_work_type="code_review")],
        verbose=True,
    )
```

`MintAttestTool` reads `MINT_API_KEY` from the environment, so no key handling lives in
the crew. Prefer fully-automatic attestation of every step? The SDK also ships
`mint_attest_step_callback` for use as `Crew(step_callback=…)`.

## Resources

- **MINT Protocol** — https://github.com/FoundryNet/mint-mcp
- **mint-attest SDK** — https://pypi.org/project/mint-attest/
- **MINT Explorer** — https://mint-explorer.vercel.app
- **CrewAI docs** — https://docs.crewai.com

## License

MIT © FoundryNet
