from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3} ч.; '
        'Дистанция: {distance:.3} км; '
        'Ср. скорость: {speed:.3} км/ч; '
        'Потрачено ккал: {calories:.3}.'
    )

    def get_message(self) -> str:
        """Функция возврата сообщения."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000.0
    LEN_STEP = 0.65
    H_IN_MIN = 60.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
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

    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Расчёт затраченных каллорий при беге."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.H_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KOEF_CAL_WALKING_1 = 0.035
    KOEF_CAL_WALKING_2 = 0.029
    HEIGH_IN_M = 100.0
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
        """Расчёт затраченных каллорий при спортивной ходьбе."""
        return (
            (
                self.KOEF_CAL_WALKING_1 * self.weight +
                (
                    (self.get_mean_speed() * self.KMH_IN_MS)**2
                    / (self.height / self.HEIGH_IN_M)
                )
                * self.KOEF_CAL_WALKING_2
                * self.weight
            )
            * self.duration * self.H_IN_MIN
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEPpyte = 1.38
    KOEF_CALORIES_1 = 1.1
    KOEF_CALORIES_2 = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Расчёт средней скорости при плавании."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self):
        """Расчёт затраченных каллорий при плавании."""
        return (
            (
                self.get_mean_speed()
                + self.KOEF_CALORIES_1
            )
            * self.KOEF_CALORIES_2
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать полученные от датчиков данные."""

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
