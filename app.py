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

    # Result box for calculations
    result_box = st.empty()

    # Ohm's Law Calculator
    if calc_type == "Ohm's Law":
        v = st.number_input("Voltage (V)", value=0.0)
        i = st.number_input("Current (I)", value=0.0)
        r = st.number_input("Resistance (R)", value=0.0)

        if st.button("Calculate Ohm's Law"):
            v, i, r = calculate_ohms_law(v if v > 0 else None, i if i > 0 else None, r if r > 0 else None)
            result_box.success(f"Voltage = {v} V, Current = {i} A, Resistance = {r} Ω")

    # Series and Parallel Resistor Calculator
    elif calc_type == "Series/Parallel Resistor":
        calculation_type = st.selectbox("Select calculation type", ["Series", "Parallel"])
        resistances = st.text_input("Enter resistances (comma-separated, e.g., 10, 20, 30)")

        if st.button("Calculate Resistors"):
            if resistances:
                try:
                    res_list = [float(r) for r in resistances.split(',')]
                    if calculation_type == "Series":
                        series_res = calculate_series_resistance(res_list)
                        result_box.success(f"Total Series Resistance: {series_res} Ω")
                    elif calculation_type == "Parallel":
                        parallel_res = calculate_parallel_resistance(res_list)
                        result_box.success(f"Total Parallel Resistance: {parallel_res} Ω")
                except ValueError:
                    result_box.error("Please enter valid resistor values.")
            else:
                result_box.text("Results will appear here.")

    # Voltage/Current Divider Calculator
    elif calc_type == "Voltage/Current Divider":
        divider_type = st.selectbox("Select divider type", ["Voltage Divider", "Current Divider"])

        if divider_type == "Voltage Divider":
            vin = st.number_input("Enter input voltage (Vin)", value=0.0)
            r1 = st.number_input("Enter R1", value=0.0)
            r2 = st.number_input("Enter R2", value=0.0)

            if st.button("Calculate Voltage Divider"):
                vout = voltage_divider(vin, r1, r2)
                result_box.success(f"Output Voltage (Vout): {vout} V")

        elif divider_type == "Current Divider":
            itotal = st.number_input("Enter total current (Itotal)", value=0.0)
            r1 = st.number_input("Enter R1", value=0.0)
            r2 = st.number_input("Enter R2", value=0.0)

            if st.button("Calculate Current Divider"):
                i1, i2 = current_divider(itotal, r1, r2)
                result_box.success(f"Current through R1: {i1} A, Current through R2: {i2} A")

# AC Mode
elif st.session_state.mode == 'AC':
    st.header("AC Calculators")

    calc_type = st.selectbox("Choose an AC calculation", ["Vrms", "RLC Impedance", "3-Phase Power"])

    # Result box for AC calculations
    result_box = st.empty()

    # Vrms Calculator
    if calc_type == "Vrms":
        peak_voltage = st.number_input("Peak Voltage (Vpeak)", value=0.0)
        waveform_type = st.selectbox("Select Waveform Type", options=["sine", "square", "triangle", "sawtooth", "half-wave rectified", "full-wave rectified"])

        if st.button("Calculate RMS Voltage"):
            rms_voltage = calculate_rms_voltage(peak_voltage, waveform_type)
            result_box.success(f"Calculated RMS Voltage for {waveform_type} wave: {rms_voltage} V")

    # RLC Impedance Calculator
    elif calc_type == "RLC Impedance":
        r = st.number_input("Resistance (R)", value=0.0)
        l = st.number_input("Inductance (L in Henry)", value=0.0)
        c = st.number_input("Capacitance (C in Farad)", value=0.0)
        frequency = st.number_input("Frequency (Hz)", value=0.0)

        if st.button("Calculate RLC Impedance"):
            impedance = calculate_rlc_impedance(r, l, c, frequency)
            result_box.success(f"RLC Impedance: {impedance} Ω")

    # 3-Phase Power Calculator
    elif calc_type == "3-Phase Power":
        v_phase = st.number_input("Phase Voltage (V)", value=0.0)
        i_phase = st.number_input("Phase Current (I)", value=0.0)
        power_factor = st.number_input("Power Factor (0-1)", value=1.0)
        connection_type = st.selectbox("Connection Type", options=["Y", "Delta"])

        if st.button("Calculate 3-Phase Power"):
            total_power = three_phase_power(v_phase, i_phase, power_factor, connection_type)
            result_box.success(f"Calculated 3-Phase Power: {total_power} W")

# Device Reader Mode with Resistor Reader
elif st.session_state.mode == 'Device Reader':
    st.header("Device Reader")
    
    st.subheader("Resistor Reader (4-Band and 5-Band)")
    resistor_type = st.selectbox("Select Resistor Type", options=["4-Band", "5-Band"])

    # Result box for resistor reading
    result_box = st.empty()

    if resistor_type == "4-Band":
        colors = st.text_input("Enter 4 colors (comma-separated, e.g., red, green, blue, gold)").split(",")
        
        if st.button("Calculate Resistance"):
            if len(colors) == 4:
                try:
                    resistance = read_4_band_resistor(colors)
                    result_box.success(f"4-Band Resistor Value: {round(resistance, 2)} Ω")
                except KeyError:
                    result_box.error("Invalid color entered. Please enter valid resistor colors.")

    elif resistor_type == "5-Band":
        colors = st.text_input("Enter 5 colors (comma-separated, e.g., red, green, blue, orange, gold)").split(",")
        
        if st.button("Calculate Resistance"):
            if len(colors) == 5:
                try:
                    resistance = read_5_band_resistor(colors)
                    result_box.success(f"5-Band Resistor Value: {round(resistance, 2)} Ω")
                except KeyError:
                    result_box.error("Invalid color entered. Please enter valid resistor colors.")
