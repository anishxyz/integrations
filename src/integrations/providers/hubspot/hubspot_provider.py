"""HubSpot provider implementation."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx


from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    CreateCompany,
    CreateContact,
    CreateCosBlogPost,
    CreateCustomObject,
    CreateDeal,
    CreateEngagement,
    CreateFormSubmission,
    CreateLineItem,
    CreateOrUpdateContact,
    CreateProduct,
    FindCompany,
    FindContact,
    FindCustomObject,
    FindDeal,
    FindOrCreateCompany,
    FindOrCreateContact,
    FindOrCreateCustomObject,
    FindOrCreateDeal,
    FindOrCreateLineItem,
    GetCompany,
    GetContact,
    GetCustomObject,
    GetDeal,
    GetFilePublicUrl,
    GetOwnerByEmail,
    GetOwnerById,
    GetProduct,
    RemoveAssociations,
    RemoveEmailSubscription,
    UpdateCompany,
    UpdateContact,
    UpdateCustomObject,
    UpdateDeal,
    UpdateProduct,
    UploadFile,
)
from .hubspot_settings import HubspotSettings


class HubspotProvider(HttpxClientMixin, BaseProvider[HubspotSettings]):
    """Provider exposing HubSpot CRM and CMS operations."""

    settings_class = HubspotSettings

    create_contact: CreateContact
    update_contact: UpdateContact
    create_or_update_contact: CreateOrUpdateContact
    get_contact: GetContact
    find_contact: FindContact
    find_or_create_contact: FindOrCreateContact

    create_company: CreateCompany
    update_company: UpdateCompany
    get_company: GetCompany
    find_company: FindCompany
    find_or_create_company: FindOrCreateCompany

    create_deal: CreateDeal
    update_deal: UpdateDeal
    get_deal: GetDeal
    find_deal: FindDeal
    find_or_create_deal: FindOrCreateDeal

    create_custom_object: CreateCustomObject
    update_custom_object: UpdateCustomObject
    get_custom_object: GetCustomObject
    find_custom_object: FindCustomObject
    find_or_create_custom_object: FindOrCreateCustomObject

    create_line_item: CreateLineItem
    find_or_create_line_item: FindOrCreateLineItem

    create_engagement: CreateEngagement
    remove_associations: RemoveAssociations
    upload_file: UploadFile
    create_form_submission: CreateFormSubmission
    remove_email_subscription: RemoveEmailSubscription
    create_cos_blog_post: CreateCosBlogPost
    create_product: CreateProduct
    update_product: UpdateProduct
    get_product: GetProduct
    get_file_public_url: GetFilePublicUrl
    get_owner_by_email: GetOwnerByEmail
    get_owner_by_id: GetOwnerById
    raw_request: RawHttpRequestAction

    create_contact = action(
        CreateContact,
        description="Create a HubSpot contact.",
    )
    update_contact = action(
        UpdateContact,
        description="Update a HubSpot contact.",
    )
    create_or_update_contact = action(
        CreateOrUpdateContact,
        description="Create or update a contact using a unique identifier.",
    )
    get_contact = action(
        GetContact,
        description="Retrieve a HubSpot contact by ID.",
    )
    find_contact = action(
        FindContact,
        description="Search HubSpot contacts.",
    )
    find_or_create_contact = action(
        FindOrCreateContact,
        description="Find a contact or create it if missing.",
    )

    create_company = action(
        CreateCompany,
        description="Create a HubSpot company.",
    )
    update_company = action(
        UpdateCompany,
        description="Update a HubSpot company.",
    )
    get_company = action(
        GetCompany,
        description="Retrieve a HubSpot company by ID.",
    )
    find_company = action(
        FindCompany,
        description="Search HubSpot companies.",
    )
    find_or_create_company = action(
        FindOrCreateCompany,
        description="Find a company or create it if missing.",
    )

    create_deal = action(
        CreateDeal,
        description="Create a HubSpot deal.",
    )
    update_deal = action(
        UpdateDeal,
        description="Update a HubSpot deal.",
    )
    get_deal = action(
        GetDeal,
        description="Retrieve a HubSpot deal by ID.",
    )
    find_deal = action(
        FindDeal,
        description="Search HubSpot deals.",
    )
    find_or_create_deal = action(
        FindOrCreateDeal,
        description="Find a deal or create it if missing.",
    )

    create_custom_object = action(
        CreateCustomObject,
        description="Create a HubSpot custom object.",
    )
    update_custom_object = action(
        UpdateCustomObject,
        description="Update a HubSpot custom object.",
    )
    get_custom_object = action(
        GetCustomObject,
        description="Retrieve a HubSpot custom object.",
    )
    find_custom_object = action(
        FindCustomObject,
        description="Search HubSpot custom objects.",
    )
    find_or_create_custom_object = action(
        FindOrCreateCustomObject,
        description="Find a custom object or create it if missing.",
    )

    create_line_item = action(
        CreateLineItem,
        description="Create a HubSpot line item.",
    )
    find_or_create_line_item = action(
        FindOrCreateLineItem,
        description="Find a line item or create it if missing.",
    )

    create_engagement = action(
        CreateEngagement,
        description="Create a HubSpot engagement.",
    )
    remove_associations = action(
        RemoveAssociations,
        description="Remove associations between CRM records.",
    )
    upload_file = action(
        UploadFile,
        description="Upload a file to HubSpot.",
    )
    create_form_submission = action(
        CreateFormSubmission,
        description="Submit a HubSpot form.",
    )
    remove_email_subscription = action(
        RemoveEmailSubscription,
        description="Unsubscribe an email address.",
    )
    create_cos_blog_post = action(
        CreateCosBlogPost,
        description="Create a HubSpot CMS blog post.",
    )
    create_product = action(
        CreateProduct,
        description="Create a HubSpot product.",
    )
    update_product = action(
        UpdateProduct,
        description="Update a HubSpot product.",
    )
    get_product = action(
        GetProduct,
        description="Retrieve a HubSpot product by ID.",
    )
    get_file_public_url = action(
        GetFilePublicUrl,
        description="Get the public URL for a HubSpot file.",
    )
    get_owner_by_email = action(
        GetOwnerByEmail,
        description="Retrieve a HubSpot owner by email.",
    )
    get_owner_by_id = action(
        GetOwnerById,
        description="Retrieve a HubSpot owner by ID.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Send a raw HubSpot API request (beta).",
    )

    def process_httpx_response(self, response: httpx.Response) -> Any:
        def fallback(resp: httpx.Response) -> dict[str, str]:
            return {"value": resp.text}

        payload = self.parse_httpx_response(
            response,
            require_json=True,
            empty_value={},
            fallback=fallback,
        )
        payload = self.postprocess_httpx_payload(payload)
        if payload is None:
            return None
        if isinstance(payload, Mapping):
            error = payload.get("error")
            if isinstance(error, Mapping):
                message = error.get("message", "HubSpot API error")
                raise ValueError(message)
            return dict(payload)
        return {"value": payload}

    def httpx_headers(self) -> Mapping[str, str]:
        headers: dict[str, str] = {}
        token = self.settings.access_token
        if not token:
            raise ValueError("Hubspot token is required")
        headers["Authorization"] = f"Bearer {token}"
        user_agent = self.settings.user_agent
        if user_agent:
            headers["User-Agent"] = user_agent
        return headers
