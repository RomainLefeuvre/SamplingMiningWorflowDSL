from bidouille.OperatorBuilder import OperatorBuilder

if __name__ == "__main__":
    builder = OperatorBuilder()
    test = builder.filterOperator("lang:JS").build()

    for operator in test:
        print(vars(operator)) # should print _constraint too -> attributes of subtypes and not only _attr of operator class