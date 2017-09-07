from unittest import TestCase, mock

from djmodel_filler import ModelFiller
from djmodel_filler.utils import xmlparser


class TestDMapper(TestCase):

    def test_only_exist_keys(self):
        MAP_STRUCTURE = {
            'name': {'path': '/title'},
        }

        # dirty hack that helps with mocking Model.objects.create()
        # and can store send objects in store
        class DJObject(object):
            store = []
            def create(self, **kwargs):
                self.store.append(kwargs)

        model = mock.MagicMock
        model.objects = DJObject()

        # ModelFiller need to initialize with django model
        mf = ModelFiller(model)

        # I provide only one data parser - xmlparser
        # but you`re free to do your own, just check that its return data as python dict / list mixed nodes
        data = xmlparser('test_source.xml')
        mf.transfer_data(data, MAP_STRUCTURE, '/feed/events/event')

        self.assertTrue(isinstance(model.objects.store, list))
        self.assertTrue(len(model.objects.store), len(data))