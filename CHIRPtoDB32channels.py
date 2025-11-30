## EXAMPLE USE
## python CHIRPtoDB32channels.py "C:\Users\grant\Downloads\h8.csv" "C:\Users\grant\Downloads\xx.csv"
## if the second file doesn't exist, it will create it. If it does exist, it will append to it.

import csv
import os
import argparse
import sys


def convert_tidradio_to_dm32(input_file, output_file):
    # Define DM32 headers
    dm32_headers = [
        "No.","Channel Name","Channel Type","RX Frequency[MHz]","TX Frequency[MHz]",
        "Power","Band Width","Scan List","TX Admit","Emergency System","Squelch Level",
        "APRS Report Type","Forbid TX","APRS Receive","Forbid Talkaround","Auto Scan",
        "Lone Work","Emergency Indicator","Emergency ACK","Analog APRS PTT Mode",
        "Digital APRS PTT Mode","TX Contact","RX Group List","Color Code","Time Slot",
        "Encryption","Encryption ID","APRS Report Channel","Direct Dual Mode",
        "Private Confirm","Short Data Confirm","DMR ID","CTC/DCS Decode","CTC/DCS Encode",
        "Scramble","RX Squelch Mode","Signaling Type","PTT ID","VOX Function","PTT ID Display"
    ]

    # If the output exists and has content, append; otherwise create and write header.
    output_exists = os.path.isfile(output_file)
    write_header = True
    if output_exists:
        try:
            with open(output_file, newline='') as of:
                existing_header = next(csv.reader(of), None)
                if existing_header:
                    write_header = False
                    if existing_header != dm32_headers:
                        print(f"Warning: existing header in '{output_file}' differs from expected DM32 headers.", file=sys.stderr)
        except Exception as e:
            print(f"Warning reading existing output file header: {e}", file=sys.stderr)

    # If appending to an existing file, continue numbering after existing rows
    start_index = 1
    if output_exists and not write_header:
        try:
            with open(output_file, newline='') as of:
                existing_reader = csv.reader(of)
                next(existing_reader, None)
                start_index = sum(1 for _ in existing_reader) + 1
        except Exception:
            start_index = 1

    with open(input_file, newline='') as infile, open(output_file, 'a', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=dm32_headers)
        if write_header:
            writer.writeheader()

        for i, row in enumerate(reader, start=start_index):
            rx_freq = float(row["Frequency"])
            duplex = row["Duplex"].strip()
            offset = float(row["Offset"]) if row["Offset"] else 0.0

            # Calculate TX frequency based on duplex
            if duplex == "+":
                tx_freq = rx_freq + offset
            elif duplex == "-":
                tx_freq = rx_freq - offset
            else:
                tx_freq = rx_freq  # simplex

            # Map power
            power_map = {"8.0W": "High", "4.0W": "Low"}
            power = power_map.get(row.get("Power",""), "High")

            # Bandwidth: assume FM channels are 25kHz, narrow FM 12.5kHz
            bandwidth = "25KHz" if rx_freq < 400 else "12.5KHz"

            dm32_row = {
                "No.": i,
                "Channel Name": row["Name"],
                "Channel Type": "Analog" if row["Mode"] == "FM" else "Digital",
                "RX Frequency[MHz]": f"{rx_freq:.5f}",
                "TX Frequency[MHz]": f"{tx_freq:.5f}",
                "Power": power,
                "Band Width": bandwidth,
                "Scan List": "None",
                "TX Admit": "Always",
                "Emergency System": "None",
                "Squelch Level": "3",
                "APRS Report Type": "Off",
                "Forbid TX": "0",
                "APRS Receive": "0",
                "Forbid Talkaround": "0",
                "Auto Scan": "0",
                "Lone Work": "0",
                "Emergency Indicator": "0",
                "Emergency ACK": "0",
                "Analog APRS PTT Mode": "0",
                "Digital APRS PTT Mode": "0",
                "TX Contact": row["Name"],
                "RX Group List": row["Name"],
                "Color Code": "1",
                "Time Slot": "Slot 1",
                "Encryption": "0",
                "Encryption ID": "None",
                "APRS Report Channel": "1",
                "Direct Dual Mode": "0",
                "Private Confirm": "0",
                "Short Data Confirm": "0",
                "DMR ID": "DM32",
                "CTC/DCS Decode": row.get("cToneFreq","None"),
                "CTC/DCS Encode": row.get("cToneFreq","None"),
                "Scramble": "None",
                "RX Squelch Mode": "Carrier/CTC",
                "Signaling Type": "None",
                "PTT ID": "OFF",
                "VOX Function": "0",
                "PTT ID Display": "0"
            }

            writer.writerow(dm32_row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CHIRP/TID radio CSV to DM32 format")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("output", nargs="?", default="DM32_converted.csv", help="Output CSV file (default: DM32_converted.csv)")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(2)

    try:
        convert_tidradio_to_dm32(args.input, args.output)
        print(f"Wrote output to '{args.output}'")
    except Exception as e:
        print(f"Error converting file: {e}", file=sys.stderr)
        sys.exit(1)