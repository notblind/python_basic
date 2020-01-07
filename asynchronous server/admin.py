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
		menu = json.loads(data)
		print('Получено меню:')

		keys = []
		for key, item in menu.items():
			keys.append(key)
			print('№{} - {} {}р'.format(key, item[0], item[1]))
		print('Введите название и цену бургера')
		name = input('Название:')
		name.strip()
		while(True):
			cost = input('Цена:')
			cost.strip()
			if cost.isdigit():
				break
			print("Строка не валидна")
		key = keys[-1]
		menu[int(key)+1] = [name, int(cost)]
		self.transport.write(json.dumps(menu).encode())
		print('Меню отправлено на сервер')


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