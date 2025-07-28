import json
import random

brands = ["Honda", "Toyota", "Nissan", "BMW", "Tesla", "Ford", "Chevrolet", "Hyundai", "Kia", "Mazda"]
models = {
    "Honda": ["Accord", "Civic", "CR-V"],
    "Toyota": ["Camry", "Corolla", "RAV4"],
    "Nissan": ["Altima", "Rogue", "Sentra"],
    "BMW": ["320i", "330i", "X3"],
    "Tesla": ["Model 3", "Model Y","Cyber Truck"],
    "Ford": ["Fusion", "Escape", "Focus"],
    "Chevrolet": ["Malibu", "Equinox"],
    "Hyundai": ["Elantra", "Tucson"],
    "Kia": ["Optima", "Sportage"],
    "Mazda": ["Mazda3", "CX-5"]
}
descriptions = [
    "Clean title, low mileage, automatic, Bluetooth, rearview camera.",
    "One-owner, premium trim, sunroof, leather seats, lane assist.",
    "Certified pre-owned, all-wheel drive, touchscreen, spacious interior.",
    "Turbo engine, navigation system, excellent fuel economy, Apple CarPlay.",
    "Electric, fast charging, autopilot, tech-loaded interior."
]

inventory = []

for i in range(5):
    brand = random.choice(brands)
    model = random.choice(models[brand])
    year = random.randint(2015, 2023)
    title = f"{year} {brand} {model}"
    condition = random.choice(["Used","New"])
    price = f"${random.randint(12000, 35000)}"
    description = random.choice(descriptions)
    inventory.append({
        "title": title,
        "brand": brand,
        "model" : model,
        "year" : year,
        "comndition": condition,
        "price": price,
        "description": description
    })

with open("data/vehicle_inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print("✅ Simulated data saved to data/vehicle_inventory.json")
