HEIGHT_CAN = 40


# determines how full the can is
def calculatePercentage(reading):
    return 100 if reading >= HEIGHT_CAN else round((HEIGHT_CAN - reading) / HEIGHT_CAN * 100)