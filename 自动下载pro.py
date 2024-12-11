score = input("Enter Score: ")
try:
    score = float(score)
    0< score < 1
    
except:

    print("error! please enter valid number")
    quit()
if score < 0.6:
    print("F")
elif score < 0.7:
    print("D")
elif score < 0.8:
    print("C")
elif score < 0.9:
    print("B")
else score < 1:
    print("A")