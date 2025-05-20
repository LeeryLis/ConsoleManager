import random
import numpy as np


class MathFuncs:
    def sum_func(self, *numbers: int) -> int:
        return sum(numbers)

    def generate_random_numbers_uniform(self, count: int, min_value: int, max_value: int) -> list[int] | ValueError:
        if count <= 0:
            raise ValueError("Количество чисел должно быть положительным")

        return [int(round(random.uniform(min_value, max_value))) for _ in range(count)]

    def generate_random_numbers_normal(self, count: int, mean: int, std_dev: int) -> list[int] | ValueError:
        if count <= 0:
            raise ValueError("Количество чисел должно быть положительным")

        return [int(value) for value in np.random.normal(mean, std_dev, count)]

    def generate_random_numbers_exponential(self, count: int, scale: float) -> list[int] | ValueError:
        if count <= 0:
            raise ValueError("Количество чисел должно быть положительным")

        return [int(value) for value in np.random.exponential(scale, count)]
