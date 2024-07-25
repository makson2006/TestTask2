import unittest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from unittest.mock import patch, MagicMock
from models import Device, ApiUser, Location
from main import app, create_device, update_device, read_device


class TestDeviceAPI(AioHTTPTestCase):
    async def get_application(self, deletee_device=None):
        app = web.Application()
        app.router.add_post('/device', create_device)
        app.router.add_get('/device/{id}', read_device)
        app.router.add_put('/device/{id}', update_device)
        app.router.add_delete('/device/{id}', deletee_device)
        return app

    @unittest_run_loop
    @patch('models.Device.create')
    async def test_create_device(self, mock_create):
        mock_create.return_value = MagicMock(id=1, name='Test Device', type='Sensor', login='test_login', password='test_password', location_id=1, api_user_id=1)
        data = {'name': 'Test Device', 'type': 'Sensor', 'login': 'test_login', 'password': 'test_password', 'location': 1, 'api_user': 1}
        resp = await self.client.post('/device', json=data)
        assert resp.status == 200
        response_data = await resp.json()
        assert 'name' in response_data
        assert response_data['name'] == 'Test Device'

    @unittest_run_loop
    @patch('models.Device.get')
    async def test_read_device(self, mock_get):
        mock_device = MagicMock(id=1, name='Test Device', type='Sensor', login='test_login', password='test_password', location_id=1, api_user_id=1)
        mock_get.return_value = mock_device
        resp = await self.client.get('/device/1')
        assert resp.status == 200
        response_data = await resp.json()
        assert 'name' in response_data
        assert response_data['name'] == 'Test Device'

    @unittest_run_loop
    @patch('models.Device.update')
    @patch('models.Device.get')
    async def test_update_device(self, mock_get, mock_update):
        mock_device = MagicMock(id=1, name='Updated Device', type='Sensor', login='updated_login', password='updated_password', location_id=1, api_user_id=1)
        mock_get.return_value = mock_device
        data = {'name': 'Updated Device', 'type': 'Sensor', 'login': 'updated_login', 'password': 'updated_password', 'location': 1, 'api_user': 1}
        resp = await self.client.put('/device/1', json=data)
        assert resp.status == 200
        response_data = await resp.json()
        assert 'name' in response_data
        assert response_data['name'] == 'Updated Device'

    @unittest_run_loop
    @patch('models.Device.delete')
    async def test_delete_device(self, mock_delete):
        resp = await self.client.delete('/device/1')
        assert resp.status == 200
        response_data = await resp.json()
        assert response_data['status'] == 'deleted'

if __name__ == '__main__':
    unittest.main()
