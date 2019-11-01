
import os

pngPicArr = set() #所有的png图片名字
mFilesArr = [] # 所有的.m文件

absolutePath = os.environ['PWD']

print('开始检测项目中的图片……')

def findPngFilesByModuleDirName(dirName) :
	if os.path.isdir(dirName) :
		for subName in os.listdir(dirName):
			findPngFilesByModuleDirName(dirName+'/'+subName)
	elif os.path.isfile(dirName) :
		subfix = os.path.splitext(dirName)[1]
		if subfix == '.png':
			filePath = os.path.split(dirName)[1]
			fileName = filePath.replace('@2x.png','')
			fileName = fileName.replace('@3x.png','')
			fileName = fileName.replace('.png','')
			pngPicArr.add(fileName)
		elif subfix == '.m':
			mFilesArr.append(dirName)

for name in os.listdir(absolutePath):
	print('正在检测模块：'+name)
	findPngFilesByModuleDirName(absolutePath+'/'+name)

print('检测项目中的图片完成')

totalPngCount = len(pngPicArr)

if totalPngCount <= 0:
	print('没有找到图片')
	exit()

print('总共找到了'+str(totalPngCount)+'个图片')
print('请耐心等待，正在校验哪些图片未使用……')

totalFilesCount = len(mFilesArr)
index = 1
for file in mFilesArr:
	try:
		f = open(file, 'r',encoding='utf-8')
		content = f.read()
	except Exception as e:
		continue
	finally:
		if f:
			f.close()

	tempArr = []
	for picName in pngPicArr:
		if content.find(picName) != -1:
			tempArr.append(picName)

	for object in tempArr:
		pngPicArr.remove(object)

	print("\r[{0}] {1} / {2} ".format('当前进度',str(index),str(totalFilesCount)),end='',flush=True)
	index +=1

print('\n检测完成')

print('未使用的图片可能有:')
print(pngPicArr)