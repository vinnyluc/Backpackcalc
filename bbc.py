things = {'зажигалка': 20, 'компас': 100, 'фрукты': 500, 'рубашка': 300,
        'термос': 1000, 'аптечка': 200, 'куртка': 600, 'бинокль': 400,
        'удочка': 1200, 'салфетки': 40, 'бутерброды': 820, 'палатка': 5500,
        'спальный мешок': 2250, 'жвачка': 10, 'карта': 5}
print("Введите вес в рюкзаке в кг:")
ves = int(input()) * 1000
sorted_things = dict(sorted(things.items(), key=lambda x: -x[1]))
count = 0
for k, v in sorted_things.items():
    if v <= ves:
        ves -= v
        print(k, "=", v, "гр., осталось в рюкзаке", ves, "гр.")
        count += 1
print("В рюкзаке", count, "вещей")
print("Осталось в рюкзаке", ves, "гр.")
print("Вес вещей в рюкзаке", sum(sorted_things.values()) - ves, "гр.")
print(sorted_things.values)