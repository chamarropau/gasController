class Step:
    def __init__(self, step_num, config, measurements):
        self._step_num = step_num
        self._config = config
        self._measurements = measurements

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"\n\nSTEP: {self._step_num} \n\t{str(self._config)}, \n\t{str(self._measurements)}"