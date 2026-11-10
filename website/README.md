# NAVARIS Public Website Preview

This folder contains a public-facing Arabic-first marketing page that reuses the repository's NAVARIS identity and the ChatGPT-like conversation layout already present in `app/src/app/globals.css`. It is intentionally limited to service descriptions and contact buttons; internal tools, project data, workbooks and analysis are not exposed.

## Preview locally

From the repository root, open `website/index.html` in a browser, or run a static server:

```bash
python -m http.server 8080
```

Then visit `http://localhost:8080/website/`.

The WhatsApp links open a prefilled draft; the visitor must choose to send it. There is no automated analysis, booking, payment, or lead storage in this static page. No YouTube URL is configured because the channel URL has not been supplied.

## Publish

This is a preview, not a deployment. Before making it the live GitHub Pages homepage, verify page ownership and required repository workflows, test Arabic/mobile accessibility and all links, then deliberately switch the Pages source to this folder (or merge its approved contents into the current root `index.html`). Preserve the existing website until that review passes.
