import asyncio
import json

class EchoClient(asyncio.Protocol):

	def __init__(self, on_con_lost):
		self.on_con_lost = on_con_lost

	def connection_made(self, transport):
		self.transport = transport
		print('Установлено сеодинение')

	def connection_lost(self, exc):
		print('Сервер закрыл сеодинение')
		self.on_con_lost.set_result(True)

	def data_received(self, data):
		mes = json.loads(data)
		if (type(mes)==dict):
			menu = mes
			print('Получено меню:')

			for key, item in menu.items():
				print('№{} - {} {}р'.format(key, item[0], item[1]))

			list_order = []
			print('Составьте заказ.\nПример ввода данных: 2\nДля прекращения ввода введите "q"')
			while(True):  
				ch=False
				item = input('Введите номер бургера:')
				item = item.strip()
				if item == 'q':
					break
				if item.isdigit()==True:
					for key in menu.keys():
						if key==item:
							ch=True
							break
					if ch==True:
						list_order.append(item)
					else:
						print('Номера с таким бургером нет в меню')
				else:
					print('Не валидная строка')
			print('Ваш заказ:')
			for order in list_order:
				for key, item in menu.items():
					if key==order:
						print('№{} - {} {}р'.format(key, item[0], item[1]))

			self.transport.write(json.dumps(list_order).encode())
			print('Заказ отпрален на сервер')

		else:
			print('Сервер прислал стоимость вашего заказа: {}р'.format(mes))
			print('1-Заплатить, 2-Уйти\n')
			while(True):
				ch = input('Выбор:')
				if ch=='1' or ch=='2':
					break
			self.transport.write(json.dumps(ch).encode())
			print('Выбор отправлен на сервер')




async def main():

	loop = asyncio.get_running_loop()
	on_con_lost = loop.create_future()
	transport, protocol = await loop.create_connection(
		lambda: EchoClient(on_con_lost),
		'localhost', 8044)

	try:
		await on_con_lost
	finally:
		transport.close()


if __name__ == '__main__':
	asyncio.run(main())