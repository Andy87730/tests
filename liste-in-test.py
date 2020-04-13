x = {"one":"a","two":"b","three":"c","four":"d"}
y = ["two","2"]

if y[0] in x:
    print("ist drin")
    print(x.get(y[0]))
else:
    print("nicht drin")


    