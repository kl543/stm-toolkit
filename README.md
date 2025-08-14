# STM Data Toolkit (minimal notebooks)

Small, self-contained notebooks for common STM/AFM post-processing tasks.  
Only a few example figures are shown; raw data and low-level details are intentionally omitted.

- **Focus:** topography detrending, dI/dV linecuts, simple coverage estimation (AFM edge detection).
- **Design goals:** tiny, reproducible, easy to skim; keep repository size small (notebooks saved with cleared outputs).

---

## Notebooks

**1) Edge detection for coverage (AFM / C60)**  
- View (nbviewer):  
  https://nbviewer.org/github/kl543/stm-toolkit/blob/main/notebooks/edge-detection.ipynb  
- Download (.ipynb):  
  https://raw.githubusercontent.com/kl543/stm-toolkit/main/notebooks/edge-detection.ipynb

**2) dI/dV linecut & topography path (K3C60)**  
- View (nbviewer):  
  https://nbviewer.org/github/kl543/stm-toolkit/blob/main/notebooks/linecut%20and%20topography.ipynb  
- Download (.ipynb):  
  https://raw.githubusercontent.com/kl543/stm-toolkit/main/notebooks/linecut%20and%20topography.ipynb

> Tip: If you rename the file to `linecut-topography.ipynb`, update the two links above accordingly.

---

## Selected Figures

<p align="center">
  <img src="assets/img/stm-k3c60-topography-10nm-gold-linecut-arrow.png"
       alt="STM topography of K3C60 (10 nm, gold colormap); arrow marks linecut path."
       width="360">
  <img src="assets/img/stm-k3c60-didv-linecut-stack-heatmap-10nm-pm20mv.png"
       alt="K3C60 dI/dV linecut: stacked spectra and heatmap (±20 mV) along ~10 nm path."
       width="360">
  <img src="assets/img/afm-c60-coverage-edge-detection-10nm-2025-07-19.png"
       alt="AFM C60 coverage measured via edge detection on a 10 nm scan."
       width="360">
</p>

---

## Repository Layout

