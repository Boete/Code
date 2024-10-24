import streamlit as st
import math

# Function to add custom CSS for buttons
def set_button_style():
    st.markdown("""
    <style>
    div.stButton > button {
        width: 100%; 
        height: 50px; 
        font-size: 20px; 
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'result_text' not in st.session_state:
    st.session_state.result_text = ""  # Initialize result text in session state

# Set mode based on button clicks
def set_mode(mode):
    st.session_state.mode = mode
    st.session_state.result_text = ""  # Clear result when mode is changed

# Function to calculate Ohm's law (Voltage, Current, Resistance)
def calculate_ohms_law(v=None, i=None, r=None):
    if v is not None and i is not None:
        r = v / i
        return v, i, r
    elif v is not None and r is not None:
        i = v / r
        return v, i, r
    elif i is not None and r is not None:
        v = i * r
        return v, i, r
    return None, None, None

# Function to calculate total resistance in series
def calculate_series_resistance(resistances):
    return sum(resistances)

# Function to calculate total resistance in parallel
def calculate_parallel_resistance(resistances):
    return 1 / sum(1/r for r in resistances)

# Function to calculate voltage division
def voltage_divider(vin, r1, r2):
    vout = vin * (r2 / (r1 + r2))
    return vout

# Function to calculate current division
def current_divider(itotal, r1, r2):
    i1 = itotal * (r2 / (r1 + r2))
    i2 = itotal * (r1 / (r1 + r2))
    return i1, i2

# Function to calculate RMS voltage based on waveform type
def calculate_rms_voltage(peak_voltage, waveform_type):
    if waveform_type == 'sine':
        return peak_voltage / math.sqrt(2)
    elif waveform_type == 'square':
        return peak_voltage
    elif waveform_type == 'triangle':
        return peak_voltage / math.sqrt(3)
    elif waveform_type == 'sawtooth':
        return peak_voltage / 2
    elif waveform_type == 'half-wave rectified':
        return peak_voltage / 2
    elif waveform_type == 'full-wave rectified':
        return peak_voltage / math.sqrt(2)
    return 0

# Function to calculate impedance of an RLC circuit
def calculate_rlc_impedance(r, l, c, frequency):
    omega = 2 * math.pi * frequency
    xl = omega * l
    xc = 1 / (omega * c)
    impedance = math.sqrt(r**2 + (xl - xc)**2)
    return impedance

# Function to calculate 3-phase power
def three_phase_power(v_phase, i_phase, power_factor, connection_type):
    if connection_type.upper() == 'Y':
        return math.sqrt(3) * v_phase * i_phase * power_factor
    elif connection_type.upper() == 'DELTA':
        return 3 * v_phase * i_phase * power_factor
    return 0

# Function to read 4-band resistor
def read_4_band_resistor(colors):
    color_codes = {
        "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
        "green": 5, "blue": 6, "violet": 7, "gray": 8, "white": 9
    }
    first_digit = color_codes[colors[0].lower()]
    second_digit = color_codes[colors[1].lower()]
    multiplier = 10 ** color_codes[colors[2].lower()]
    resistance = (first_digit * 10 + second_digit) * multiplier
    return resistance

# Function to read 5-band resistor
def read_5_band_resistor(colors):
    color_codes = {
        "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
        "green": 5, "blue": 6, "violet": 7, "gray": 8, "white": 9
    }
    first_digit = color_codes[colors[0].lower()]
    second_digit = color_codes[colors[1].lower()]
    third_digit = color_codes[colors[2].lower()]
    multiplier = 10 ** color_codes[colors[3].lower()]
    resistance = (first_digit * 100 + second_digit * 10 + third_digit) * multiplier
    return resistance

# Streamlit App
st.title("Electrical Calculator")

# Apply custom button style
set_button_style()

# Buttons for navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("DC"):
        set_mode('DC')
with col2:
    if st.button("AC"):
        set_mode('AC')
with col3:
    if st.button("Device Reader"):
        set_mode('Device Reader')

# DC Mode
if st.session_state.mode == 'DC':
    st.header("DC Calculators")

    calc_type = st.selectbox("Choose a DC calculation", ["Ohm's Law", "Series/Parallel Resistor", "Voltage/Current Divider"])

    # Ohm's Law Calculator
    if calc_type == "Ohm's Law":
        v = st.number_input("Voltage (V)", value=0.0)
        i = st.number_input("Current (I)", value=0.0)
        r = st.number_input("Resistance (R)", value=0.0)

        if st.button("Calculate Ohm's Law"):
            v, i, r = calculate_ohms_law(v if v > 0 else None, i if i > 0 else None, r if r > 0 else None)
            st.session_state.result_text = f"Calculated Values: Voltage = {v} V, Current = {i} A, Resistance = {r} Ω"
        # Result Box as a text box at the bottom
        st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)

    # Series and Parallel Resistor Calculator
    elif calc_type == "Series/Parallel Resistor":
        calculation_type = st.selectbox("Select calculation type", ["Series", "Parallel"])
        resistances = st.text_input("Enter resistances (comma-separated, e.g., 10, 20, 30)")

        if resistances:
            try:
                res_list = [float(r) for r in resistances.split(',')]
                if calculation_type == "Series":
                    series_res = calculate_series_resistance(res_list)
                    if st.button("Calculate Series Resistance"):
                        st.session_state.result_text = f"Total Series Resistance: {series_res} Ω"
                elif calculation_type == "Parallel":
                    parallel_res = calculate_parallel_resistance(res_list)
                    if st.button("Calculate Parallel Resistance"):
                        st.session_state.result_text = f"Total Parallel Resistance: {parallel_res} Ω"
                # Result Box as a text box at the bottom
                st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)
            except ValueError:
                st.session_state.result_text = "Please enter valid resistor values."

    # Voltage/Current Divider Calculator
    elif calc_type == "Voltage/Current Divider":
        divider_type = st.selectbox("Select divider type", ["Voltage Divider", "Current Divider"])

        if divider_type == "Voltage Divider":
            vin = st.number_input("Enter input voltage (Vin)", value=0.0)
            r1 = st.number_input("Enter R1", value=0.0)
            r2 = st.number_input("Enter R2", value=0.0)

            if st.button("Calculate Voltage Divider"):
                vout = voltage_divider(vin, r1, r2)
                st.session_state.result_text = f"Output Voltage (Vout): {vout} V"

        elif divider_type == "Current Divider":
            itotal = st.number_input("Enter total current (Itotal)", value=0.0)
            r1 = st.number_input("Enter R1", value=0.0)
            r2 = st.number_input("Enter R2", value=0.0)

            if st.button("Calculate Current Divider"):
                i1, i2 = current_divider(itotal, r1, r2)
                st.session_state.result_text = f"Current through R1: {i1} A, Current through R2: {i2} A"
        # Result Box as a text box at the bottom
        st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)

# AC Mode
elif st.session_state.mode == 'AC':
    st.header("AC Calculators")

    calc_type = st.selectbox("Choose an AC calculation", ["Vrms", "RLC Impedance", "3-Phase Power"])

    # Vrms Calculator
    if calc_type == "Vrms":
        peak_voltage = st.number_input("Peak Voltage (Vpeak)", value=0.0)
        waveform_type = st.selectbox("Select Waveform Type", options=["sine", "square", "triangle", "sawtooth", "half-wave rectified", "full-wave rectified"])

        if st.button("Calculate RMS Voltage"):
            rms_voltage = calculate_rms_voltage(peak_voltage, waveform_type)
            st.session_state.result_text = f"RMS Voltage: {rms_voltage} V"
        # Result Box as a text box at the bottom
        st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)

    # RLC Impedance Calculator
    elif calc_type == "RLC Impedance":
        r = st.number_input("Resistance (R in Ohms)", value=0.0)
        l = st.number_input("Inductance (L in Henry)", value=0.0)
        c = st.number_input("Capacitance (C in Farad)", value=0.0)
        frequency = st.number_input("Frequency (Hz)", value=0.0)

        if st.button("Calculate RLC Impedance"):
            impedance = calculate_rlc_impedance(r, l, c, frequency)
            st.session_state.result_text = f"Impedance: {impedance} Ω"
        # Result Box as a text box at the bottom
        st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)

    # 3-Phase Power Calculator
    elif calc_type == "3-Phase Power":
        v_phase = st.number_input("Phase Voltage (V)", value=0.0)
        i_phase = st.number_input("Phase Current (I)", value=0.0)
        power_factor = st.number_input("Power Factor (pf)", value=1.0)
        connection_type = st.selectbox("Connection Type", options=["Y", "Delta"])

        if st.button("Calculate 3-Phase Power"):
            power = three_phase_power(v_phase, i_phase, power_factor, connection_type)
            st.session_state.result_text = f"3-Phase Power: {power} W"
        # Result Box as a text box at the bottom
        st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)
# Device Reader Mode
elif st.session_state.mode == 'Device Reader':
    st.header("Device Reader")

    reader_type = st.selectbox("Choose a device reader", ["4-Band Resistor", "5-Band Resistor"])

    # 4-Band Resistor Reader
    if reader_type == "4-Band Resistor":
        colors = [st.selectbox(f"Choose color for {band}", ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "gray", "white"]) for band in ["Band 1", "Band 2", "Multiplier"]]

        if st.button("Read 4-Band Resistor"):
            resistance = read_4_band_resistor(colors)
            st.session_state.result_text = f"4-Band Resistor Value: {resistance} Ω"
        # Result Box as a text box at the bottom
        st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)

    # 5-Band Resistor Reader
    elif reader_type == "5-Band Resistor":
        colors = [st.selectbox(f"Choose color for {band}", ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "gray", "white"]) for band in ["Band 1", "Band 2", "Band 3", "Multiplier"]]

        if st.button("Read 5-Band Resistor"):
            resistance = read_5_band_resistor(colors)
            st.session_state.result_text = f"5-Band Resistor Value: {resistance} Ω"
        # Result Box as a text box at the bottom
        st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)

# Result Box as a text box at the bottom
# st.text_area("Results", value=st.session_state.result_text, height=100, key="result_box", disabled=True)
