from uuid import uuid4


class VehicleTestHelper(object):

    vin = f'VIN-{uuid4()}'

    def __init__(self):
        super().__init__(self)
