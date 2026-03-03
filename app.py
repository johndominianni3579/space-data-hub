import streamlit as st
import os
from datetime import datetime

# Import your collectors
from collectors.spacex_api import get_next_launch
from collectors.nasa_artemis_api import get_artemis_updates
from collectors.rocket_specs import get_spacex_fleet
from collectors.nasa_visuals import get_apod
from collectors.asteroids import get_nearby_asteroids

from utilities.artifical_gravity import calculate_gravity
from utilities.mars_trip_duration import calculate_mars_trip

st.set_page_config(page_title="2026 Space Hub", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #3e4452; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ 2026 Global Space Exploration Hub")
st.caption(f"Real-time Data Sync: {datetime.now().strftime('%B %d, %Y')}")

# --- SIDEBAR: MISSION ENGINEERING TOOLS ---
with st.sidebar:
    st.header("🛠️ Mission Engineering")
    
    # Tool 1: Artificial Gravity
    st.subheader("Gravity Designer")
    radius = st.slider("Spacecraft Radius (meters):", 5, 500, 50)
    rpm = calculate_gravity(radius)
    st.info(f"Required Spin: **{rpm} RPM** for 1G")
    
    st.markdown("---")
    
    # Tool 2: Mars Duration
    st.subheader("Mars Transit Calc")
    speed = st.number_input("Speed (kph):", value=28000, step=1000)
    trip = calculate_mars_trip(speed)
    st.success(f"Travel Time: **{trip['days']} Days**")
    st.caption(f"Approx. {trip['months']} Months at {trip['speed']}")

# --- SECTION 1: NASA APOD  ---
st.header("🌠 Astronomy Picture of the Day")
apod = get_apod()

if "error" not in apod:
    col_visual, col_txt = st.columns([2, 1])
    
    with col_visual:
        # Check if the media is a video or image
        if apod.get("media_type") == "video":
            st.video(apod['url'])
        else:
            st.image(apod['url'], use_container_width=True)
            
    with col_txt:
        st.subheader(apod['title'])
        st.write(apod['explanation'])
else:
    st.error("NASA Visuals API currently limited or unavailable.")

st.markdown("---")

# --- SECTION 2: LIVE MISSION DATA ---
col_launch, col_asteroids = st.columns(2)

with col_launch:
    st.header("SpaceX's Next Launch")
    launch = get_next_launch()
    if "error" not in launch:
        st.subheader(f"🚀 Mission: {launch['name']}")
        st.write(f"**NET Date:** {launch['date']}")
        st.write(f"*Details:* {launch['details']}")
    else:
        st.warning(launch['error'])

with col_asteroids:
    st.header("Near-Earth Asteroids")
    asteroids = get_nearby_asteroids()
    if asteroids:
        for a in asteroids:
            with st.expander(f"Object: {a['name']}"):
                st.write(f"Hazardous: **{a['hazard']}**")
                st.write(f"Velocity: {a['velocity_kph']} kph")
                st.write(f"Miss Distance: {a['miss_dist_km']} km")
    else:
        st.info("No asteroid approach data for today.")

st.markdown("---")

# --- SECTION 3: ARTEMIS & FLEET ---
st.header("The NASA Artemis Human Exploration Program's Upcoming Missions")
artemis = get_artemis_updates()
art_cols = st.columns(len(artemis)) # Dynamically create columns based on count

for i, mission in enumerate(artemis):
    with art_cols[i]:
        # Check if the mission is Artemis 4 to use your local file
        if mission.get('name') == "Artemis IV":
            image_to_show = os.path.join("assets", "artemis_4_placeholder.jpeg")
            caption_text = f"{mission['name']} (Placeholder Image)"
        else:
            image_to_show = mission['image']
            caption_text = mission['name']

        st.image(image_to_show, caption=caption_text, use_container_width=True)
        st.write(f"**Status:** {mission['status']}")

st.markdown("---")

# --- SECTION 4: SPACEX FLEET & STARSHIP ROADMAP ---
st.header("The SpaceX Starship Fleet & Roadmap")
fleet = get_spacex_fleet()
if isinstance(fleet, list):
    for rocket in fleet:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(rocket['image'], width=300)
            with col2:
                st.subheader(rocket['name'])
                st.write(f"**Active:** {rocket['active']} | **Height:** {rocket['height_m']} | **Mass:** {rocket['mass_kg']}")
                
                if "roadmap" in rocket:
                    st.write("---")
                    st.write("**2026-2027 Starship Roadmap:**")
                    for date, event in rocket["roadmap"].items():
                        st.write(f"✅ **{date}**: {event}")
            st.write("---")