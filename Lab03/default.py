import numpy as np

def calculate_weighted_energy_consumption(energy_matrix: np.ndarray, weight_vector: np.ndarray) -> float:
    if energy_matrix.shape[0] != weight_vector.shape[0]:
        raise ValueError("Кількість вузлів у матриці і векторі ваг не збігається.")

    # Перемноження кожного вузла на його вагу
    weighted_matrix = energy_matrix * weight_vector[:, np.newaxis]

    # Повертаємо суму всіх енергоспоживань
    total_energy = np.sum(weighted_matrix)
    return total_energy

# 5 вузлів, 24 години
consumption = np.random.rand(5, 24) * 10  # випадкове споживання [0..10] кВт
weights = np.array([1.0, 0.9, 1.1, 0.8, 1.0])  # наприклад, коеф. ефективності

total = calculate_weighted_energy_consumption(consumption, weights)
print(f"Загальне скориговане споживання енергії: {total:.2f} кВт⋅год")

