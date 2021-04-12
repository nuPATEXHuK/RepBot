import requests
import random

revolver_drum = [1, 1, 1, 1, 0, 1]
while True:
    bullet = random.randint(0, 5)
    print(bullet)
    print(revolver_drum)
    if (revolver_drum[bullet] != 0):
        continue
    else:
        revolver_drum[bullet] = 1
        break
print("Итог:")
print(revolver_drum)