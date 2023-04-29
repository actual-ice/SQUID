import bluetooth

print("Performing BLE inquiry...")
nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

for addr, name in nearby_devices:
    print(addr, name)