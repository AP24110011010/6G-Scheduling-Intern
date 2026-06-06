
project_name = "Event-Driven 6G Scheduling"
week_number = 1
is_simulation = True
risk_threshold = 0.7

print("Project:", project_name)
print("Week:", week_number)
print("Risk Threshold:", risk_threshold)


devices = ["Device1", "Device2", "Device3", "Device4", "Device5"]

print("\nAvailable Devices:")
for device in devices:
    print(" -", device)


device_info = {
    "Device1": {"risk": 0.3, "status": "normal"},
    "Device2": {"risk": 0.7, "status": "at-risk"},
    "Device3": {"risk": 0.5, "status": "normal"},
    "Device4": {"risk": 0.9, "status": "compromised"},
    "Device5": {"risk": 0.2, "status": "normal"},
}

print("\nDevice Status:")
for name, info in device_info.items():
    print(f"  {name} | Risk: {info['risk']} | Status: {info['status']}")


def send_packet(source, destination):
    print(f"\nPacket sent from {source} to {destination}")

def check_risk(device_name, threshold=0.6):
    risk = device_info[device_name]["risk"]
    if risk >= threshold:
        print(f"  WARNING: {device_name} has high risk ({risk}) - above threshold {threshold}")
    else:
        print(f"  {device_name} is safe (risk={risk})")


send_packet("Device1", "Device5")
send_packet("Device3", "Device2")

print("\nRisk Check for All Devices:")
for device in devices:
    check_risk(device)

total_risk = 0
for device in devices:
    total_risk += device_info[device]["risk"]

average_risk = total_risk / len(devices)
print(f"\nAverage Network Risk Score: {round(average_risk, 3)}")
