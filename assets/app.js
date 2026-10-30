(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-button');
  function setTheme(theme) {
    root.dataset.theme = theme;
    themeButton.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    themeButton.setAttribute('aria-pressed', String(theme === 'dark'));
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#191321' : '#f3eefb';
  }
  let savedTheme;
  try { savedTheme = localStorage.getItem('lounge-theme'); } catch { /* Storage may be disabled. */ }
  setTheme(savedTheme === 'light' || savedTheme === 'dark' ? savedTheme : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  themeButton.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(theme);
    try { localStorage.setItem('lounge-theme', theme); } catch { /* Keep the toggle usable without storage. */ }
  });

  let toastTimer;
  function toast(message) {
    const element = document.querySelector('#toast');
    element.textContent = message;
    element.classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => element.classList.remove('visible'), 3500);
  }
  async function copyText(text) {
    if (!navigator.clipboard?.writeText) return false;
    try { await navigator.clipboard.writeText(text); return true; }
    catch { return false; }
  }
  const copyButton = document.querySelector('#copy-code');
  copyButton?.addEventListener('click', async () => {
    const input = document.querySelector('#friend-code');
    if (await copyText(input.value)) {
      toast('copied!');
    } else {
      input.focus();
      input.select();
      toast('Code selected. Hold to copy, or press Ctrl/Cmd + C.');
    }
  });
})();
