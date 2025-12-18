# Planetary Motion 3D Simulation

A real-time 3D simulation of the solar system built with Python. This application visualizes the positions of planets using accurate ephemeris data and allows for interactive exploration.

## Features

*   **Real-Time Simulation**: Uses NASA's JPL ephemeris data (`de421.bsp`) via `skyfield` to calculate precise planetary positions.
*   **3D Visualization**: Interactive 3D plot using `matplotlib` showing the Sun and planets (Mercury through Neptune).
*   **Planet Inspector**: Click on any planet to open a detailed view featuring:
    *   A rotating 3D model with high-resolution textures.
    *   Real-time physical data (Mass, Diameter, Gravity, etc.).
*   **Interactive Controls**:
    *   **Focus**: Dropdown menu to center the camera on specific planets.
    *   **Speed Control**: Slider to adjust the simulation speed (days per frame).
    *   **Play/Pause**: Toggle the animation state.

## Requirements

*   Python 3.x
*   `skyfield`
*   `matplotlib`
*   `numpy`
*   `Pillow` (PIL)
*   `tkinter` (usually included with Python)
*   Google's Antigravity was also used to create the 3D version of this model from the 2D version

## Installation

1.  Clone or download this repository.
2.  Install the required dependencies:
    ```bash
    pip install skyfield matplotlib numpy Pillow
    ```
3.  Ensure the `assets` folder contains the planet texture images (PNG format).
4.  Ensure `de421.bsp` is present in the project directory (it will be downloaded automatically by skyfield if missing, but having it pre-downloaded is recommended).

## Usage

Run the main script:

```bash
python Planetry_Motion.py
```

### Controls
*   **Navigation**: Use the mouse to rotate, zoom, and pan the 3D view.
*   **Click**: Click on a planet dot to open the Inspector window.
*   **GUI**: Use the bottom control panel to change focus, speed, or pause the simulation.

## Assets
High-quality textures are loaded from the `assets/` directory to render realistic planet surfaces in the Inspector view.

## Application Structure

```text
Planetary_Motion.py
|--- Load Ephemeris Data (de421.bsp)
|
|--- Initialize GUI (Tkinter)
|    |--- Main Window
|    |--- 3D Plot Area (Matplotlib)
|    |--- Control Panel (Play, Speed, Focus)
|
|--- Animation Loop
|    |--- Update Time
|    |--- Calculate Positions (Skyfield)
|    |--- Redraw Scene
|
|--- User Interaction
     |--- Click Planet
          |--- Open Inspector Window
               |--- Load Texture (assets/*.png)
               |--- Render Rotating 3D Model
               |--- Display Physics Data
```
