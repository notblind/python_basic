import asyncio
import json

class echo(asyncio.Protocol):


	def connection_made(self, transport):

		peername = transport.get_extra_info('peername')
		print('Подключился клиент {}'.format(peername))
		transport.write(json.dumps(menu).encode())
		print('Для клиента {} отправлено меню'.format(peername))
		self.transport = transport

	def cost_order(self, list_order):
		cost = 0
		for item in list_order:
			for key, item_menu in menu.items():
				if item==key:
					cost = cost + item_menu[1]
		return cost



	def data_received(self, data):
		mes = json.loads(data)
		if type(mes)==list:
			list_order = mes
			print('Получен заказ от {}'.format(self.transport.get_extra_info('peername')))

			cost = self.cost_order(list_order)
			self.transport.write(json.dumps(cost).encode())
			print('Для клиента {} отправлена стоимость заказа'.format(self.transport.get_extra_info('peername')))
		elif type(mes)==dict:
			print('Получено новою меню от админа {} Закрываем с ним соединение'.format(self.transport.get_extra_info('peername')))
			global menu 
			menu = mes
			self.transport.close()
		else:
			if mes=='1':
				print('Клиент {} заплатил за заказ. Соединение с ним закрываем'.format(self.transport.get_extra_info('peername')))
			else:
				print('Клиент {} ушел. Соединение с ним закрываем'.format(self.transport.get_extra_info('peername')))
			self.transport.close()


name = 'menu.json'
menu = open(name, mode='r')
menu = json.load(menu)

async def main():
	loop = asyncio.get_running_loop()
	server = await loop.create_server( lambda: echo(), 'localhost', 8044)
	addr = server.sockets[0].getsockname()
	print(f'Сервер создан {addr}')

	async with server:
		await server.serve_forever()


if __name__ == '__main__':
	asyncio.run(main())