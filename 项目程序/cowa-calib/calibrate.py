import os, sys, shutil, threading, zipfile
import os.path  

def suffix( file, *suffixName ) :  
    array = map( file.endswith, suffixName )  
    if True in array :  
        return True  
    else :  
        return False  
def delOut(path):   
    for file in os.listdir( path ) :  
        targetFile = os.path.join( path, file )  
        if suffix( file, '.xml', '.bin', '.txt' ):  
            #print targetFile
            os.remove( targetFile )      
def calibrate(cam):
    os.system('bin\\calibrate.exe image %d'%cam)
def zip(path):
    f = zipfile.ZipFile('path.zip','w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            f.write(os.path.join(dirpath,filename))
    f.close()
    
if __name__ == '__main_1_':
    tasks = []
    for i in [1, 2, 4]:
        delOut('image/%d'%i)  
        task = threading.Thread(target=calibrate, args=(i,))
        task.start()
        tasks.append(task)
        
    for task in tasks:
        task.join()
#zip('image')
