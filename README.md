# nevip’s lounge

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https%3A%2F%2Fgithub.com%2Fnevip1%2Flounge)

**Deploy using the Cloudflare website:** see the [browser-only deployment guide](DEPLOY.md). No local Node.js, Python, or terminal is required for that workflow.

A small purple link page at `/`, with a Nintendo Switch friend code and profile link at `/switch`.

## Preview

Requires Python 3.10 or newer. No package install or Node.js required.

```sh
python3 scripts/serve.py
```

Open **http://127.0.0.1:4173**. The command builds once and starts a local server. After editing, run `python3 scripts/build.py` in another terminal and refresh.

## Personalize

Edit `lounge.json`. It contains the display name, canonical domain, version, Switch friend code, full Nintendo profile share URL, and app download page. The supplied friend code and share URL are already configured. This file is public configuration; keep secrets out of it.

The friend code uses `SW-0000-0000-0000` format. Preserve the full Nintendo share link, including the final token. Empty friend code/link values produce a clear coming-soon state instead of fake account details. Public links must use HTTPS, and the build checks that the friend URL matches the code.

## Deploy with Cloudflare Workers

For website deployment, follow [DEPLOY.md](DEPLOY.md). The commands below are the optional terminal workflow.

Requires Python 3.10+ and Node.js 22+ with npm. Run these commands from this repository on your computer:

```sh
npm install
npx wrangler login
npm run deploy:check
npm run deploy
```

`deploy:check` builds and validates the upload without publishing. `deploy` automatically rebuilds the site and uploads `dist/` using Workers Static Assets. There is no application server to manage.

The [Wrangler config](wrangler.jsonc) already sets:

- Worker name: `nevip-lounge`.
- Custom domain: **`lounge.nevip.dev`**.
- Clean URLs: `/switch/` redirects to `/switch`.
- Unknown routes: the custom `404.html` with HTTP 404.
- A `workers.dev` address as an additional deployment URL.

Sign in to the Cloudflare account that manages the active `nevip.dev` zone. Deploying the custom domain lets Cloudflare create its DNS record and certificate. If `lounge.nevip.dev` already has a DNS record, resolve that conflict in the dashboard first; do not replace another service accidentally. To deploy only to `workers.dev`, remove the `routes` array before running `npm run deploy`.

Check `https://lounge.nevip.dev/` and `https://lounge.nevip.dev/switch` after Wrangler reports a successful deployment. A local build or dry run alone does not verify a live deployment.

### Deploy automatically from GitHub

In Cloudflare **Workers & Pages**, create/import a Worker connected to this GitHub repository. Use these build settings:

| Setting | Value |
| --- | --- |
| Worker name | `nevip-lounge` |
| Root directory | `/` |
| Build command | Leave empty (Wrangler runs the configured Python build) |
| Deploy command | `npm run deploy` |

Dependency installation is automatic. Python 3 must be available in the build image. Keep `wrangler.jsonc` in the repository root. Once connected, pushes to the selected production branch rebuild and deploy the site. This repository has not been pushed or deployed by the local setup.

### Preview the Workers runtime

```sh
npm run dev
```

Wrangler prints its local URL, watches the source directories, and rebuilds on changes. For the dependency-free Python preview, use `python3 scripts/serve.py` instead.

The configuration follows Cloudflare’s [Workers Static Assets documentation](https://developers.cloudflare.com/workers/static-assets/) and [Custom Domains documentation](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/).

Nintendo app links point to [Nintendo’s official lounge](https://lounge.nintendo.com/), the download destination referenced in [Nintendo’s support instructions](https://www.nintendo.com/en-gb/Support/Troubleshooting/How-to-Download-or-Update-the-Nintendo-Switch-App-1520024.html).

## Details

- Static HTML/CSS and small vanilla JavaScript; built using Python’s standard library.
- Friend-code copying, with manual selection when browser permissions prevent clipboard access.
- Light/dark theme with local preference storage. Copying relies on JavaScript; the code and profile link remain available without it.
- Responsive layout, keyboard focus styles, accessible feedback, and reduced-motion support.
- DM Sans and Space Grotesk load from Google Fonts, with system fallbacks if unavailable.
- No analytics, cookies, backend, or database.
- Future contributors: read [AGENTS.md](AGENTS.md).
