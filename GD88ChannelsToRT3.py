import csv

def convert_try_to_rt3s(try_file, rt3s_file):
    with open(try_file, newline='') as infile, open(rt3s_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = [
            "Channel Mode", "Channel Name", "RX Frequency(MHz)", "TX Frequency(MHz)", "Band Width",
            "Scan List", "Squelch", "RX Ref Frequency", "TX Ref Frequency", "TOT[s]", "TOT Rekey Delay[s]",
            "Power", "Admit Criteria", "Auto Scan", "Rx Only", "Lone Worker", "VOX", "Allow Talkaround",
            "Send GPS Info", "Receive GPS Info", "Private Call Confirmed", "Emergency Alarm Ack",
            "Data Call Confirmed", "Allow Interrupt", "DCDM Switch", "Leader/MS", "Emergency System",
            "Contact Name", "Group List", "Color Code", "Repeater Slot", "In Call Criteria", "Privacy",
            "Privacy No.", "GPS System", "CTCSS/DCS Dec", "CTCSS/DCS Enc", "Rx Signaling System",
            "Tx Signaling System", "QT Reverse", "Non-QT/DQT Turn-off Freq", "Display PTT ID",
            "Reverse Burst/Turn-off Code", "Decode 1", "Decode 2", "Decode 3", "Decode 4", "Decode 5",
            "Decode 6", "Decode 7", "Decode 8"
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            mode = "1" if row["Type"].upper() == "ANALOG" else "2"
            power = "2" if row["Power"].upper() == "HIGH" else "0"
            rx_freq = f"{int(row['RX Freq']) / 1e6:.5f}"
            tx_freq = f"{int(row['TX Freq']) / 1e6:.5f}"
            slot = "1" if row["TX TS"] == "TS1" else "2"
            color_code = row.get("TX CC", "1")

            rt3s_row = {
                "Channel Mode": mode,
                "Channel Name": row["CH Name"],
                "RX Frequency(MHz)": rx_freq,
                "TX Frequency(MHz)": tx_freq,
                "Band Width": "0",
                "Scan List": "0",
                "Squelch": "3",
                "RX Ref Frequency": "0",
                "TX Ref Frequency": "0",
                "TOT[s]": "4",
                "TOT Rekey Delay[s]": "0",
                "Power": power,
                "Admit Criteria": "0",
                "Auto Scan": "0",
                "Rx Only": "0",
                "Lone Worker": "0",
                "VOX": "0",
                "Allow Talkaround": "0",
                "Send GPS Info": "0",
                "Receive GPS Info": "0",
                "Private Call Confirmed": "0",
                "Emergency Alarm Ack": "0",
                "Data Call Confirmed": "0",
                "Allow Interrupt": "0",
                "DCDM Switch": "1",
                "Leader/MS": "0",
                "Emergency System": "1",
                "Contact Name": row.get("Contact Name", "None"),
                "Group List": row.get("RX Group Name", "None"),
                "Color Code": color_code,
                "Repeater Slot": slot,
                "In Call Criteria": "1",
                "Privacy": "0",
                "Privacy No.": "0",
                "GPS System": "0",
                "CTCSS/DCS Dec": row.get("RX Tone", "None"),
                "CTCSS/DCS Enc": row.get("TX Tone", "None"),
                "Rx Signaling System": "0",
                "Tx Signaling System": "0",
                "QT Reverse": "0",
                "Non-QT/DQT Turn-off Freq": "0",
                "Display PTT ID": "0",
                "Reverse Burst/Turn-off Code": "0",
                "Decode 1": "0",
                "Decode 2": "0",
                "Decode 3": "0",
                "Decode 4": "0",
                "Decode 5": "0",
                "Decode 6": "0",
                "Decode 7": "0",
                "Decode 8": "0"
            }

            writer.writerow(rt3s_row)

# Example usage:
convert_try_to_rt3s(r"C:\Users\grant\Downloads\try.csv", r"C:\Users\grant\Downloads\converted_rt3s.csv")

