import numpy as np

with open ('./nuero_pdb.txt') as f:
    lines=f.readlines()
    length=len(lines)
    print length
    #num=np.random.randint(0,length,300)
    with open('./validation_name.txt','w+') as file:
        for i in range(length-60):
            a = i+50
            print i
            #i=int[i]
            #print i
            if a%50==0:
                file.write(lines[i])
