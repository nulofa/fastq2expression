import pandas as pd

a = pd.DataFrame(data = {
    'Gene': ("A","B","C","D","E"),
    'Length': (100, 50, 25, 5, 1),
     'S1': (80, 10,  6,  3,   1),
     'S2': (20, 20, 10, 50, 400)
})

print(a.values)
print(a.columns)
print(a.axes)
# print(a.head(3))
