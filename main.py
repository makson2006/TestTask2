from aiohttp import web
import logging
from models import database, Device, ApiUser, Location
from playhouse.shortcuts import model_to_dict

logging.basicConfig(level=logging.INFO)


async def create_device(request):
    try:
        data = await request.json()
        logging.info(f"Отримані дані для створення пристрою: {data}")
        device = Device.create(**data)
        return web.json_response(model_to_dict(device))
    except Exception as e:
        logging.error(f"Помилка при створенні пристрою: {e}")
        return web.json_response({'error': str(e)}, status=500)

async def read_device(request):
    try:
        device_id = int(request.match_info['id'])
        device = Device.get(Device.id == device_id)
        return web.json_response(model_to_dict(device))
    except Exception as e:
        logging.error(f"Помилка при читанні пристрою: {e}")
        return web.json_response({'error': str(e)}, status=500)

async def update_device(request):
    try:
        device_id = int(request.match_info['id'])
        data = await request.json()  # Дочекатися результату
        Device.update(**data).where(Device.id == device_id).execute()
        device = Device.get(Device.id == device_id)
        return web.json_response(model_to_dict(device))
    except Exception as e:
        logging.error(f"Помилка при оновленні пристрою: {e}")
        return web.json_response({'error': str(e)}, status=500)

async def delete_device(request):
    try:
        device_id = int(request.match_info['id'])
        Device.delete().where(Device.id == device_id).execute()
        return web.json_response({'status': 'deleted'})
    except Exception as e:
        logging.error(f"Помилка при видаленні пристрою: {e}")
        return web.json_response({'error': str(e)}, status=500)

async def check_db_connection(app):
    try:
        database.connect()
        database.create_tables([ApiUser, Location, Device], safe=True)
        logging.info("Підключення до бази даних успішне.")
    except Exception as e:
        logging.error(f"Помилка підключення до бази даних: {e}")
    finally:
        if not database.is_closed():
            database.close()

app = web.Application()
app.router.add_post('/device', create_device)
app.router.add_get('/device/{id}', read_device)
app.router.add_put('/device/{id}', update_device)
app.router.add_delete('/device/{id}', delete_device)

app.on_startup.append(check_db_connection)

if __name__ == '__main__':
    web.run_app(app, port=8080)
