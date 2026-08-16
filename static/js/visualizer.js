/**
 * Microelectric Visualizer Module
 * Renders 2D polarization vectors and Landau free energy double-well potential curves on HTML5 Canvas.
 */

window.renderVisualizer = function() {
    const config = window.collectParameters ? window.collectParameters() : {};
    renderVectorGrid(config);
    renderEnergyCurve(config);
};

function renderVectorGrid(config) {
    const canvas = document.getElementById('vector-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    const isDark = document.body.classList.contains('dark-mode');
    ctx.fillStyle = isDark ? '#1e1e1e' : '#f9f9f9';
    ctx.fillRect(0, 0, width, height);

    const ip = config.Initial_Polarization || {};
    const mode = ip.initialization_mode || 'random_noise';
    const px0 = parseFloat(ip.initial_Px || 0);
    const py0 = parseFloat(ip.initial_Py || 0);
    const pz0 = parseFloat(ip.initial_Pz || 0.75);
    const noise = parseFloat(ip.noise_amplitude || 0.05);

    const rows = 12;
    const cols = 12;
    const cellW = width / cols;
    const cellH = height / rows;

    ctx.lineWidth = 1.5;

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const centerX = c * cellW + cellW / 2;
            const centerY = r * cellH + cellH / 2;

            let vx = px0;
            let vy = py0;

            if (mode === 'random_noise') {
                vx += (Math.random() - 0.5) * noise * 2;
                vy += (Math.random() - 0.5) * noise * 2;
            } else if (mode === 'vortex') {
                const dx = c - cols / 2;
                const dy = r - rows / 2;
                const norm = Math.sqrt(dx * dx + dy * dy) || 1;
                vx = -dy / norm;
                vy = dx / norm;
            } else if (mode === 'single_domain') {
                vy = pz0 !== 0 ? pz0 : 0.75;
            }

            const len = Math.sqrt(vx * vx + vy * vy) || 1;
            const scale = 12;
            const dirX = (vx / len) * scale;
            const dirY = -(vy / len) * scale; // Invert Y for canvas

            // Draw vector arrow
            ctx.strokeStyle = isDark ? '#8ac926' : '#52b69a';
            ctx.beginPath();
            ctx.moveTo(centerX - dirX / 2, centerY - dirY / 2);
            ctx.lineTo(centerX + dirX / 2, centerY + dirY / 2);
            ctx.stroke();

            // Arrow head point
            ctx.fillStyle = isDark ? '#f4a261' : '#e76f51';
            ctx.beginPath();
            ctx.arc(centerX + dirX / 2, centerY + dirY / 2, 2.5, 0, 2 * Math.PI);
            ctx.fill();
        }
    }
}

function renderEnergyCurve(config) {
    const canvas = document.getElementById('energy-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    const isDark = document.body.classList.contains('dark-mode');
    ctx.fillStyle = isDark ? '#1e1e1e' : '#f9f9f9';
    ctx.fillRect(0, 0, width, height);

    const lf = config.Landau_Free || {};
    const a1 = parseFloat(lf.alpha1 || -1.25e8);
    const a11 = parseFloat(lf.alpha11 || -2.1e8);
    const a111 = parseFloat(lf.alpha111 || 2.6e9);

    // Draw coordinate axes
    ctx.strokeStyle = isDark ? '#555' : '#ccc';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(width / 2, 20);
    ctx.lineTo(width / 2, height - 20);
    ctx.moveTo(20, height / 2);
    ctx.lineTo(width - 20, height / 2);
    ctx.stroke();

    // Plot energy potential f(P) = a1*P^2 + a11*P^4 + a111*P^6
    ctx.strokeStyle = isDark ? '#f4a261' : '#0056b3';
    ctx.lineWidth = 2.5;
    ctx.beginPath();

    const points = [];
    let minE = Infinity;
    let maxE = -Infinity;

    for (let i = 0; i <= width; i++) {
        const pNorm = ((i - width / 2) / (width / 2)) * 1.2; // P in [-1.2, 1.2]
        const p2 = pNorm * pNorm;
        const energy = a1 * p2 + a11 * p2 * p2 + a111 * p2 * p2 * p2;

        if (energy < minE) minE = energy;
        if (energy > maxE) maxE = energy;
        points.push({ x: i, e: energy });
    }

    const range = (maxE - minE) || 1;

    for (let i = 0; i < points.length; i++) {
        const pt = points[i];
        const y = height - 30 - ((pt.e - minE) / range) * (height - 60);
        if (i === 0) {
            ctx.moveTo(pt.x, y);
        } else {
            ctx.lineTo(pt.x, y);
        }
    }
    ctx.stroke();

    // Draw labels
    ctx.fillStyle = isDark ? '#aaa' : '#666';
    ctx.font = '12px Poppins, sans-serif';
    ctx.fillText('Polarization (P)', width - 110, height / 2 - 8);
    ctx.fillText('Free Energy f(P)', width / 2 + 10, 30);
}
