# Microelectric Application

A simple web-based application scaffold for microelectric projects. This repository currently contains static HTML pages and assets to open, create, and manage microelectric project files.

## Features

- Static HTML pages for common project flows:
  - `index.html`: Landing page
  - `new_project.html`: Start a new project
  - `open_project.html`: Open an existing project
- Basic styling via `static/style.css`
- Template scaffolding under `not commited/templates/`
- Configuration artifacts in `file_configuration/`
- Specification file `Microelectric.spec`

## Folder Structure

```
microelectric-application/
├── Microelectric.spec
├── file_configuration/
├── not commited/
│   └── templates/
└── static/
    ├── index.html
    ├── new_project.html
    ├── open_project.html
    └── style.css
```

## Getting Started

Because this project is currently static, you can open the HTML files directly in a browser.

### Option 1: Open files directly
- Double-click `static/index.html` to launch the app.
- Or open from the terminal:

```bash
xdg-open static/index.html
```

### Option 2: Serve locally (recommended)
Use a lightweight local web server to avoid cross-origin or file URL quirks.

- Python 3 built-in server:

```bash
# From repository root
python3 -m http.server 8080
# Then open http://localhost:8080/static/index.html
```

- Node.js (if installed):

```bash
# Using npx (no install)
npx serve static -l 8080
# Then open http://localhost:8080/index.html
```

## Development

- Edit the pages in `static/` and styles in `static/style.css`.
- Place reusable HTML snippets under `not commited/templates/`.
- Store or update project configuration under `file_configuration/`.
- Keep `Microelectric.spec` in sync with the UI as features evolve.

## Roadmap

- Add a minimal build step and asset pipeline.
- Implement JavaScript behavior for project creation/opening flows.
- Introduce tests (UI and integration) and CI.
- Document file formats used in `file_configuration/`.

## Contributing

1. Fork the repo and create a feature branch.
2. Make changes with clear commits.
3. Open a pull request describing the change and testing steps.

## License

Specify the license here (e.g., MIT). If none, consider adding one.

## Contact

Maintainer: amir-khoshdel-louyeh

If you have questions or suggestions, please open an issue.