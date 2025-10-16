# MCPKit: Secure MCP blueprints for enterprise data

MCPKit is a blueprint for building authenticated Model Context Protocol (MCP) servers that let you bring proprietary data, content, and systems into ChatGPT, via ChatGPT Dev Mode. 

Built by MCP engineers for enterprise builders, MCPKit accelerates the path from prototype to production when native connectors or existing MCP services do not cover your use case.

## Why build a MCP Server?

- Serve high-value data directly inside ChatGPT through the connectors platform while respecting your existing authentication and entitlement rules.
- Keep sensitive content behind an authorization layer you control; MCPKit uses Auth0 as the example but supports any OIDC-compliant provider.

## Example use cases

- **Financial services:** Combine research reports, expert-call transcripts, and market indicators so portfolio teams can query entitlements-controlled insights. The synthetic bundle in this repo mirrors alternative data feeds you can adapt to production.
- **Customer support & success:** Give agents a gated knowledge base that blends CRM data, playbooks, and ticket summaries, ensuring only authorized roles can trigger refunds or policy exceptions.
- **Healthcare & life sciences:** Surface regulated documentation, SOPs, and clinical references with audit logging and patient privacy intact, ready to integrate with hospital identity providers.
- **Manufacturing & operations:** Connect maintenance logs, IoT telemetry, and supplier contracts to drive automated workflows while respecting regional access policies.

## Sample data

Use `synthetic_financial_data/` as a realistic sandbox for pipelines and demos. It contains alternative data artifacts such as analyst reports, expert-call summaries, and web-search trends with consistent tickers and timestamps. Swap in your own feeds once you are ready to plug into live systems.

## What you get in MCPKit

- **Authenticated MCP server scaffolds:** Python and TypeScript servers that implement a number of different tools, include Deep Research-compatible `search` and `fetch` tools, apply entitlement checks, and follow the recommended resource/authorization separation model.
- **Authorization patterns:** The servers also implement the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) pattern of separate resource and authorization servers. For the authorization server, we use an end-to-end Auth0 integration that you can replace with Okta, Azure AD, or an internal IdP by updating JWKS resolution, token validation, and tenant metadata.
- Sample data and data ingestion pipeline examples

## Reference implementations

- [TypeScript authenticated MCP server](typescript-authenticated-mcp-server-scaffold/README.md)
- [Python authenticated MCP server](python-authenticated-mcp-server-scaffold/README.md)

Both implementations share a consistent API surface, emit structured logs, and lean on Auth0 for token exchange. Replace Auth0 with your preferred authorization provider by updating the server configuration documented in each README.

## Develop with ChatGPT Dev Mode

- **Run locally:** Start either scaffold (`npm run dev` or `python -m server.app`) with your Auth0 application or alternate authorization server settings.
- **Expose securely via ngrok:** Tunnel the MCP server (`ngrok http <port>`) so ChatGPT can reach it during development without production deployment.
- **Register in ChatGPT Dev Mode:** Provide the tunneled URL, login with OAuth, validate queries, observe entitlement behavior, and iterate quickly.
- **Harden for production:** When you are ready, deploy your MCP server on your hosting platform of choice.
