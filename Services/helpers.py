HEIGHT_CAN = 40

def calculatePercentage(value):
    if value > HEIGHT_CAN:
        return 0
    elif value >= HEIGHT_CAN:
        return 100
    else:
        # Calculate percentage of water in can + add 10% safety
        return round((HEIGHT_CAN-value)/HEIGHT_CAN*100+10, 2)
