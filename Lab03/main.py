import numpy as np
from energy_calc import calculate_weighted_energy_consumption

# Дані
consumption = np.random.rand(5, 24) * 10
weights = np.array([1.0, 0.9, 1.1, 0.8, 1.0], dtype=np.float64)

# Виклик
total = calculate_weighted_energy_consumption(consumption, weights)
print(f"Оптимізоване споживання енергії: {total:.2f} кВт⋅год")
