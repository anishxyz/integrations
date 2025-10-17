"""Public API import surface tests."""

from __future__ import annotations


def test_root_level_exports() -> None:
    import integrations
    import integrations.core as core

    assert integrations.Integrations is core.Integrations
    assert integrations.BaseProvider is core.BaseProvider
    assert integrations.ProviderSettings is core.ProviderSettings
    assert integrations.BaseAction is core.BaseAction
    assert integrations.HttpxClientMixin is core.HttpxClientMixin
    assert integrations.ProviderIdentifier is core.ProviderIdentifier
    assert integrations.ProviderKey is core.ProviderKey
    assert integrations.action is core.action
    assert integrations.available_providers is core.available_providers
    assert integrations.get_provider is core.get_provider
    assert integrations.provider_key is core.provider_key
    assert integrations.provider_override is core.provider_override
    assert integrations.register_provider is core.register_provider


def test_providers_module_exports() -> None:
    from integrations import providers
    from integrations.providers import gmail, github, notion, slack
    import integrations.core as core

    assert providers.GithubProvider is github.GithubProvider
    assert providers.GithubSettings is github.GithubSettings
    assert providers.GmailProvider is gmail.GmailProvider
    assert providers.GmailSettings is gmail.GmailSettings
    assert providers.NotionProvider is notion.NotionProvider
    assert providers.NotionSettings is notion.NotionSettings
    assert providers.SlackProvider is slack.SlackProvider
    assert providers.SlackSettings is slack.SlackSettings
    assert providers.BaseProvider is core.BaseProvider
    assert providers.ProviderSettings is core.ProviderSettings
    assert providers.HttpxClientMixin is core.HttpxClientMixin
    assert providers.available_providers is core.available_providers
    assert providers.get_provider is core.get_provider
    assert providers.register_provider is core.register_provider
