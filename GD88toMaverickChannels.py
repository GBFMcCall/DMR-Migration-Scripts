import csv
from pathlib import Path

GD88_FILE = Path("gd88.csv")
MAV_WORKING_FILE = Path("maverick_working_copy.csv")
TG_FILE = Path("talkgroups.CSV")
OUTPUT_FILE = Path("maverick_from_gd88_final.csv")


def hz_to_mhz(val: str) -> str:
    if not val:
        return ""
    s = str(val).strip()
    try:
        f = float(s)
        if f > 1000:
            f = f / 1_000_000.0
        return f"{f:.5f}"
    except ValueError:
        return s


def load_tg_mapping(tg_file: Path):
    """Load talkgroups.CSV into {name: radio_id} dict for lookup."""
    mapping = {}
    with tg_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("Name") or "").strip()
            radio_id = row.get("Radio ID", "").strip()
            if name and radio_id:
                mapping[name] = radio_id
    print(f"Loaded {len(mapping)} talkgroups: {list(mapping.keys())[:5]}...")
    return mapping


def map_channel_type(gd_type: str, template_type: str) -> str:
    if not gd_type:
        return template_type
    t = gd_type.strip().upper()
    if "ANALOG" in t:
        return "A-Analog"
    if "DIGITAL" in t:
        return "D-Digital"
    return template_type


def slot_from_gd88(row: dict, default_slot: str) -> str:
    for key in ("CCTX", "TSTX", "TS TX", "TS"):
        if key in row and row[key]:
            ts = row[key].strip().upper()
            if ts.startswith("TS"):
                return ts[2:]
            return ts
    return default_slot


def color_code_from_gd88(row: dict, default_cc: str) -> str:
    for key in ("CC", "CC TX", "CCTX"):
        if key in row and row[key]:
            return row[key].strip()
    return default_cc


def main():
    print("1. Loading talkgroups.CSV...")
    tg_mapping = load_tg_mapping(TG_FILE)

    print("2. Loading Maverick working file...")
    if not MAV_WORKING_FILE.exists():
        print(f"ERROR: {MAV_WORKING_FILE} not found.")
        return

    with MAV_WORKING_FILE.open("r", encoding="utf-8-sig", newline="") as f:
        mreader = csv.DictReader(f)
        header = mreader.fieldnames
        working_rows = list(mreader)

    digital_template = next(
        (r for r in working_rows if (r.get("Channel Type") or "").startswith("D")),
        None,
    )
    analog_template = next(
        (r for r in working_rows if (r.get("Channel Type") or "").startswith("A")),
        None,
    )

    if digital_template is None or analog_template is None:
        print("ERROR: Missing digital/analog template rows.")
        return

    print("3. Converting GD88 channels...")
    if not GD88_FILE.exists():
        print(f"ERROR: {GD88_FILE} not found.")
        return

    with GD88_FILE.open("r", encoding="utf-8-sig", newline="") as src, \
         OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as dst:

        gd_reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=header)
        writer.writeheader()

        next_no = 1000  # Adjust if needed to avoid existing channels
        rows_written = 0

        for gd_row in gd_reader:
            if not any(gd_row.values()):
                continue

            # === ADJUST THESE GD88 FIELD NAMES TO MATCH YOUR HEADER ===
            gd_name = (
                gd_row.get("Name")
                or gd_row.get("CH Name")
                or gd_row.get("NameRX")
                or ""
            ).strip()
            if not gd_name:
                continue

            gd_rx = gd_row.get("RX Freq") or ""
            gd_tx = gd_row.get("TX Freq") or ""
            gd_type = gd_row.get("Type") or ""
            gd_contact = (
                gd_row.get("Contact Name")
                or gd_row.get("Contact NameRX Group Name")
                or ""
            ).strip()

            is_digital = "DIGITAL" in gd_type.upper()
            template = digital_template if is_digital else analog_template

            out = dict(template)

            # Core channel fields
            out["No."] = str(next_no)
            next_no += 1
            out["Channel Name"] = gd_name[:16]
            out["Receive Frequency"] = hz_to_mhz(gd_rx)
            out["Transmit Frequency"] = hz_to_mhz(gd_tx)
            out["Channel Type"] = map_channel_type(gd_type, template.get("Channel Type", ""))

            # Contact/TG lookup using talkgroups.CSV
            if gd_contact and gd_contact in tg_mapping:
                out["Contact/TG"] = gd_contact[:16]
                out["Contact/TG TG/DMR ID"] = tg_mapping[gd_contact]
                print(f"Mapped '{gd_contact}' -> TG {tg_mapping[gd_contact]}")
            elif gd_contact:
                print(f"WARNING: '{gd_contact}' not found in talkgroups.CSV")

            # DMR-specific fields
            if is_digital:
                out["Slot"] = slot_from_gd88(gd_row, template.get("Slot", "1"))
                out["RX Color Code"] = color_code_from_gd88(gd_row, template.get("RX Color Code", "1"))

            # Optional fields
            gd_scan = gd_row.get("Scan List Name") or ""
            if gd_scan:
                out["Scan List"] = gd_scan[:16]

            gd_rxgrp = gd_row.get("RX Group Name") or ""
            if gd_rxgrp:
                out["Receive Group List"] = gd_rxgrp[:16]

            writer.writerow(out)
            rows_written += 1

    print(f"✅ SUCCESS: Wrote {rows_written} channels to {OUTPUT_FILE.resolve()}")
    print("CPS Import: Tools → Import → Channels → maverick_from_gd88_final.csv")


if __name__ == "__main__":
    main()
