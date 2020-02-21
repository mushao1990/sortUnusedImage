
import os

picTypeStr = input('请输入要扫描的图片类型，类型之间以逗号隔开，如png,jpg\n如果不填，默认是扫描png和jpg图片，按enter键跳过\n')

picTypeArr = ['.png','.jpg']
if len(picTypeStr) > 0:
	tempPicArr = picTypeStr.split(',')
	if len(tempPicArr) > 0 :
		picTypeArr = ['.'+ x.lower() for x in tempPicArr]

scanFileStr = input('请输入要扫描的文件类型，类型之间以逗号隔开，如m,h\n如果不填，默认是扫描.m类型文件，按enter键跳过\n')

fileTypeArr = ['.m']
if len(scanFileStr) > 0 :
	tempFileArr = scanFileStr.split(',')
	fileTypeArr = ['.'+ x.replace(' ','').lower() for x in tempFileArr]

allPicArr = set() #所有的png图片名字
allFilesArr = [] # 所有的文件

absolutePath = os.environ['PWD']

print('开始检测原生项目中的图片……')

def findPngFilesByModuleDirName(dirName) :
	if os.path.isdir(dirName) :
		for subName in os.listdir(dirName):
			findPngFilesByModuleDirName(dirName+'/'+subName)
	elif os.path.isfile(dirName) :
		subfix = os.path.splitext(dirName)[1]
		if subfix in picTypeArr:
			filePath = os.path.split(dirName)[1]
			if subfix == '.png':
				fileName = filePath.replace('@2x.png','')
				fileName = fileName.replace('@3x.png','')
				fileName = fileName.replace(subfix,'')
				fileName = fileName.replace('_zx','')
				fileName = fileName.replace('_ty','')
				allPicArr.add(fileName)
			else:
				fileName = filePath.replace(subfix,'')
				fileName = fileName.replace('_zx','')
				fileName = fileName.replace('_ty','')
				allPicArr.add(fileName)
		elif subfix in fileTypeArr:
			allFilesArr.append(dirName)

for name in os.listdir(absolutePath):
	print('正在扫描模块：'+name)
	findPngFilesByModuleDirName(absolutePath+'/'+name)

print('完成扫描原生项目中的图片')

if len(allPicArr) <= 0:
	print('没有找到图片')
	exit()

print('\n总共找到了'+str(len(allPicArr))+'个图片\n')
print('请耐心等待，正在校验哪些图片原生项目未使用……')


def rmoveExistPicFromAllFilesArray() : #从数组里移除存在的图片名

	totalFilesCount = len(allFilesArr)
	index = 1
	for file in allFilesArr:
	    try:
	        f = open(file, 'r',encoding='utf-8')
	        content = f.read()
	    except Exception as e:
	        continue
	    finally:
	        if f:
	            f.close()

	    tempArr = []
	    for picName in allPicArr:
	        if content.find(picName) != -1:
	            tempArr.append(picName)

	    for object in tempArr:
	        allPicArr.remove(object)

	    print("\r[{0}] {1} / {2} ".format('当前进度',str(index),str(totalFilesCount)),end='',flush=True)
	    index +=1	

def findFilesByModuleDirName(dirName,fileLastP) :
	dirName = dirName.replace(' ','')
	if os.path.isdir(dirName):
		for subName in os.listdir(dirName):
			findFilesByModuleDirName(dirName+'/'+subName,fileLastP)
	elif os.path.isfile(dirName) :
		subfix = os.path.splitext(dirName)[1]
		if subfix in fileLastP:
			allFilesArr.append(dirName)

rmoveExistPicFromAllFilesArray()
print('\n当前未使用图片为：'+str(len(allPicArr))+'个')
print('\n当前目录未使用图片已经扫描完成')


while True:
	otherPath = input('\n是否需要检测其他原生模块使用了以上的图片,如不需要检测，按enter键结束。\n如需检测，请输入其他模块文件夹路径：')
	if len(otherPath) > 0:
		allFilesArr = []
		findFilesByModuleDirName(otherPath,fileTypeArr)
		rmoveExistPicFromAllFilesArray()
		print('\n当前目录未使用图片已经扫描完成')
		print('\n当前未使用图片为：'+str(len(allPicArr))+'个')
	else:
		break

print('\n原生检测完成')

while True:
	rnPath = input('\n有些原生未使用图片可能在RN项目中使用，如不需要检测，按enter键结束。\n如需检测，请输入RN项目文件路径：')
	if len(rnPath) <= 0 :
		break
	else :
		allFilesArr = []
		findFilesByModuleDirName(rnPath,['.js'])
		rmoveExistPicFromAllFilesArray()
		print('\n当前目录未使用图片已经扫描完成')
		print('\n当前未使用图片为：'+str(len(allPicArr))+'个')

print('检测完成')
print('总共找到了'+str(len(allPicArr))+'个图片')
print('未使用的图片可能有：\n%s \n请谨慎删除'%allPicArr)

