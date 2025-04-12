import pandas as pd

def convert_gd88_to_dm32(gd88_file, dm32_file):
    """
    Converts a GD88 channel CSV file to a DM32 channel CSV file format.

    Args:
        gd88_file (str): Path to the GD88 channel CSV file.
        dm32_file (str): Path to the DM32 channel CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the converted data.
    """

    # Read the GD88 CSV file into a DataFrame
    gd88_df = pd.read_csv(gd88_file)

    # Create a new DataFrame with the DM32 column structure
    dm32_df = pd.DataFrame(columns=[
        "No.", "Channel Name", "Channel Type", "RX Frequency[MHz]", "TX Frequency[MHz]",
        "Power", "Band Width", "Scan List", "TX Admit", "Emergency System", "Squelch Level",
        "APRS Report Type", "Forbid TX", "APRS Receive", "Forbid Talkaround", "Auto Scan",
        "Lone Work", "Emergency Indicator", "Emergency ACK", "Analog APRS PTT Mode",
        "Digital APRS PTT Mode", "TX Contact", "RX Group List", "Color Code", "Time Slot",
        "Encryption", "Encryption ID", "APRS Report Channel", "Direct Dual Mode",
        "Private Confirm", "Short Data Confirm", "DMR ID", "CTC/DCS Encode", "CTC/DCS Decode",
        "Scramble", "RX Squelch Mode", "Signaling Type", "PTT ID", "VOX Function", "PTT ID Display"
    ])

    # Iterate over each row in the GD88 DataFrame and map the data to the DM32 DataFrame
    new_rows = []
    for index, row in gd88_df.iterrows():
        channel_type = "Analog" if row["Type"].upper() == "ANALOG" else "Digital"
        rx_freq_mhz = row["RX Freq"] / 1000000.0
        tx_freq_mhz = row["TX Freq"] / 1000000.0

        new_row = {
            "No.": index + 1,
            "Channel Name": row["CH Name"],
            "Channel Type": channel_type,
            "RX Frequency[MHz]": rx_freq_mhz,
            "TX Frequency[MHz]": tx_freq_mhz,
            "Power": row["Power"],
            "Band Width": row["Bandwidth"],
            "Scan List": row["Scan List Name"],
            "TX Admit": "Allow TX",
            "Emergency System": "None",
            "Squelch Level": 3,
            "APRS Report Type": "Off",
            "Forbid TX": 0,
            "APRS Receive": 0,
            "Forbid Talkaround": 0,
            "Auto Scan": 0,
            "Lone Work": 0,
            "Emergency Indicator": 0,
            "Emergency ACK": 0,
            "Analog APRS PTT Mode": 0,
            "Digital APRS PTT Mode": 0,
            "TX Contact": row["Contact Name"],
            "RX Group List": row["RX Group Name"],
            "Color Code": row["RX CC"] if channel_type == "Digital" else 0,
            "Time Slot": row["RX TS"] if channel_type == "Digital" else "Slot 1",
            "Encryption": 0,
            "Encryption ID": "None",
            "APRS Report Channel": 1,
            "Direct Dual Mode": 0,
            "Private Confirm": 0,
            "Short Data Confirm": 0,
            "DMR ID": "Radio 1",
            "CTC/DCS Encode": "None",
            "CTC/DCS Decode": "None",
            "Scramble": "None",
            "RX Squelch Mode": "Carrier/CTC",
            "Signaling Type": "None",
            "PTT ID": "OFF",
            "VOX Function": 0,
            "PTT ID Display": 0
        }
        new_rows.append(new_row)

    dm32_df = pd.concat([dm32_df, pd.DataFrame(new_rows)], ignore_index=True)

    return dm32_df

# File paths
gd88_file = "gd88channel.csv"
dm32_file = "dm32channel.csv"
output_file = "output.csv"  # Specify the output file name

# Convert the data
converted_df = convert_gd88_to_dm32(gd88_file, dm32_file)

# Save the converted data to a CSV file
converted_df.to_csv(output_file, index=False)

# Display the first 3 rows of the converted data
print(converted_df.head(3))
