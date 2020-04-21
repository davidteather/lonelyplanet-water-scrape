with open("reformat.csv", 'w+') as obj:
    print('Created')

with open("data.csv", 'r', encoding="utf-8") as inp:
    
    lines = inp.readlines()

    with open("reformat.csv", 'a', encoding="utf-8") as output:
        output.write("City,Link,Content\n")
        for x in range(1,int(lines[0].replace("\n", ""))):
            # iterate over lines
            output.write(lines[x].split("\t")[0].replace(",", "%2C") + " " + lines[x].split("\t")[1].split("/")[0].title().replace(",", "%2C") + "\n")
        