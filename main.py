
import random
enter_list = []
package = []
package_list = []
for a in range(0,9):
    enter_list.append(random.randint(0,1))

print(enter_list)
current = 0
inpack = 0
for a in enter_list:
        if enter_list[current] == 1:
            package.append('111')
        elif enter_list[current] == 0:
            package.append('000')
        inpack +=1
        current += 1
        if inpack == 7:
            package_list.extend(package)
            package_list.append("")
            inpack = 0
            package.clear()



print(package_list)