class Passenger:
	def __init__(self, weight):
		self.weight = weight


class Taxi:
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.busy = False

	def make_busy(self):
		self.busy = True

	def make_free(self):
		self.busy = False

class FreightTaxi(Taxi):
	car = 'Freight'
	quantity = 2
	weight = 'any'
	cost = 50

	def __init__(self, name, number):
		super().__init__(name, number)

class LightTaxi(Taxi):
	car = 'Light'
	quantity = 4
	weight = 50
	cost = 30

	def __init__(self, name, number):
		super().__init__(name, number)

class CallTaxi():
	lcars = []
	fcars = []
	
	def __init__(self, distance, passengers = [], lcars = [], fcars = []):
		self.passengers = passengers
		self.distance = distance
		CallTaxi.lcars += lcars
		CallTaxi.fcars += fcars

	def addpass(self, passenger):
		self.passengers.append(passenger)

	def delpass(self, passenger):
		try:
			self.passengers.remove(passenger)
		except:
			print('Удалить пассажира не удалось')

	def addcar(self, lcars = [], fcars = []):
		CallTaxi.lcars += lcars
		CallTaxi.fcars += fcars

	def weight(self):
		weight = 0
		for item in self.passengers:
			weight += item.weight
		return weight

	def printcar(self, car, cost):
		print('Имя водителя: {0}\nНомер машины: {1}\nТип транспортного средства: {2}\nСтоимость поездки: {3}\n'.format(car.name, car.number, car.car, cost))

	def reservation(self):
		length = len(self.passengers)
		for car in CallTaxi.lcars:
			if car.busy == False and length<=car.quantity and self.weight()<=car.weight:
				car.make_busy()
				self.printcar(car, self.distance*car.cost)
				return car
		for car in CallTaxi.fcars:
			if car.busy == False and length<=car.quantity:
				car.make_busy()
				self.printcar(car, self.distance*car.cost)
				return car
		print('\nНет доступных машин\n')



st1 = Passenger(50)
st2 = Passenger(15)
st3 = Passenger(15)

lt1 = LightTaxi('Константин', 'K467AK')
lt2 = LightTaxi('Виталий', 'Е3272KO')

ft1 = FreightTaxi('Роман', 'K3829JC')
ft2 = FreightTaxi('Владимир', 'C1200TX')

call = CallTaxi(10, [st1, st2], lcars=[lt1, lt2], fcars =[ft1, ft2])

call.reservation()
call.reservation()
ft2.busy = False
call.reservation()

call = CallTaxi(30, [st1, st2, st3])
call.reservation()
call = CallTaxi(20, [st1])
call.reservation()