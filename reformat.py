with open("reformat.csv", 'w+') as obj:
    print('Created')

with open("cities.csv", 'r') as inp:
    
    lines = inp.readlines()

    with open("reformat.csv", 'a') as output:
        output.write("City,Link,Content\n")
        for x in range(1,len(lines)):
            # iterate over lines
            output.write(lines[x].split(",")[0] + " " + lines[x].split(",")[1].split("/")[3].title() + "," + lines[x].split(",")[1] + "," + lines[x].split(",")[2].replace("\n","") + "\n")
        