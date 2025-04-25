from sandwich.SandwichBuilder import SandwichBuilder

if __name__ == "__main__":
    builder = SandwichBuilder()
    sandwich1 = (builder.addBread()
                 .addMeat()
                 .addLettuce()
                 .addTomato())
    print(sandwich1.sandwich._parts)