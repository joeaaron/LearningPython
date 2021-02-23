#coding:utf-8
import time
from sys import argv
script ,filename = argv
print ("the input file name is:%r." %filename)

start = time.time()
print ("open the file...")
file = open(filename,"r+")
count = 0
#统计源文件的点数
for line in file:
    count=count+1
print ("size is %d" %count)
file.close()

#output = open("out.pcd","w+")
f_prefix = filename.split('.')[0]
output_filename = '{prefix}.pcd'.format(prefix=f_prefix)
output = open(output_filename,"w+")

list = ['# .PCD v.5 - Point Cloud Data file format\n','VERSION .5\n','FIELDS x y z\n','SIZE 4 4 4\n','TYPE F F F\n','COUNT 1 1 1\n']

output.writelines(list)
output.write('WIDTH ') #注意后边有空格
output.write(str(count))
output.write('\nHEIGHT')
output.write(str(1))  #强制类型转换，文件的输入只能是str格式
output.write('\nPOINTS ')
output.write(str(count))
output.write('\nDATA ascii\n')
file1 = open(filename,"r")
all = file1.read()
output.write(all)
output.close()
file1.close()

end = time.time()
print ("run time is: ", end-start)