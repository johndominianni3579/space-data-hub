# 2026 Space Hub
**[View Live App](https://space-data-app-u6sgbiledu9gwaumfr2xkb.streamlit.app)**

An interactive, data-driven dashboard tracking the future of human spaceflight. This project aggregates real-time data from NASA and SpaceX to provide insights into upcoming missions, lunar exploration, and near-Earth objects.

### Key Features
* **Live SpaceX Tracking:** Fetches the soonest upcoming missions and satellite deployments.
* **Artemis Mission Log:** A hybrid module merging live NASA Image Library data with a manual 2026 mission status tracker.
* **NeoWs Asteroid Feed:** Real-time monitoring of nearby asteroids, including hazardous status and miss distance in kilometers.
* **Physics Utilities:** Integrated calculators for Artificial Gravity (RPM) and Mars Voyage durations based on user-defined speeds.
* **JSON:** Uses JSON: Uses persistence to store data from NASA and SpaceX's Public API
* **Security:** Uses environment variables to hide API keys

### Stack
* **Language:** Python 3.1
* **Framework:** Streamlit (UI/Deployment)
* **APIs:** NASA (APOD, NeoWs, Image Library), The Space Devs, SpaceX-API.
* **Libraries:** Requests, Pandas, Altair, Dotenv.
