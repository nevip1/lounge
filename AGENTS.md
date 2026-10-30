# Working on nevip’s lounge

This is a small personal link hub at `lounge.nevip.dev`. The homepage is the lobby; individual platforms have their own shareable routes, starting with `/switch`.

## Keep it personal

- Keep the purple/lavender palette, narrow centered layout, simple link cards, and small playful details. Both themes must stay purple. The owner wants a personal link page, not a landing page.
- Write like a person. Use very short, casual copy and lowercase labels where natural. Avoid slogans, welcome essays, filler cards, and sections explaining the obvious. Avoid marketing language, invented activity/status, fake stats, and filler sections.
- Only show actual profiles, friend codes, and destinations supplied by the owner. Never fabricate account details or working links for platforms that haven’t been configured.
- Keep Nintendo branding referential. This is nevip’s personal site, not an official Nintendo service.
- Preserve the light/dark themes, mobile layout, keyboard focus, reduced-motion support, and useful clipboard failure states.

## Project map

- `lounge.json`: public profile information, canonical domain, Nintendo code/link, and version. No secrets belong here.
- `templates/page.html`: shared document, header, footer, metadata.
- `templates/home.html`, `templates/switch.html`: page content.
- `templates/console.html`: unused legacy illustration.
- `assets/switch-avatar.png`: approved avatar shown on `/switch`; use this same artwork when updating the social preview.
- `assets/switch-preview-v2.png`: approved 1200×630 Switch social image with the owner’s avatar and “add me on switch” wording. The owner approved this image-tool extraction after being told that some small details were redrawn. Keep the approved artwork; do not add a provider/site-name label. Bump the image filename when replacing it to avoid stale social caches.
- `assets/style.css`: responsive styles and themes.
- `assets/app.js`: theme preference, friend-code clipboard, toast feedback.
- `scripts/build.py`: HTML escaping, config validation, and static generation.
- `scripts/serve.py`: local preview, `/switch` route, and real 404 responses.
- `dist/`: generated deployment output, ignored by Git. Never edit it directly.
- `wrangler.jsonc`: Cloudflare Workers Static Assets, clean routes, 404 handling, custom domain.
- `package.json`: optional Wrangler tooling for Workers preview and deployment.
- `DEPLOY.md`: browser-only Cloudflare dashboard instructions. Keep this workflow working without local CLI setup.

## Run and ship

Python 3.10+ is the only static-build dependency. Cloudflare Workers tooling additionally needs Node.js 22+ and `npm install`.

```sh
python3 scripts/build.py
python3 scripts/serve.py
```

Preview: `http://127.0.0.1:4173`. Build again after source changes; the preview serves the generated files. Deploy with `npm run deploy`; Wrangler automatically runs the Python build. First use `npm run deploy:check` for a non-publishing dry run. `npm run dev` previews the actual Workers asset routing. `/switch/` redirects to `/switch`; unknown routes must return the custom page with HTTP 404. The configured custom domain is `lounge.nevip.dev`, requiring the active `nevip.dev` zone in the deploying Cloudflare account. A config file is not proof of a live deployment. Do not replace an existing DNS destination without checking its purpose.

Cloudflare Workers Builds can install dependencies and execute `npm run deploy` from the website. Keep the build command in Wrangler so website deployment rebuilds generated files. The README deploy button clones a public source repository; importing `nevip1/lounge` in the dashboard is the preferred path for the owner. Changes must exist on GitHub before either flow can read them.

## Before finishing

- Build successfully and check `/`, `/switch`, `/switch/`, and an unknown route.
- Check mobile and desktop layouts when a browser is available. Be explicit if visual verification is unavailable.
- Verify friend-code copying, theme persistence, keyboard navigation, and external destinations when possible.
- Preserve the complete Nintendo friend URL, including its trailing share token. It cannot be reconstructed reliably from the code alone.
- Change the version in `lounge.json` with user-visible updates.
- Keep the site static unless a requested feature actually needs a backend. Avoid analytics, trackers, dependencies, or account systems without a concrete reason.
- Do not claim deployment is live from a local build or preview alone.
