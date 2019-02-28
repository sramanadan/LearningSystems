
# coding: utf-8

# #star cubing
import pandas as pd
from sys import getsizeof
import timeit
import csv 


# cube representation
class TreeNode(object):
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"

        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'


# In[19]:

#generating cubes for test data
raw_data = []
cat_data_count={}
with open('test.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    categories = next(reader)
    for cat in categories:
        cat_data_count[cat]= []
    for row in reader:
        raw_data.append(tuple(row[:-1]))
        for entry in row:
            i = row.index(entry)
            curr_cat = categories[i]
            cat_data_count[curr_cat].append(entry)
print("Raw Data",raw_data)
print("Counts",cat_data_count)


count_data = {}
for key in cat_data_count:
    cat_data=cat_data_count[key]
    for entry in cat_data:
        if entry in count_data:
            count_data[entry] = count_data[entry]+1
        else:
            count_data[entry]=1
print (count_data)


star_data= []
for entry in raw_data:
    l=[]
    for t in entry:
        index = entry.index(t)
        if count_data[t]<2:
            l.append("*")
        else:
            l.append(t)
    star_data.append(tuple(l))
print(star_data)


star_data_count = {}
total_count = 0
for e in star_data:
    total_count=total_count+1
    if e in star_data_count:
        star_data_count[e]=star_data_count[e]+1
    else:
        star_data_count[e] =1
print(star_data_count)
print(total_count)
root = TreeNode(["root",total_count],[])
root.children=[]
cubes= []
curr=root;
for entry in star_data_count:
    #print("Current Entry: ", entry)
    curr=root
    index=0
    count = star_data_count[entry]
    while True:
        child_names = []
        for child in curr.children:
            child_names.append(child.value[0])
        #print("Current index and children:",index,child_names)

        if entry[index] in child_names: 
            found = child_names.index(entry[index])
            index=index+1
            curr.children[found].value[1] = curr.children[found].value[1]+count
            curr=curr.children[found]
        else:
            #print("To Add",entry[index:])
            for d in entry[index:]:
                curr.children.append(TreeNode([d,count],[]))
                curr=curr.children[-1]
            #print("-------------------------------------------")
            break
print(root)

cubes={}
for entry in star_data_count:
    index=0
    items_so_far=[]
    for e in entry:
        cat_left=categories[index+1:]
        result= []
        result.extend(items_so_far)
        result.extend(cat_left)
        result = tuple(result)
        if result in cubes:
            cubes[result]=cubes[result]+star_data_count[entry]
        else:
            cubes[result]=star_data_count[entry]
        items_so_far.append(e)
        index=index+1
print('cubes for test data:')
print(cubes)



# Generating cubes for Breast Cancer data


#preprocessing the data 
data=pd.read_csv("breastCancer.csv") #parsing
temptable = data

#applying iceberg conditions 
temptable.loc[temptable['size_uniformity'] >4 , "size_uniformity"] = "*" #iceberg conditions
temptable.loc[temptable['clump_thickness'] >4 , "clump_thickness"] = "*" #iceberg conditions

 
 
my_df = pd.DataFrame(temptable)
my_df.to_csv('out.csv', index=False, header=False)
newData = pd.read_csv("out.csv")
 
 
with open('out.csv', newline='') as file:
    reader = csv.reader(file)
    l = list(map(tuple, reader))
     
def pos_star(s): #returns the postion of stars in that row
    star=[]
    for k in range(0,len(s)-1):
        if s[k]=='*':
            star.append(k)
    return star
 
basetable=[[]] # table containing stars 
for row in range(0,len(l)-1):
    count = 0
    temp = pos_star(l[row])
    for k in range(0,len(l)-1):
        if pos_star(l[k])==temp:
           count=count+1
    basetable.append([l[row],count])
 
my_df = pd.DataFrame(basetable)
my_df.to_csv('basetable.csv', index=False, header=False)



total_size=0
star_data_count = {}
start_time = timeit.default_timer()
with open('basetable.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data = tuple(row[1:])
        if data in star_data_count:
            star_data_count[data] = star_data_count[data]+1
        else:
            star_data_count[data]=1
total_size=total_size+getsizeof(star_data_count)


root = TreeNode(["root",total_count],[])
root.children=[]
cubes= []
curr=root;
for entry in star_data_count:
    #print("Current Entry: ", entry)
    curr=root
    index=0
    count = star_data_count[entry]
    while True:
        child_names = []
        for child in curr.children:
            child_names.append(child.value[0])
        #print("Current index and children:",index,child_names)

        if entry[index] in child_names: 
            found = child_names.index(entry[index])
            index=index+1
            curr.children[found].value[1] = curr.children[found].value[1]+count
            curr=curr.children[found]
        else:
            #print("To Add",entry[index:])
            for d in entry[index:]:
                curr.children.append(TreeNode([d,count],[]))
                curr=curr.children[-1]
            #print("-------------------------------------------")
            break
print(root)
total_size=total_size+getsizeof(root)           
            
cubes={}
for entry in star_data_count:
    index=0
    items_so_far=[]
    for e in entry:
        cat_left=categories[index+1:]
        result= []
        result.extend(items_so_far)
        result.extend(cat_left)
        result = tuple(result)
        if result in cubes:
            cubes[result]=cubes[result]+star_data_count[entry]
        else:
            cubes[result]=star_data_count[entry]
        items_so_far.append(e)
        index=index+1
elapsed = timeit.default_timer() - start_time
total_size=total_size+getsizeof(cubes)


#writing cubes to new .csv file
csv_columns = ['cube', 'count']
with open('breast_cancer_cubes.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for key, value in cubes.items():
        #print(key,value)
        writer.writerow({'cube': key, 'count': value})
print("Elapsed Time: ",elapsed)
print("Total Size", total_size)
cubes


# 4 Dimensional data


total_size=0

raw_data = []
cat_data_count={}
start_time = timeit.default_timer()
with open('4-test.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    categories = next(reader)
    for cat in categories:
        cat_data_count[cat]= []
    for row in reader:
        raw_data.append(tuple(row[:-1]))
        for entry in row:
            i = row.index(entry)
            curr_cat = categories[i]
            cat_data_count[curr_cat].append(entry)
#print("Raw Data",raw_data)
#print("Counts",cat_data_count)


count_data = {}
for key in cat_data_count:
    cat_data=cat_data_count[key]
    for entry in cat_data:
        if entry in count_data:
            count_data[entry] = count_data[entry]+1
        else:
            count_data[entry]=1
#print (count_data)
total_size=total_size+getsizeof(count_data)

star_data= []
for entry in raw_data:
    l=[]
    for t in entry:
        index = entry.index(t)
        if count_data[t]<2:
            l.append("*")
        else:
            l.append(t)
    star_data.append(tuple(l))
#print(star_data)
total_size=total_size+getsizeof(star_data)

star_data_count = {}
total_count = 0
for e in star_data:
    total_count=total_count+1
    if e in star_data_count:
        star_data_count[e]=star_data_count[e]+1
    else:
        star_data_count[e] =1
#print(star_data_count)
#print(total_count)
total_size=total_size+getsizeof(star_data_count)




root = TreeNode(["root",total_count],[])
root.children=[]
cubes= []
curr=root;
for entry in star_data_count:
    #print("Current Entry: ", entry)
    curr=root
    index=0
    count = star_data_count[entry]
    while True:
        child_names = []
        for child in curr.children:
            child_names.append(child.value[0])
        #print("Current index and children:",index,child_names)

        if entry[index] in child_names: 
            found = child_names.index(entry[index])
            index=index+1
            curr.children[found].value[1] = curr.children[found].value[1]+count
            curr=curr.children[found]
        else:
            #print("To Add",entry[index:])
            for d in entry[index:]:
                curr.children.append(TreeNode([d,count],[]))
                curr=curr.children[-1]
            #print("-------------------------------------------")
            break
print(root)
total_size=total_size+getsizeof(root)



cubes={}
for entry in star_data_count:
    index=0
    items_so_far=[]
    for e in entry:
        cat_left=categories[index+1:]
        result= []
        result.extend(items_so_far)
        result.extend(cat_left)
        result = tuple(result)
        if result in cubes:
            cubes[result]=cubes[result]+star_data_count[entry]
        else:
            cubes[result]=star_data_count[entry]
        items_so_far.append(e)
        index=index+1
elapsed = timeit.default_timer() - start_time
total_size=total_size+getsizeof(cubes)


csv_columns = ['cube', 'count']
with open('4_dimension_cubes.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for key, value in cubes.items():
        #print(key,value)
        writer.writerow({'cube': key, 'count': value})
print("Elapsed Time:", elapsed)
print("Total_size Used",total_size) 

raw_data = []
cat_data_count={}
total_size=0
start_time = timeit.default_timer()
with open('5-test.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    categories = next(reader)
    for cat in categories:
        cat_data_count[cat]= []
    for row in reader:
        raw_data.append(tuple(row[:-1]))
        for entry in row:
            i = row.index(entry)
            curr_cat = categories[i]
            cat_data_count[curr_cat].append(entry)
#print("Raw Data",raw_data)
#print("Counts",cat_data_count)


count_data = {}
for key in cat_data_count:
    cat_data=cat_data_count[key]
    for entry in cat_data:
        if entry in count_data:
            count_data[entry] = count_data[entry]+1
        else:
            count_data[entry]=1

total_size=total_size+getsizeof(count_data)

star_data= []
for entry in raw_data:
    l=[]
    for t in entry:
        index = entry.index(t)
        if count_data[t]<2:
            l.append("*")
        else:
            l.append(t)
    star_data.append(tuple(l))
#print(star_data)
total_size=total_size+getsizeof(star_data)



star_data_count = {}
total_count = 0
for e in star_data:
    total_count=total_count+1
    if e in star_data_count:
        star_data_count[e]=star_data_count[e]+1
    else:
        star_data_count[e] =1
#print(star_data_count)
#print(total_count)
total_size=total_size+getsizeof(star_data_count)




root = TreeNode(["root",total_count],[])
root.children=[]
cubes= []
curr=root;
for entry in star_data_count:
    #print("Current Entry: ", entry)
    curr=root
    index=0
    count = star_data_count[entry]
    while True:
        child_names = []
        for child in curr.children:
            child_names.append(child.value[0])
        #print("Current index and children:",index,child_names)

        if entry[index] in child_names: 
            found = child_names.index(entry[index])
            index=index+1
            curr.children[found].value[1] = curr.children[found].value[1]+count
            curr=curr.children[found]
        else:
            #print("To Add",entry[index:])
            for d in entry[index:]:
                curr.children.append(TreeNode([d,count],[]))
                curr=curr.children[-1]
            #print("-------------------------------------------")
            break
print(root)
total_size=total_size+getsizeof(root)



cubes={}
for entry in star_data_count:
    index=0
    items_so_far=[]
    for e in entry:
        cat_left=categories[index+1:]
        result= []
        result.extend(items_so_far)
        result.extend(cat_left)
        result = tuple(result)
        if result in cubes:
            cubes[result]=cubes[result]+star_data_count[entry]
        else:
            cubes[result]=star_data_count[entry]
        items_so_far.append(e)
        index=index+1
elapsed = timeit.default_timer() - start_time
total_size=total_size+getsizeof(cubes)

csv_columns = ['cube', 'count']
with open('5_dimension_cubes.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for key, value in cubes.items():
        #print(key,value)
        writer.writerow({'cube': key, 'count': value})
print("Elapsed Time:",elapsed)
print("Total Size",total_size)
print(cubes)

