class Time:
    def __init__(self, day: int, month: int, year: int = 2024):
        if self._is_correct_time(day, month, year):
            self.day = day
            self.month = month
            self.year = year
        else:
            self.day = 1
            self.month = 1
            self.year = year

    def copy(self):
        return Time(self.day, self.month, self.year)

    def _is_correct_time(self, day: int, month: int, year: int) -> bool:
        if day < 1 or day > 31 or month < 1 or month > 12:
            return False
        
        days_in_month = self.days_month(month, year)
        if day > days_in_month: return False
        return True

    def _is_leap_year(self, year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def days_month(self, month: int, year: int) -> int:
        if month < 1 or month > 12: return 0
        
        if month in [4, 6, 9, 11]:
            return 30
        if month == 2:
            if self._is_leap_year(year):
                return 29
            else: return 28
        return 31
    
    def next_day(self, incr_day: int):
        new_day = self.day
        new_month = self.month
        
        if incr_day > 0 and new_day == 31 and new_month == 12:
            return self
        elif incr_day < 0 and new_day == 1 and new_month == 1:
            return self
        
        # Procesar incremento positivo
        if incr_day > 0:
            while incr_day > 0:
                days_in_current_month = self.days_month(new_month, self.year)
                days_remaining_in_month = days_in_current_month - new_day

                if incr_day <= days_remaining_in_month:
                    new_day += incr_day
                    incr_day = 0

                else:
                    incr_day -= (days_remaining_in_month + 1)
                    new_day = 1
                    new_month += 1
                    
                    if new_month > 12:
                        new_day = 31
                        new_month = 12
                        incr_day = 0
        
        # Procesar incremento negativo
        elif incr_day < 0:
            incr_day = abs(incr_day) 
            
            while incr_day > 0:

                if incr_day < new_day:
                    new_day -= incr_day
                    incr_day = 0
                else:
                    incr_day -= new_day
                    new_month -= 1
                    
                    if new_month < 1:
                        new_day = 1
                        new_month = 1
                        incr_day = 0
                    else:
                        new_day = self.days_month(new_month, self.year)
        
        self.day = new_day
        self.month = new_month
        return self
    
    def __str__(self):
        return f"{self.day:02d}/{self.month:02d}/{self.year}"