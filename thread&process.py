import random
import time

from multiprocessing import Process
from multiprocessing import Lock as Lm
from multiprocessing import  Queue as Qm
from threading import Thread
from threading import Lock as Lt
from queue import Queue as Qt

class Student:

	def __init__(self,number, x, y, card):
		self.number = number
		self.x = x
		self.y = y
		self.card = card 



class Building():
	
	students = []
	list_big = []
	not_card = []
	biggest_bag = [0 , 0]
	max_x = 80
	max_y = 80

	def __init__(self, number, q, lock):
		self.number = number
		self.students = []
		self.q = q
		self.lock = lock


	def add(self, student):
		self.students.append(student)

	def delete(self):
		Building.students = []
		Building.list_big = []
		Building.not_card = []
		Building.biggest_bag = [0 , 0]

	def search(self):
		size = self.students[-1].x * self.students[-1].y
		if size > Building.biggest_bag[1]:
			Building.biggest_bag[0] = self.students[-1].number
			Building.biggest_bag[1] = size

		if self.students[-1].x > Building.max_x or self.students[-1].y > Building.max_y:
			Building.list_big.append(self.students[-1])
			print('Проверить студента под номером {0}, вошедший в корпус под номером {1}'.format(self.students[-1].number, self.number))

		if self.students[-1].card == False:
			Building.not_card.append(self.students[-1])
	
	def run(self):
		while(self.q.empty() == False):
			x = random.randint(5, 100)
			y = random.randint(5, 100)
			card = random.choice([True, False])
			self.lock.acquire()
			try:
				if self.q.empty():
					break
				a = self.q.get()
				st = Student(a, x, y, card)
				self.add(st)
				self.search()
			finally:
				self.lock.release()
			time.sleep(0.1)


class ThreadF(Building, Thread):
	def __init__(self, number, q, lock):
		Building.__init__(self, number, q, lock)
		Thread.__init__(self)  

class ProcessF(Building, Process):
	def __init__(self, number, q, lock):
		Building.__init__(self, number, q, lock)
		Process.__init__(self)  

if __name__ == '__main__':
	#Однопоточной
	print('----Однопоточная----')
	lt = Lt()
	qt = Qt()
	for i in range(1,101):
		qt.put(i)
	start_time = time.time()
	threads = []
	threads.append(ThreadF(1, qt, lt))
	threads[0].start()
	threads[0].join()
	time_one_thread = time.time() - start_time
	one_thread_big = threads[0].biggest_bag[0]
	list_not_one_thread = ''
	for item in threads[0].not_card:
		list_not_one_thread += str(item.number)
		list_not_one_thread += ' '
	threads[0].delete()

	#Многопоточная
	print()
	print('----Многопоточная----')
	lt = Lt()
	qt = Qt()
	for i in range(1,101):
		qt.put(i)
	start_time = time.time()
	threads = []
	for i in range(1, 4):
		threads.append(ThreadF(i, qt, lt))

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()
	time_thread = time.time() - start_time
	thread_big = threads[0].biggest_bag[0]
	list_not_thread = ''
	for item in threads[0].not_card:
		list_not_thread += str(item.number)
		list_not_thread += ' '
	threads[0].delete()
	
	#Многопроцессная
	print()
	print('----Многопроцессная----')
	lm = Lm()
	qm = Qm()
	for i in range(1,101):
		qm.put(i)
	start_time = time.time()
	processes = []
	for i in range(1, 4):
		processes.append(ProcessF(i, qm, lm))

	for process in processes:
		process.start()

	for process in processes:
		process.join()
	qm.close()
	time_multi = time.time() - start_time
	process_big = threads[0].biggest_bag[0]
	print('----Однопоточная----')
	print('Время выполнения программы: {0}'.format(time_one_thread))
	print('Студент с самой большой сумкой: {0}'.format(one_thread_big))
	print('Студенты без студенческого билета: ' + list_not_one_thread)
	print('')
	print('----Многопоточная----')
	print('Время выполнения программы: {0}'.format(time_thread))
	print('Студент с самой большой сумкой: {0}'.format(thread_big))
	print('Студенты без студенческого билета: ' + list_not_thread)
	print('')
	print('----Многопроцессная----')
	print('Время выполнения программы: {0}'.format(time_multi))
	print('')