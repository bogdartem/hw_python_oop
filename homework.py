class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float
            ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    # Отформатировать до тысячных долей
    # (до третьего знака после запятой).
    def get_message(self) -> str:
        # Возвращаем сообщение методом.
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    # 1 шаг в метрах, один гребок при плавании — 1.38 метра.
    # Переопределить в методе при гребке.
    LEN_STEP: float = 0.65
    H_IN_MIN: int = 60       # константа перевода часов в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        # Передали входные данные в селф.
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        # Передаём в переменную расстояние по расчетной формуле.
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Переменная для ср.ск-ти. Расчёт по формуле.
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Не трогаем-с, меняем в дочерних классах.
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM
            * self.duration * self.H_IN_MIN
            )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KOEF_CAL_WALKING_1 = 0.035
    KOEF_CAL_WALKING_2 = 0.029
    HEIGH_IN_M = 100
    KMH_IN_MS = round(1000 / 3600, 3)

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.KOEF_CAL_WALKING_1
             * self.weight
             + ((self.get_mean_speed() * self.KMH_IN_MS)**2
                / (self.height / self.HEIGH_IN_M))
                * self.KOEF_CAL_WALKING_2
                * self.weight)
            * self.duration
            * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    KOEF_CALORIES_1 = 1.1
    KOEF_CALORIES_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return (
            (self.get_mean_speed()
             + self.KOEF_CALORIES_1)
            * self.KOEF_CALORIES_2
            * self.weight
            * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
        }

    return workout_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
