import csv

def freq_to_hz(freq_str):
    """Convert frequency in MHz to Hz as integer string."""
    try:
        return str(int(float(freq_str) * 1_000_000))
    except:
        return "0"

def power_to_code(power_str):
    """Convert power string to H/M/L code."""
    if "High" in power_str:
        return "H"
    elif "Low" in power_str:
        return "L"
    elif "Mid" in power_str or "Med" in power_str:
        return "M"
    return "H"  # default

def bandwidth_from_mode(mode_str):
    """Return bandwidth based on FM/AM mode. Default to 25000."""
    # If you want to handle narrow FM, modify this function.
    return "25000"

def ctcss_dcs_to_field(tone_mode, ctcss, dcs):
    """Determine sub-audio field for CTCSS/DCS."""
    if tone_mode == "Tone" or tone_mode == "T Sql":
        return ctcss.replace(" Hz", "")
    elif tone_mode == "DCS":
        return dcs
    return "0"

def main():
    import os
    print("Current working directory:", os.getcwd())

    with open('ft3d.csv', newline='') as infile, open('channels_out.csv', 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        
        # Write header as in channels.csv
        writer.writerow([
            "title", "tx_freq", "rx_freq", "tx_sub_audio(CTCSS=freq/DCS=number)", "rx_sub_audio(CTCSS=freq/DCS=number)",
            "tx_power(H/M/L)", "bandwidth(12500/25000)", "scan(0=OFF/1=ON)", "talk around(0=OFF/1=ON)",
            "pre_de_emph_bypass(0=OFF/1=ON)", "sign(0=OFF/1=ON)", "tx_dis(0=OFF/1=ON)", "mute(0=OFF/1=ON)",
            "rx_modulation(0=FM/1=AM)", "tx_modulation(0=FM/1=AM)"
        ])
        
        for row in reader:
            title = row["Name"]
            tx_freq = freq_to_hz(row["Transmit Frequency"])
            rx_freq = freq_to_hz(row["Receive Frequency"])
            tx_power = power_to_code(row["Tx Power"])
            bandwidth = bandwidth_from_mode(row["Operating Mode"])
            
            # Sub-audio
            tx_sub_audio = ctcss_dcs_to_field(row["Tone Mode"], row["CTCSS"], row["DCS"])
            rx_sub_audio = ctcss_dcs_to_field(row["Tone Mode"], row["CTCSS"], row["DCS"])
            
            # Scan: 1 if not skipped, 0 if Skip == "On"
            scan = "0" if row["Skip"] == "On" else "1"
            
            # The rest default to 0 unless otherwise specified
            talk_around = "0"
            pre_de_emph_bypass = "0"
            sign = "0"
            tx_dis = "0"
            mute = "0"
            
            # Modulation: FM=0, AM=1
            rx_modulation = "0" if row["Operating Mode"] == "FM" else "1"
            tx_modulation = rx_modulation
            
            writer.writerow([
                title, tx_freq, rx_freq, tx_sub_audio, rx_sub_audio, tx_power, bandwidth, scan,
                talk_around, pre_de_emph_bypass, sign, tx_dis, mute, rx_modulation, tx_modulation
            ])

if __name__ == "__main__":
    main()
