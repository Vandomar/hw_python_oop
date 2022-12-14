from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {0}; '
                    'Длительность: {1} ч.; '
                    'Дистанция: {2} км; '
                    'Ср. скорость: {3} км/ч; '
                    'Потрачено ккал: {4}.')

    def get_message(self) -> str:
        return self.message.format(
            self.training_type,
            "%.3f" % self.duration,
            "%.3f" % self.distance,
            "%.3f" % self.speed,
            "%.3f" % self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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
        distance = (self.action
                    * self.LEN_STEP
                    / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_movement = self.get_distance() / self.duration
        return average_movement

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        show = InfoMessage(training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return show


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_CALORIE_1
                    * self.get_mean_speed()
                    - self.COEFF_CALORIE_2)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.MIN_IN_HOUR))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    COEFF_CALORIE_3: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = float(
            (
                self.COEFF_CALORIE_1
                * self.weight
                + (self.get_mean_speed()
                   ** self.COEFF_CALORIE_3
                   // self.height)
                * self.COEFF_CALORIE_2
                * self.weight) * (self.duration * self.MIN_IN_HOUR))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration
                      )
        return mean_speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed()
                     + self.COEFF_CALORIE_1)
                    * self.COEFF_CALORIE_2
                    * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'RUN': Running,
                     'SWM': Swimming,
                     'WLK': SportsWalking}
    if workout_type not in training_type:
        raise TypeError('Read_Package check error')
    else:
        return training_type[workout_type](*data)


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
