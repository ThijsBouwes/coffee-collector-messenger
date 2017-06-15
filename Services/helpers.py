HEIGHT_CAN = 40;
def calculatePercentage(value):
    if value > HEIGHT_CAN:
        return 0
    elif value >= HEIGHT_CAN:
        return 100
    else: 
        return round((HEIGHT_CAN-value)/HEIGHT_CAN*100+10, 2)