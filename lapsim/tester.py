import lapsim

best_time = 100
best_speed = 0
for speed in range(1, 90):
    time = lapsim.main(speed)
    if time < best_time:
        best_time = time
        best_speed = speed

print(f"Best time was {best_time} with a top speed of {best_speed}")