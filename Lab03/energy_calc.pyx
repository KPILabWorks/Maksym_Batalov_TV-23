import numpy as np
cimport numpy as np

def calculate_weighted_energy_consumption(np.ndarray[np.float64_t, ndim=2] energy_matrix,
                                           np.ndarray[np.float64_t, ndim=1] weight_vector):
    cdef Py_ssize_t n = energy_matrix.shape[0]
    cdef Py_ssize_t t = energy_matrix.shape[1]
    cdef double total_energy = 0.0
    cdef Py_ssize_t i, j

    if weight_vector.shape[0] != n:
        raise ValueError("Кількість вузлів у матриці і векторі ваг не збігається.")

    for i in range(n):
        for j in range(t):
            total_energy += energy_matrix[i, j] * weight_vector[i]

    return total_energy
