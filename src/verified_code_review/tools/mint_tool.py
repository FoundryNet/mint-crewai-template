"""MINT attestation tool wiring for the crew.

`MintAttestTool` ships in the `mint-attest` SDK (`mint_attest.crewai`). On CrewAI 1.x,
`BaseTool` auto-generates a pydantic args schema from the tool's `_run` signature, but
the SDK's `_run` uses string annotations (`from __future__ import annotations`), which
CrewAI 1.x can't resolve on its own. We give the tool an explicit `args_schema` so it
works across CrewAI versions. (No behavior change — these are exactly the args the
agent already passes.)
"""
from __future__ import annotations

from typing import Optional, Type

from pydantic import BaseModel, Field

from mint_attest.crewai import MintAttestTool


class MintAttestInput(BaseModel):
    """Arguments the agent passes when it attests a completed unit of work."""
    summary: str = Field(..., description="One line: what you did and the result.")
    work_type: Optional[str] = Field(
        default="code_review",
        description="One of: research | analysis | generation | code_review | delivery | custom",
    )


def make_mint_attest_tool(name: str = "verified-code-review-crew",
                          work_type: str = "code_review") -> MintAttestTool:
    """Build a MintAttestTool with an explicit schema. Reads MINT_API_KEY from env."""
    return MintAttestTool(
        name=name,
        default_work_type=work_type,
        args_schema=MintAttestInput,
    )
