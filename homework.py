from asyncio import constants
from turtle import distance
from typing_extensions import Self


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type:str,
                 duration:float,
                 distance:float,
                 speed:float,
                 calories:float ) -> None:
                self.training_type = training_type
                self.duration = "%.3f" % duration
                self.distance ="%.3f" % distance
                self.speed ="%.3f" % speed
                self.calories="%.3f" %calories
 
    def get_message(self)->str:
        message = (
                  f'Тип тренировки: {self.training_type}; '
                  f'Длительность: {self.duration} ч.; ' 
                  f'Дистанция: {self.distance} км; ' 
                  f'Ср. скорость: {self.speed} км/ч; ' 
                  f'Потрачено ккал: {self.calories}.' 
                  )
        return (message)          
                

class Training:
    """Базовый класс тренировки."""
    LEN_STEP:float = 0.65
    M_IN_KM:int = 1000
    MIN_IN_HOUR:int=60
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
        distance = ( self.action 
                    * self.LEN_STEP
                     / self.M_IN_KM )
        return distance
        
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_movement = (self.get_distance() / self.duration)
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
    LEN_STEP:float = 0.65
    M_IN_KM:int = 1000
    MIN_IN_HOUR:int=60
    def __init__(self, action: int, duration: float, weight: float) -> None:
         super().__init__(action, duration, weight)

    def get_distance(self) -> float:
         return super().get_distance()  

    def get_mean_speed(self) -> float:
         return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        calories =( ( coeff_calorie_1
                            * self.get_mean_speed()
                            - coeff_calorie_2)
                            * self.weight / self.M_IN_KM
                            * (self.duration*self.MIN_IN_HOUR) 
                    )
        return calories     


class SportsWalking(Training):
    LEN_STEP:float = 0.65
    M_IN_KM:int = 1000
    MIN_IN_HOUR:int=60
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height:float) -> None:
         super().__init__(action, duration, weight)
         self.height = height

    def get_distance(self) -> float:
         return super().get_distance()  

    def get_mean_speed(self) -> float:
         return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        coeff_calorie_3 = 2
        calories = float( (coeff_calorie_1
                     * self.weight
                     + (self.get_mean_speed()
                     **coeff_calorie_3
                     // self.height) 
                     * coeff_calorie_2 
                     * self.weight) 
                     * (self.duration*self.MIN_IN_HOUR) )
        return calories


class Swimming(Training):
    LEN_STEP = 1.38
    M_IN_KM:int = 1000
    """Тренировка: плавание."""
    def __init__(self, action: int,
                duration: float,
                weight: float,
                length_pool: float,
                count_pool: int) -> None:
         super().__init__(action, duration, weight)
         self.length_pool=length_pool
         self.count_pool=count_pool
    
    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        mean_speed=(self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration
                 )
        return mean_speed
 
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2 
        calories =  ( (self.get_mean_speed()
                     + coeff_calorie_1)
                     * coeff_calorie_2
                     * self.weight) 
        return calories  


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'RUN' : Running,
                     'SWM' : Swimming,
                     'WLK' : SportsWalking}
   # if workout_type is not training_type.keys:
   #     raise TypeError('Read_Package check error')
    return training_type[workout_type](*data)
    


def main(training: Training) -> None:
    """Главная функция."""
    info=training.show_training_info()
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

