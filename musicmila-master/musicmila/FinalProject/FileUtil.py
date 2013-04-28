import os
import shutil


def getAllFileinDir(src):
	
	file_paths = []
	
	for root1,dirs,files in os.walk(src):
		#print root1
		if len(files) > 0:
			for f in files:
				path = os.path.join(root1,f)
				file_paths.append(path)
				#print dirs,files,path

	return file_paths
def main():
	print os.getcwd()
	src = os.getcwd()+'/fake'
	dest = os.getcwd()+'/real'
	print src
	
	#file_paths = [os.path.join(root1, d, f) 
	file_paths = getAllFileinDir(src)
	for path in file_paths:
    		print "File Path = ",path
		shutil.copy(path,dest)



if __name__ == '__main__':
    main()
