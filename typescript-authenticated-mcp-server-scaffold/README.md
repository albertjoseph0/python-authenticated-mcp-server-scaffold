# TypeScript Authenticated MCP Server Scaffold

This project mirrors the Python authenticated MCP server, but is implemented entirely in TypeScript using the official [`@modelcontextprotocol/sdk`](https://www.npmjs.com/package/@modelcontextprotocol/sdk). It demonstrates how to:

- Protect an MCP Streamable HTTP endpoint with OAuth 2.1 / Auth0 access tokens (proxied upstream via `ProxyOAuthServerProvider`)
- Publish the `search` + `fetch` tools required by ChatGPT Deep Research, backed by an OpenAI vector store
- Publish a structured `airfare_trend_insights` tool that filters local CSV/TSV/JSON datasets

📁 Directory layout lives alongside the Python scaffold so you can compare implementations one-to-one.

---

## Prerequisites

- Node.js 20+
- An Auth0 tenant (or compatible OAuth 2.1 provider) issuing RS256 JWT access tokens
- An OpenAI API key and vector store loaded with your expert-call content
- (Optional) [`ngrok`](https://ngrok.com/) or similar tunnel for remote testing

---

## 1. Install & bootstrap

```bash
cd typescript-authenticated-mcp-server-scaffold
npm install
```

---

## 2. Configure Auth0 authentication

> The scaffold expects OAuth 2.1 bearer tokens issued by Auth0. If you prefer another IdP, keep the same environment variable shape and expose a JWKS-backed RS256 JWT.

1. **Create an API (resource server)**  
   - Auth0 Dashboard → *APIs* → *Create API*  
   - Name it (e.g., `mcp-typescript-server`)  
   - Identifier → `https://your-domain.example.com/mcp` (add this value to `JWT_AUDIENCES`)  
   - Signing Algorithm → **RS256**  
   - Enable **RBAC** and **Add Permissions in the Access Token**  
   - Add a permission named `user` (required scope)

2. **Register OAuth clients (prefer dynamic registration)**  
   - Enable Auth0’s [Dynamic Client Registration](https://auth0.com/docs/get-started/auth0-overview/register-applications/dynamic-client-registration) so MCP clients can register with Authorization Code + PKCE on demand. *(Heads-up: the MCP ecosystem is phasing out dynamic registration; treat this as a transitional aid and plan to pre-register production clients.)* The scaffold’s `/register` endpoint proxies to Auth0 and enforces `OAUTH_ALLOWED_CLIENTS`, so make sure each entry includes the callback URLs your client will request (Inspector, ChatGPT, Claude, etc.).  
   - If DCR is unavailable in your tenant, create a **Single Page Application** instead, authorize it for the API created in step 1, grant the `user` permission, and copy the **Client ID** into `OAUTH_ALLOWED_CLIENTS` alongside the allowed redirect URLs.

3. **Gather tenant metadata**  
   - Tenant domain (e.g., `https://dev-your-tenant.us.auth0.com/`) → `AUTH0_ISSUER`  
   - Expected scopes → keep the scaffold default `REQUIRED_SCOPES=openid,user` unless you renamed the permission  
   - Allowed OAuth clients → build `OAUTH_ALLOWED_CLIENTS` as `clientId|https://redirect-a,https://redirect-b;anotherClient|https://...` using the same callback URLs you configured on the Auth0 application

4. **Ensure JWT access tokens**
   - In Auth0, set a [default API audience](https://community.auth0.com/t/rfc-8707-implementation-audience-vs-resource/188990/4) **to the identifier you created in step 1** (e.g., `https://your-domain.example.com/mcp`) so Authorization Code flows return a signed JWT instead of an opaque (encrypted) token  
   - If your IdP returns opaque tokens, swap in an introspection-based verifier before running the server.

This server proxies `/authorize`, `/token`, `/register`, and `/revoke` straight to Auth0 via the SDK’s `ProxyOAuthServerProvider`. Incoming bearer tokens are validated locally with JWKS, audience, and scope checks before any MCP traffic is processed.

---

## 3. Environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Key settings:

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI API key used for vector store search/fetch |
| `VECTOR_STORE_ID` | The OpenAI vector store ID backing `search` / `fetch` |
| `AUTH0_ISSUER` | Auth0 issuer URL (`https://<tenant>.us.auth0.com/`) |
| `JWT_AUDIENCES` | Comma-separated list of audiences your access tokens must include |
| `REQUIRED_SCOPES` | Comma-separated scopes required on incoming tokens (default: `openid,user`) |
| `OAUTH_ALLOWED_CLIENTS` | Semicolon-separated entries of `clientId|https://redirect-a,https://redirect-b` for clients allowed to use the proxied Auth endpoints |
| `PORT` | HTTP port for the MCP server (default 8788) |
| `RESOURCE_SERVER_URL` | Public URL where clients reach this server (used in metadata + audience checks) |

> **Allowed clients syntax**: `OAUTH_ALLOWED_CLIENTS=inspector|http://localhost:3000/callback;chatgpt|https://chat.openai.com/auth/callback`.

---

## 4. Run the server

```bash
npm run dev
```

The entry point (`src/server.ts`) starts an Express app on `http://localhost:8788` by default and mounts two sets of routes:

- `/mcp` – Streamable HTTP MCP endpoint protected by bearer token verification
- `/authorize`, `/token`, `/revoke`, `/.well-known/*` – OAuth endpoints proxied upstream to Auth0 via the official SDK

For production you can use `npm run start` (also powered by `tsx`). Deployments should set the same environment variables and ensure HTTPS termination.

---

## 5. Tool overview

| Tool | Purpose | Backing data |
| --- | --- | --- |
| `search` | Semantic search over expert-call transcripts | OpenAI vector store |
| `fetch` | Retrieve full transcript text by file ID | OpenAI vector store |
| `airfare_trend_insights` | Filterable airfare pricing & demand dataset | CSV/TSV/JSON files in `synthetic_financial_data/web_search_trends` |

The TypeScript implementation closely mirrors the Python logic, including snippet generation, metadata retrieval, and filter semantics.

---

## 6. Authentication flow

1. MCP clients discover the OAuth metadata exposed by `mcpAuthRouter`
2. `/authorize`, `/token`, and `/revoke` requests are forwarded to Auth0 with no local state
3. Successful token responses are returned to the client untouched
4. Subsequent calls to `/mcp` must include `Authorization: Bearer <token>`
5. `verifyBearerToken` validates the JWT via the Auth0 JWKS, enforces required scopes & audience, and attaches claims to the request context

Auth0 Universal Login, Auth Code + PKCE, and refresh tokens are all handled upstream; this server simply validates and trusts the resulting tokens.

---

## 7. Testing with MCP Inspector

1. Ensure the server is running on `http://localhost:8788`
2. `npx @modelcontextprotocol/inspector@latest`
3. In the Inspector UI choose **HTTP Streaming**, URL `http://localhost:8788/mcp`
4. Complete the Auth0 login flow (the allowed client must match `OAUTH_ALLOWED_CLIENTS`)
5. Exercise the `search`, `fetch`, and `airfare_trend_insights` tools in the Inspector

---

## 8. Next steps

- Wire up your own data sources by editing the tool handlers in `src/server.ts`
- Deploy on a cloud hosting platform like [Render](https://render.com/) or [Vercel](https://vercel.com/).

Enjoy exploring MCP with TypeScript!
