"""Generate portable static pages. Python 3.10+, standard library only."""
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'


def render(template, values):
    return re.sub(r'\{\{(\w+)\}\}', lambda m: values[m[1]], template)


def build():
    config = json.loads((ROOT / 'lounge.json').read_text())
    switch = config['switch']
    code = switch['friendCode']
    if code and not re.fullmatch(r'SW-\d{4}-\d{4}-\d{4}', code):
        raise ValueError('friendCode must be empty or use SW-0000-0000-0000 format')
    for url in [config['domain'], switch['appUrl'], switch['friendUrl']]:
        if url and (urlparse(url).scheme != 'https' or not urlparse(url).netloc):
            raise ValueError('Public links must be absolute HTTPS URLs')
    if switch['friendUrl'] and urlparse(switch['friendUrl']).hostname != 'lounge.nintendo.com':
        raise ValueError('friendUrl must be an official lounge.nintendo.com share link')
    if code and switch['friendUrl'] and code[3:] not in switch['friendUrl']:
        raise ValueError('The friend code and Nintendo share URL must match')
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / 'assets', DIST / 'assets')
    base = (ROOT / 'templates/page.html').read_text()
    values = {key: html.escape(str(value), quote=True) for key, value in {
        'name': config['name'], 'version': config['version'],
        'friend_code': code or 'Coming soon', 'app_url': switch['appUrl'],
        'code_disabled': '' if code else 'disabled',
        'code_help': 'Copy it here. Paste it on your console.' if code else 'My player card is still being set up. Check back soon.',
    }.items()}
    values['console'] = (ROOT / 'templates/console.html').read_text()
    values['friend_action'] = (
        '<a class="primary-button" href="' + html.escape(switch['friendUrl'], quote=True) +
        '" target="_blank" rel="noopener noreferrer">add friend <span aria-hidden="true">↗</span>'
        '<span class="sr-only"> (opens in a new tab)</span></a>'
        if switch['friendUrl'] else '<p class="code-help">My app link is coming soon.</p>'
    )
    for page, path, title, description in [
        ('home', '', f"{config['name']}’s lounge — links & friend codes", 'nevip’s links and friend codes.'),
        ('switch', '/switch', f"Nintendo Switch — {config['name']}’s lounge", f"Add {config['name']} on Nintendo Switch. Friend code: {code or 'coming soon'}. "),
    ]:
        content = render((ROOT / f'templates/{page}.html').read_text(), values)
        social_title = 'add me on switch' if page == 'switch' else title
        social_description = (code or 'friend code coming soon') if page == 'switch' else description
        social_image_meta = ''
        if page == 'switch':
            image_url = html.escape(config['domain'].rstrip('/') + '/assets/switch-preview-v2.png', quote=True)
            social_image_meta = f'''<meta property="og:image" content="{image_url}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Neven’s Switch avatar above the words add me on switch on a purple background.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="add me on switch">
  <meta name="twitter:description" content="{html.escape(social_description, quote=True)}">
  <meta name="twitter:image" content="{image_url}">'''

        page_values = {**values, 'page': page, 'content': content,
                       'title': html.escape(title), 'description': html.escape(description, quote=True),
                       'social_title': html.escape(social_title, quote=True),
                       'social_description': html.escape(social_description, quote=True),
                       'social_image_meta': social_image_meta,
                       'canonical': html.escape(config['domain'].rstrip('/') + path, quote=True),
                       'home_current': 'aria-current="page"' if page == 'home' else '',
                       'switch_current': 'aria-current="page"' if page == 'switch' else ''}
        output = DIST / path.lstrip('/') / 'index.html'
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render(base, page_values))
    (DIST / '404.html').write_text(render(base, {**values, 'page': '404', 'title': 'Lost in the lounge',
        'description': 'This corner of the lounge does not exist.', 'canonical': html.escape(config['domain'], quote=True),
        'social_title': 'Lost in the lounge', 'social_description': 'This page does not exist.',
        'social_image_meta': '', 'home_current': '', 'switch_current': '', 'content': '<section class="intro"><div class="eyebrow">404</div><h1 style="margin:24px 0">wrong page.</h1><p>nothing here.</p><a class="text-link" href="/">Back to the lounge ↗</a></section>'}))
    (DIST / '_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: DENY\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n')
    print(f'Built {DIST}: home, /switch, 404, assets')


if __name__ == '__main__':
    build()
