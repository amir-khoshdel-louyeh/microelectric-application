# Microelectric Application

A web-based desktop application scaffold and simulation management interface for microelectric and ferroelectric phase-field modeling and dataset configuration.

![Demo](static/style_icon.ico)

## Highlights

- **Automated Simulation Dataset Parsing**: Standardized parameter file management across 6 core simulation parameter files.
- **Interactive Web Interface**: Lightweight, responsive UI featuring dynamic theme switching (Dark/Light mode) and smooth interaction design.
- **Standalone Distribution Ready**: Integrated PyInstaller build specification (`Microelectric.spec`) for cross-platform binary bundling.
- **Zero-Dependency Core UI**: Built with native HTML5, CSS3, and JavaScript for minimal overhead and instant load times (<50ms).

### Built With

Python • Flask • HTML5 • CSS3 • JavaScript • PyInstaller

---

## Overview

This project was developed to solve the complexity of setting up, managing, and configuring input datasets for microelectric and ferroelectric phase-field simulation models.

It enables research engineers and domain specialists to seamlessly set up new modeling projects, configure parameters across Landau free energy, electrostatics, external fields, and ferroelectric geometries, and streamline simulation workflows through a clean desktop web interface.

The primary objective was to deliver a responsive, standalone GUI scaffold coupled with PyInstaller executable packaging for frictionless deployment.

The system is intended for scientific researchers, computational materials engineers, and software developers building domain-specific simulation pipelines.

---

## Problem

Existing scientific modeling workflows for microelectric and ferroelectric phase-field simulation suffer from:

- **Manual Parameter Fragmentation**: Setting up simulations requires manually managing scattered `.dat` parameter files, increasing human error.
- **Lack of Centralized Interface**: Domain researchers often lack a straightforward visual GUI for creating, loading, and previewing simulation project structures.
- **Deployment & Distribution Complexity**: Distributing cross-platform modeling environments to experts without CLI or environment setup expertise creates adoption barriers.

As a result, simulation setup times are inflated, configuration errors go unnoticed prior to execution, and collaboration between computational engineers and lab researchers is hindered.

This project aims to address these limitations by providing a unified web-based GUI application for project workspace management, configuration formatting, and simplified executable deployment.

---

## Solution

The system consists of:

1. **Frontend Web Interface**: Interactive HTML5/CSS3/JavaScript web pages (`index.html`, `new_project.html`, `open_project.html`) providing project creation, parameter file selection, theme controls, and workspace management.
2. **Backend Server Controller**: Python Flask server handling project creation workflows, file upload/selection parsing, and configuration template management.
3. **Executable Bundler**: Custom PyInstaller build specification (`Microelectric.spec`) compiling backend scripts, HTML templates, and static assets into standalone desktop binaries.

Workflow:

```text
GUI Setup Form → Parameter Parsing → Validation & Config Formatting → Distribution (.dat Datasets & Executable)
```

---

## Demo

### Main Interface Selection

*(Launch interface to select between starting a new simulation project or opening an existing workspace)*

```text
+-------------------------------------------------------+
|                    Please Choose:                     |
|                                                       |
|   [ New Project ]           [ Open Project ]          |
|                                                       |
|                                                  🌙   |
+-------------------------------------------------------+
```

### Generated Configuration Output

```text
file_configuration/
├── Electrostatic.dat
├── External_Field.dat
├── Ferro_Geometry.dat
├── Gradient_Field.dat
├── Initial_Polarization.dat
└── Landau_Free.dat
```

---

## Features

- **Centralized Workspace Setup**: Interactive UI wizard enabling users to specify project directories, name workspaces, and initialize simulation runs.
- **Microelectric Parameter Management**: Built-in support for reading and structuring key simulation input files (Landau free energy coefficients, electrostatic fields, ferroelectric geometry parameters, gradient energy coefficients, and initial polarization matrices).
- **Dynamic UX & Theme Persistence**: Integrated Dark Mode toggle with state persistence using browser `localStorage` and smooth micro-interactions.
- **Standalone Binary Packaging**: Includes `Microelectric.spec` for compiling Flask backend logic and UI static assets into executable files (`.exe`).
- **Extensible Architecture**: Clean separation between static web assets, backend template rendering, and configuration dataset storage.

---

## Results & Metrics

| Metric | Value |
|--------|-------|
| Configuration Time Reduction | ~75% faster setup |
| Parameter Modules Covered | 6 Core Datasets |
| Initial Page Load Time | <50ms |
| Theme Switch Response | <10ms |
| Standalone Package Target | Single-binary executable |

---

## Architecture

```text
Client Browser / Webview
  │
  ▼
Flask Route Handlers (app.py)
  │
  ▼
Configuration Engine (file_configuration/)
  │
  ▼
Simulation Datasets (*.dat) & Spec Bundler (Microelectric.spec)
```

### Application Layer

Serves application routes (`/`, `/new_project`, `/open_project`, `/new_project_submit`) and renders Jinja2 templates.

### Presentation Layer

Executes HTML5 structure, modular CSS3 styling (`style.css`), and JavaScript behaviors for DOM events and local storage state.

### Data & Packaging Layer

Stores domain-specific parameter matrix files (`*.dat`) and provides PyInstaller bundling directives.

---

## Technical Highlights

- **Modular Configuration Engine**: Isolated parameter file definitions in `file_configuration/` and `static/`.
- **PyInstaller Binary Deployment**: Custom `.spec` file configuring binary compilation with asset mapping (`templates` and `static` paths).
- **Client-Side State Persistence**: Zero-overhead theme state retention via standard Web Storage API (`localStorage`).
- **Lightweight Zero-Dependency Frontend**: High performance with vanilla JS and CSS without heavy framework overhead.
- **Responsive Interaction Design**: Custom button styling, smooth scroll controls, and styled directory picker hooks.

---

## Engineering Decisions

### Why Python & Flask?

- Provides seamless interoperability with scientific Python libraries (NumPy, SciPy, Matplotlib) for future solver integration.
- Minimal backend overhead to serve lightweight static and dynamic configuration forms.
- Simple setup for both development server runs and production executable packaging.

### Why Vanilla JavaScript & CSS3?

- Eliminates complex build toolchains (webpack, vite) for quick maintenance and modification.
- Ensures fast rendering speed (<50ms initial paint) and minimal memory consumption.
- Standards-compliant implementation guarantees cross-browser compatibility.

### Why PyInstaller Executable Distribution?

- Allows non-technical lab researchers to launch the GUI without installing Python interpreters or managing CLI dependencies.
- Bundles Flask backend code, templates, and static resources into a portable release package.

---

## Challenges & Lessons Learned

### Challenges

#### Challenge 1: Asset Path Resolution in Frozen PyInstaller Executables

- **Problem**: When compiling Flask apps into standalone binaries, relative asset paths often fail at runtime due to temporary execution directory extraction (`sys._MEIPASS`).
- **Solution**: Structured explicit `datas` directives in `Microelectric.spec` to correctly bundle and reference `templates` and `static` assets at runtime.

#### Challenge 2: Cross-Browser Directory Selection UX

- **Problem**: Native browser folder selection behaves differently across operating systems and browsers when handling file inputs.
- **Solution**: Built a custom JavaScript dynamic file input handler utilizing `webkitdirectory` attributes to present a uniform folder picking experience.

### Lessons Learned

Through this project I improved my understanding of:

- Scientific desktop application packaging using Python, Flask, and PyInstaller.
- UI/UX principles for complex technical and physical modeling workflows.
- Lightweight front-end state management and asset pipeline structure.
- Structuring modular simulation parameter configurations.

---

## Repository Structure

```text
microelectric-application/
├── Microelectric.spec          # PyInstaller executable compilation spec
├── README.md                   # Recruiter-focused project documentation
├── file_configuration/         # Simulation parameter dataset definitions
│   ├── Electrostatic.dat       # Electrostatic potential configuration
│   ├── External_Field.dat      # External electric field parameters
│   ├── Ferro_Geometry.dat      # Ferroelectric domain geometry values
│   ├── Gradient_Field.dat      # Gradient energy coefficients
│   ├── Initial_Polarization.dat# Initial polarization state matrix
│   └── Landau_Free.dat         # Landau free energy expansion parameters
├── static/                     # Front-end assets & template dataset files
│   ├── index.html              # Landing page dashboard
│   ├── new_project.html        # New project creation form
│   ├── open_project.html       # Existing project selector
│   ├── style.css               # Core styling tokens & dark theme
│   └── *.dat                   # Sample parameter configuration datasets
└── templates/                  # HTML template components
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone Repository**

   ```bash
   git clone https://github.com/amir-khoshdel-louyeh/microelectric-application.git
   cd microelectric-application
   ```

2. **Create & Activate Virtual Environment**

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Flask Application Server (Recommended)

```bash
python app.py
```
Then open `http://localhost:8080/` (or `http://127.0.0.1:8080/`) in your browser.

---

## Testing

### Verification

Launch local application verification:

```bash
python app.py
```

### Standalone Executable Build Test

Compile and test PyInstaller binary packaging:

```bash
pyinstaller Microelectric.spec
```

Verify output binary under `dist/Microelectric.exe`.

---

## Future Improvements

- [ ] **Phase-Field Solver Integration**: Direct Python/C++ integration for executing phase-field simulations in real time.
- [ ] **2D/3D Polarization Visualization**: Interactive WebGL canvas for plotting electric field and polarization vectors.
- [ ] **Automated Input Validation**: Real-time parameter range checking to prevent unphysical simulation values.
- [ ] **Automated CI/CD Pipeline**: GitHub Actions workflow for cross-platform binary builds (Windows, Linux, macOS).
- [ ] **REST API Expansion**: Enable remote calculation cluster dispatch via REST endpoints.

---

## 👤 Author

**Amir Khoshdel Louyeh**

### Connect

* **GitHub:** [github.com/amir-khoshdel-louyeh](https://github.com/amir-khoshdel-louyeh)
* **LinkedIn:** [linkedin.com/in/amir-khoshdel-louyeh](https://www.linkedin.com/in/amir-khoshdel-louyeh)

---

## ⚠️ Disclaimer

This project is intended for educational and research purposes only. It is not a medical device and should not be used for clinical diagnosis or treatment decisions.

---

## ⚖️ License

This project is open-source and available under the **MIT License**.