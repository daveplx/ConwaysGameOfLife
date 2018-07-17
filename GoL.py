from random import randint
from time import sleep
from subprocess import call
from os import system, path, utime
from copy import deepcopy
from sys import argv
import getopt

def printMatrix(matrix):
	for line in matrix:
		print(line)

def populateMatrix(matrix):
	for i in range(0,len(matrix)):
		for j in range(0, len(matrix[i])):
			matrix[i][j] = randint(0, 1)
	
def createMatrix(size=20):
	matrix = [None] * size
	for i in range(0, size):
		matrix[i] = [None] * size
	return matrix
		
def getMatrixFieldValue(matrix, x, y):
	return matrix[x][y]
	
def setMatrixFieldValue(matrix, x, y, value):
	matrix[x][y] = value
		
def getSurroundingFieldSum(matrix, x, y):
	sum = 0
	for i in range(-1, 2):
		for j in range(-1, 2):
			if not ( i == 0 and j == 0):
			
				if x+i < 0 or x+i > len(matrix)-1:
					continue
					
				if y+j < 0 or y+j > len(matrix[x])-1:
					continue
					
				try:
					currVal = getMatrixFieldValue(matrix, x+i, y+j)
					sum = sum + currVal	
				except Exception as e:
					print('Error: {}'.format(e))
	return sum
			
def updateField(matrix, x, y):
	v = getMatrixFieldValue(matrix, x, y)
	s = getSurroundingFieldSum(matrix, x, y)
	
	if (v == 0 and s == 3):
		return 1
	
	elif (v == 1 and 1 < s < 4):
		return 1
	
	else:
		return 0
		
def updateMatrix(matrix):
	n = createMatrix(len(matrix))
	
	for i in range(0, len(matrix)):
		for j in range(0, len(matrix[i])):
			n[i][j] = updateField(matrix, i, j)
	
	for i in range(0, len(matrix)):
		for j in range(0, len(matrix[i])):
			matrix[i][j] = n[i][j]
	
def tick(matrix):
	system('cls')
	updateMatrix(matrix)
	visualizeMatrix(matrix)
	sleep(tickSpeed)
	
def visualizeMatrix(matrix):
	for i in range(0, len(matrix)):
		for j in range(0, len(matrix[i])):
			if matrix[i][j] == 0:
				print(' ', end='')
			else:
				print('\u2588', end='')
		print()

def printHelp():
	print('This script will run \"Conway\'s Game of Life\". The following parameters are accepted:\n')
	print('\n\t[-h]\t\t--help\t\tshow this help')
	print('\n\t[-s] SIZE\t--size=SIZE\tDeclare the size of the base matrix')
	print('\n\t[-s] SIZE\t--size=SIZE\tDeclare the size of the base matrix')
	print('\n\t[-s] SIZE\t--size=SIZE\tDeclare the size of the base matrix')
	print('\n\t[-s] SIZE\t--size=SIZE\tDeclare the size of the base matrix')
	print('\n\t[-s] SIZE\t--size=SIZE\tDeclare the size of the base matrix')
	

def yesNoCheck():
	userInput = input('Are you sure you want to continue? [y]es / [n]o / [a]bort\n> ')
	try:
		if str(userInput).lower() in ('a', 'abort'):
			exit(0)
		if str(userInput).lower() in ('y', 'ye', 'yes'):
			return True
		else:
			return False
	except Exception as e:
		print('Error: {}'.format(e))
		exit(1)
'''
size1 = 40
m1 = createMatrix(size1)
populateMatrix(m1)
m2 = deepcopy(m1)
printMatrix(m1)
#a = randint(0, len(m1)-1)
#print('a: {}'.format(a))
#b = randint(0, len(m1[a])-1)
#print('b: {}'.format(b))
#print('m1 {}|{}: {}'.format(a, b, getMatrixFieldValue(m1, a, b)))
#print('m1 sum of fields surrounding {}|{}: {}'.format(a, b, getSurroundingFieldSum(m1, a, b)))
while(True):
	try:
		tick(m1)
	except KeyboardInterrupt:
		break
print('-----Seed-----')
printMatrix(m2)
print(argv)
'''

unixOptions = 'hs:rt:i:o:k:'
gnuOptions = ['help', 'size=', 'random', 'tickspeed=', 'infile=', 'outfile=', 'keepseed=']

argumentList = argv[1:]
size = None
populateRandom = True
tickSpeed = .1
inFile = None
outFile = None
keepSeed = None

try:
	arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
	print(str(err))
	exit(2)
	
for currentArgument, currentValue in arguments:
	if currentArgument in ('-h', '--help'):
		printHelp()
		exit(0)
	elif currentArgument in ('-s', '--size'):
		try:
			size = int(currentValue)
		except Exception as e:
			print('Error: {}'.format(e))
			printHelp()
			exit(1)
	elif currentArgument in ('-r', '--random'):
		populateRandom = True
	elif currentArgument in ('-t', '--tickspeed'):
		try:
			tickSpeed = float(currentValue)
		except Exception as e:
			print('Error: {}'.format(e))
			printHelp()
			exit(1)
	elif currentArgument in ('-i', '--infile'):
		if size != None:
			print('Size and input file defined, will ignore size and use input file\'s matrix size instead')
			if not yesNoCheck():
				exit(0)
			size = None
		inFile = currentValue
		if not path.isfile(inFile):
			print('Could not find input file and will use random instead: \'{}\''.format(inFile))
			if not yesNoCheck():
				exit(0)
	elif currentArgument in ('-o', '--outfile'):
		outFile = currentValue
		if path.isfile(outFile):
			print('Output file already exists and will be overwritten: \'{}\''.format(outFile))
			if not yesNoCheck():
				exit(0)
		else:
			try:
				with open(outFile, 'w') as f:
					f.close()
			except Exception as e:
				print('Error: {}'.format(e))
				exit(1)
	elif currentArgument in ('-k', '--keepseed'):
		keepSeed = currentValue
		if path.isfile(keepSeed):
			print('Seed output file already exists and will be overwritten: \'{}\''.format(keepSeed))
			if not yesNoCheck():
				exit(0)
		else:
			try:
				with open(keepSeed, 'w') as f:
					f.close()
			except Exception as e:
				print('Error: {}'.format(e))
				exit(1)

if size == None:
	matrix = createMatrix()
else:
	matrix = createMatrix(size)

if inFile != None:
	with open(inFile, 'r') as f:
		for i, l in enumerate(f):
			pass
		inFileSize = i  + 1
	matrix = createMatrix(inFileSize)
	with open(inFile, 'r') as f:
		count = 0
		for line in f:
			inFileArray = line.split(',')
			for i in range(0, len(inFileArray)):
				inFileArray[i] = int(str(inFileArray[i]).strip().replace('[', '').replace(']', ''))
			matrix[count] = inFileArray
			count = count + 1
	populateRandom = False

if populateRandom:
	populateMatrix(matrix)

initial_matrix = deepcopy(matrix)
if keepSeed != None:
	try:
		with open(keepSeed, 'w') as f:
			for line in initial_matrix:
				f.write(str(line) + '\n')
	except Exception as e:
		print('Error: {}'.format(e))
while(True):
	try:
		tick(matrix)
	except KeyboardInterrupt:
		break
print('---------- seed ----------')
printMatrix(initial_matrix)
if not (keepSeed == None and inFile == None):
	exit(0)
print('You can save this seed if you want, answer yes')
if yesNoCheck():
	saveSeed = input('Please enter the path where you want to save the seed\n> ')
	if path.isfile(saveSeed):
		print('File already exists and will be overwritten: \'{}\''.format(saveSeed))
		if not yesNoCheck():
			exit(0)
		try:
			with open(saveSeed, 'w') as f:
				for line in initial_matrix:
					f.write(str(line) + '\n')
			print('Seed saved as {}'.format(saveSeed))
		except Exception as e:
			print('Error: {}'.format(e))
			exit(1)