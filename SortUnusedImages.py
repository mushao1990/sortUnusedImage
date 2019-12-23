
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
				allPicArr.add(fileName)
		elif subfix in fileTypeArr:
			allFilesArr.append(dirName)

for name in os.listdir(absolutePath):
	print('正在扫描模块：'+name)
	findPngFilesByModuleDirName(absolutePath+'/'+name)

print('完成扫描原生项目中的图片')

totalPngCount = len(allPicArr)

if totalPngCount <= 0:
	print('没有找到图片')
	exit()

print('总共找到了'+str(totalPngCount)+'个图片')
print('请耐心等待，正在校验哪些图片原生项目未使用……')

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

print('\n原生检测完成')

rnPath = input('以上只是检测了原生项目，有些原生未使用图片可能在RN项目中使用，如不需要检测，按enter键结束。\n如需检测，请输入RN项目文件路径：')

print(rnPath)

if len(rnPath) <= 0 :
    print('未使用的图片可能有：\n%s \n请谨慎删除'%allPicArr)
    exit()

jsFileArr = []
def findJSFilesByModuleDirName(dirName) :
	dirName = dirName.replace(' ','')
	if os.path.isdir(dirName):
		for subName in os.listdir(dirName):
			findJSFilesByModuleDirName(dirName+'/'+subName)
	elif os.path.isfile(dirName) :
		subfix = os.path.splitext(dirName)[1]
		if subfix == '.js':
			jsFileArr.append(dirName)

findJSFilesByModuleDirName(rnPath)

totalFilesCount = len(jsFileArr)
index = 1
for file in jsFileArr:
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

print('检测完成')
print('总共找到了'+str(len(allPicArr))+'个图片')
print('未使用的图片可能有：\n%s \n请谨慎删除'%allPicArr)
