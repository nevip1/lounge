# Deploy from the Cloudflare website

No local terminal or software installation is needed. Cloudflare installs Wrangler, builds the pages, and deploys them for you.

## 1. Make sure the files are on GitHub

Open [nevip1/lounge](https://github.com/nevip1/lounge) and check that you can see `wrangler.jsonc`, `package.json`, `scripts/`, `templates/`, and `assets/`.

Cloudflare reads GitHub, not the files on your computer. If these changes are still only local, publish them using your editor’s Git controls or GitHub Desktop’s **Commit** and **Push origin**. Do not upload `node_modules/`, `.git/`, or credentials. You do not need to build or upload `dist/`.

## 2. Import your repository

1. Open [Cloudflare Workers & Pages](https://dash.cloudflare.com/?to=/:account/workers-and-pages).
2. Choose **Create application**, then the option to import/connect an existing Git repository.
3. Connect GitHub and allow access to **`nevip1/lounge`**.
4. Select **`lounge`** and its production branch.
5. Use these settings:

| Field | Value |
| --- | --- |
| Worker / project name | `nevip-lounge` |
| Root directory | Repository root (leave the default) |
| Build command | Leave empty |
| Deploy command | `npm run deploy` |

The name must match `name` in `wrangler.jsonc`. Wrangler runs `python3 scripts/build.py` automatically; Cloudflare’s build environment handles it, so you do not need Python on your computer. Dependency installation is automatic. No API token needs to be pasted into this repository.

6. Click **Deploy** and wait for the build to finish.
7. Open the `workers.dev` URL shown by Cloudflare. Check the homepage and `/switch`.

## 3. Use lounge.nevip.dev

The repository already declares `lounge.nevip.dev` as a Workers Custom Domain. Use the Cloudflare account containing the active `nevip.dev` zone. Deployment applies that domain and Cloudflare manages its DNS and certificate.

If Cloudflare reports an existing DNS record conflict, inspect what that record serves before replacing it. If you only want a temporary `workers.dev` deployment, edit `wrangler.jsonc` on GitHub, remove the `routes` array, and deploy again. Add the custom domain later from your Worker’s **Settings → Domains & Routes → Add → Custom Domain**.

When deployment and certificate setup complete, open:

- `https://lounge.nevip.dev/`
- `https://lounge.nevip.dev/switch`

## Future changes

Edit the source files or `lounge.json` on GitHub and commit the change. Cloudflare automatically rebuilds and deploys pushes to the connected production branch. Build failures appear in the Worker’s build history.

## Optional: deploy button

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https%3A%2F%2Fgithub.com%2Fnevip1%2Flounge)

This is Cloudflare’s public repository template flow: it creates a copy in your GitHub account. For your existing `nevip1/lounge` repository, use the import workflow above to keep future updates connected to the original. The button requires the source repository to be public and these files to have been pushed.

Official references: [Dashboard deployment](https://developers.cloudflare.com/workers/get-started/dashboard/), [Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/), [Deploy to Cloudflare buttons](https://developers.cloudflare.com/workers/platform/deploy-buttons/).
