with open ('/home/tyf/Desktop/5q4e.pdb','r') as f1:
    order = 1
    base_path = '/home/tyf/Desktop'
    new_pdb = base_path + str(order) + ".pdb"
    f2 = open(new_pdb,'a+')
    for line in f1:
        line_tag =line[:6].strip()
        if line_tag == 'ATOM':
            line_order =line[:6] + '%5s'%str(order) + line[11:]
            order += 1
            f2.write(line_tag)
        elif line_tag == 'END':
            f2.write(line)
            break
        else:
            f2.write(line)


