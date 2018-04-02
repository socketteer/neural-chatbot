infile1 = #cmd line arg
infile2 = #cmd line arg

charset1 = set(open(infile1).read())
chars1 = ''.join(charset1)
print(len(chars1))
print(set(chars1))

charset2 = set(open(infile2).read())
chars2 = ''.join(charset2)
print(len(chars2))
print(set(chars2))

#print missing symbols to second file

print(set(chars1) ^ set(chars2))


