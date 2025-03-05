print("==================")
print("Area Calculator 📐 - By Spestly")
print("==================")

print("1) Triangle")
print("2) Rectangle")
print("3) Square")
print("4) Circle")
print("5) Quit")

total = 0
choice = int(input("Which shape:"))

if choice == 1:
    base = float(input("Enter base:"))
    height = float(input("Enter height:"))
    total = 0.5 * base * height
    print("Area of triangle:", total)
elif choice == 2:
    length = float(input("Enter length:"))
    width = float(input("Enter width:"))
    total = length * width
    print("Area of rectangle:", total)
elif choice == 3:
    side = float(input("Enter side:"))
    total = side * side
    print("Area of square:", total)
elif choice == 4:
    radius = float(input("Enter radius:"))
    total = 3.14159 * radius * radius
    print("Area of circle:", total)
elif choice == 5:
    print("Goodbye")
