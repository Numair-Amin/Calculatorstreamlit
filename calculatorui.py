import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="iOS Calculator", layout="centered")

# --- Map emoji symbols to Python arithmetic operators ---
emoji_to_operator = {
    "➕": "+",
    "➖": "-",
    "✖️": "*",
    "➗": "/"
}

# --- Initialize session state variables ---
if "expression" not in st.session_state:
    st.session_state.expression = ""  # Current expression shown on screen
if "history" not in st.session_state:
    st.session_state.history = []  # Stores past calculations
if "show_history" not in st.session_state:
    st.session_state.show_history = False  # Toggle history panel
if "theme" not in st.session_state:
    st.session_state.theme = "Light"  # Default theme

# --- Theme Selector ---
st.session_state.theme = st.selectbox("Select Theme", ["Light", "Dark"], index=0, key="theme_selector")

theme_colors = {
    "Light": {
        "bg": "#ffffff",
        "text": "#000000",
        "border": "#000000",
        "button_bg": "#f0f0f0",
        "button_text": "#000000",
        "number_bg": "#e0e0e0",
        "operator_bg": "#ff9500",
        "equal_bg": "#34c759"
    },
    "Dark": {
        "bg": "#000000",
        "text": "#ffffff",
        "border": "#ffffff",
        "button_bg": "#4d4d4d",
        "button_text": "#ffffff",
        "number_bg": "#505050",
        "operator_bg": "#ff9500",
        "equal_bg": "#34c759"
    }
}
colors = theme_colors[st.session_state.theme]

# --- Create button click callback using closures ---
def make_callback(label):
    def callback():
        expr = st.session_state.expression

        # Convert emoji to valid operator for evaluation
        label_eval = emoji_to_operator.get(label, label)

        # Handle special buttons
        if label == "C":
            st.session_state.expression = ""
        elif label == "⌫":
            st.session_state.expression = expr[:-1]
        elif label == "=":
            try:
                result = str(eval(expr))
                st.session_state.history.append(f"{expr} = {result}")
                st.session_state.expression = result
            except:
                st.session_state.expression = "Error"
        elif label == "H":
            st.session_state.show_history = not st.session_state.show_history
        else:
            if expr == "Error":
                st.session_state.expression = label_eval
            else:
                st.session_state.expression += label_eval
    return callback

# --- Display the current expression/output box ---
st.markdown(f"""
    <div style='background-color: {colors['bg']}; color: {colors['text']}; width: 650px; 
                font-size: 48px; text-align: right; padding: 15px; 
                border-radius: 50px; margin-bottom: 20px; border: 2px solid {colors['border']};'>
        {st.session_state.expression or '0'}
    </div>
""", unsafe_allow_html=True)

# --- Custom CSS Styling for Buttons ---
st.markdown(f"""
    <style>
    div.stButton > button {{
        font-size: 32px !important;
        border-radius: 40px;
        height: 80px;
        width: 80px;
        margin: 6px;
        font-weight: bold;
        border: none;
        background-color: {colors['number_bg']} !important;
        color: {colors['button_text']} !important;
    }}

    div[data-testid="stButton-C"] > button,
    div[data-testid="stButton-⌫"] > button,
    div[data-testid="stButton-H"] > button {{
        background-color: {colors['button_bg']} !important;
        color: {colors['button_text']} !important;
    }}

    div[data-testid="stButton-➕"] > button,
    div[data-testid="stButton-➖"] > button,
    div[data-testid="stButton-✖️"] > button,
    div[data-testid="stButton-➗"] > button {{
        background-color: {colors['operator_bg']} !important;
        color: white !important;
    }}

    div[data-testid="stButton-="] > button {{
        background-color: {colors['equal_bg']} !important;
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Helper function to create a row of buttons ---
def button_row(labels):
    cols = st.columns(4)
    for i, label in enumerate(labels):
        with cols[i]:
            st.button(label, key=f"btn_{label}", on_click=make_callback(label))

# --- Calculator Button Layout ---
button_row(["C", "⌫", "H", "➗"])
button_row(["7", "8", "9", "✖️"])
button_row(["4", "5", "6", "➖"])
button_row(["1", "2", "3", "➕"])

# --- Last row: 0, ., = ---
cols = st.columns(4)
with cols[0]:
    st.button("0", key="btn_0", on_click=make_callback("0"))
with cols[1]:
    st.button(".", key="btn_dot", on_click=make_callback("."))
with cols[2]:
    st.button("=", key="btn_equal", on_click=make_callback("="))

# --- Display Calculation History ---
if st.session_state.show_history:
    st.markdown("### 🕓 History")
    if st.session_state.history:
        for entry in reversed(st.session_state.history[-10:]):
            st.code(entry)
    else:
        st.info("No history yet.")
