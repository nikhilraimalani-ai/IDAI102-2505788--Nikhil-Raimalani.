import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="WaterBuddy 💧",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
# We use session_state to remember data (like how much water you drank) 
# even when the app refreshes after a button click.
if 'current_intake' not in st.session_state:
    st.session_state.current_intake = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Helper Functions ---
def get_recommended_goal(age_group):
    """Returns recommended water intake (in ml) based on age group."""
    if age_group == "6-12 Years":
        return 1600
    elif age_group == "13-18 Years":
        return 2000
    elif age_group == "19-50 Years":
        return 2500
    elif age_group == "65+ Years":
        return 2000
    else:
        return 2000

def get_mascot_message(progress_percent):
    """Returns a mascot emoji and message based on progress."""
    if progress_percent >= 100:
        return "🎉", "Amazing job! You reached your goal! Stay hydrated!"
    elif progress_percent >= 75:
        return "🔥", "Almost there! Just a little more to go!"
    elif progress_percent >= 50:
        return "🐢", "Halfway there! Slow and steady wins the race."
    elif progress_percent >= 25:
        return "👋", "Good start! Keep sipping."
    else:
        return "💧", "Time to start drinking! Your body needs water."

# --- Sidebar: User Settings ---
st.sidebar.header("⚙️ User Profile")
st.sidebar.write("Tell us about yourself to get a personalized goal.")

age_group = st.sidebar.selectbox(
    "Select your Age Group:",
    ("6-12 Years", "13-18 Years", "19-50 Years", "65+ Years")
)

# Auto-suggest goal based on age
suggested_goal = get_recommended_goal(age_group)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Daily Goal")
# Allow manual adjustment of the goal
daily_goal = st.sidebar.number_input(
    "Your Goal (ml):", 
    min_value=500, 
    max_value=5000, 
    value=suggested_goal, 
    step=50
)

# Reset Button in Sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Day"):
    st.session_state.current_intake = 0
    st.session_state.history = []
    st.rerun()

# --- Main Interface ---
st.title("WaterBuddy 💧")
st.markdown("### Your Daily Hydration Companion")

# 1. Display Stats (Columns)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🥤 Drunk", value=f"{st.session_state.current_intake} ml")

with col2:
    remaining = max(0, daily_goal - st.session_state.current_intake)
    st.metric(label="💧 Remaining", value=f"{remaining} ml")

with col3:
    percent = min(100, int((st.session_state.current_intake / daily_goal) * 100))
    st.metric(label="📈 Progress", value=f"{percent}%")

# 2. Visual Progress Bar
# Streamlit progress bar needs a value between 0.0 and 1.0
progress_bar_val = min(1.0, st.session_state.current_intake / daily_goal)
st.progress(progress_bar_val)

# 3. Mascot & Message Area
mascot, message = get_mascot_message(percent)

# Using a container for the visual feedback to make it pop
with st.container():
    st.markdown(f"""
    <div style="text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h1 style="font-size: 60px; margin: 0;">{mascot}</h1>
        <h3 style="color: #0e1117;">{message}</h3>
    </div>
    """, unsafe_allow_html=True)

# 4. Logging Controls
st.subheader("📝 Log Water")

c1, c2 = st.columns([1, 2])

with c1:
    # Quick Add Button
    if st.button("➕ Add 250 ml", type="primary"):
        st.session_state.current_intake += 250
        st.session_state.history.append(f"Added 250ml at {time.strftime('%H:%M')}")
        
        # NOTIFICATION ADDED HERE
        st.toast("🌊 250ml added! Keep it up!", icon='💧')
        
        if st.session_state.current_intake >= daily_goal:
            st.balloons() # Celebration effect
        
        # We add a small delay so the user sees the toast before rerun (optional but smoother)
        time.sleep(1)
        st.rerun()

with c2:
    # Custom Amount Add
    with st.form("custom_add"):
        custom_amount = st.number_input("Or add custom amount (ml):", min_value=1, max_value=1000, value=100)
        submitted = st.form_submit_button("Add Custom Amount")
        if submitted:
            st.session_state.current_intake += custom_amount
            st.session_state.history.append(f"Added {custom_amount}ml at {time.strftime('%H:%M')}")
            
            # NOTIFICATION ADDED HERE
            st.toast(f"🌊 {custom_amount}ml added! Great job!", icon='💧')
            
            if st.session_state.current_intake >= daily_goal:
                st.balloons()
            
            time.sleep(1)
            st.rerun()

# 5. Hydration History (Optional feature)
with st.expander("📜 View Today's History"):
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            st.write(f"- {item}")
    else:
        st.write("No water logged yet today.")
