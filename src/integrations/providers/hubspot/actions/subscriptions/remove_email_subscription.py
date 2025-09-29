"""Remove a HubSpot email subscription."""

from __future__ import annotations

from typing import Any, Mapping

from .....core.actions import BaseAction


class RemoveEmailSubscription(BaseAction):
    """Unsubscribe an email address from marketing communications."""

    async def __call__(
        self,
        email: str,
        *,
        legal_basis: str | None = None,
        legal_basis_explanation: str | None = None,
        subscription_details: Mapping[str, Any] | None = None,
    ) -> Any:
        payload: dict[str, Any] = {"emailAddress": email}
        if legal_basis:
            payload["legalBasis"] = legal_basis
        if legal_basis_explanation:
            payload["legalBasisExplanation"] = legal_basis_explanation
        if subscription_details:
            payload.update(dict(subscription_details))
        response = await self.provider.request(
            "PUT",
            f"/communication-preferences/v3/status/email/{email}/unsubscribe",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
