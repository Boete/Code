import streamlit as st
import math

# Function to calculate voltage, current, resistance
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

# Function to calculate 3-phase power
def three_phase_power(v_phase, i_phase, power_factor, connection_type):
    if connection_type.upper() == 'Y':
        return math.sqrt(3) * v_phase * i_phase * power_factor
    elif connection_type.upper() == 'DELTA':
        return 3 * v_phase * i_phase * power_factor
    return 0

# Function to calculate resistance from 4-band resistor colors
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

# Function to calculate resistance from 5-band resistor colors
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

# Streamlit UI
st.title("Electrical Calculator")

# Sidebar for navigation
menu = ["DC", "AC", "Device Reading"]
choice = st.sidebar.selectbox("Select a mode", menu)

# DC Mode
if choice == "DC":
    st.header("Ohm's Law Calculator")
    v = st.number_input("Voltage (V)", value=0.0)
    i = st.number_input("Current (I)", value=0.0)
    r = st.number_input("Resistance (R)", value=0.0)

    if st.button("Calculate"):
        v, i, r = calculate_ohms_law(v if v > 0 else None, i if i > 0 else None, r if r > 0 else None)
        st.success(f"Calculated Values: Voltage = {v} V, Current = {i} A, Resistance = {r} Ω")

# AC Mode
elif choice == "AC":
    st.header("RMS Voltage Calculator")
    peak_voltage = st.number_input("Peak Voltage (Vpeak)", value=0.0)
    waveform_type = st.selectbox("Select Waveform Type", options=["sine", "square", "triangle", "sawtooth", "half-wave rectified", "full-wave rectified"])

    if st.button("Calculate RMS Voltage"):
        rms_voltage = calculate_rms_voltage(peak_voltage, waveform_type)
        st.success(f"Calculated RMS Voltage for {waveform_type} wave: {rms_voltage} V")

    st.header("3-Phase Power Calculator")
    v_phase = st.number_input("Phase Voltage (V)", value=0.0)
    i_phase = st.number_input("Phase Current (I)", value=0.0)
    power_factor = st.number_input("Power Factor (0-1)", value=1.0)
    connection_type = st.selectbox("Connection Type", options=["Y", "Delta"])

    if st.button("Calculate 3-Phase Power"):
        total_power = three_phase_power(v_phase, i_phase, power_factor, connection_type)
        st.success(f"Calculated 3-Phase Power: {total_power} W")

# Device Reading Mode
elif choice == "Device Reading":
    st.header("Device Reading")
    device_type = st.selectbox("Select Device Type", options=["4-Band Resistor", "5-Band Resistor"])

    color_options = [
        "black", "brown", "red", "orange", "yellow",
        "green", "blue", "violet", "gray", "white"
    ]

    if device_type == "4-Band Resistor":
        st.subheader("Enter Colors for 4-Band Resistor")
        color1 = st.selectbox("Color 1", options=color_options)
        color2 = st.selectbox("Color 2", options=color_options)
        color3 = st.selectbox("Multiplier Color", options=color_options)

        if st.button("Calculate Resistance"):
            resistance = read_4_band_resistor([color1, color2, color3])
            st.success(f"Calculated Resistance: {resistance} Ω")

    elif device_type == "5-Band Resistor":
        st.subheader("Enter Colors for 5-Band Resistor")
        color1 = st.selectbox("Color 1", options=color_options, key='color1')
        color2 = st.selectbox("Color 2", options=color_options, key='color2')
        color3 = st.selectbox("Color 3", options=color_options, key='color3')
        color4 = st.selectbox("Multiplier Color", options=color_options, key='color4')

        if st.button("Calculate Resistance"):
            resistance = read_5_band_resistor([color1, color2, color3, color4])
            st.success(f"Calculated Resistance: {resistance} Ω")
 #gjkyhgj

