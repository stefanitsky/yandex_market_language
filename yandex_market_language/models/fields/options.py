class DeliveryOptionsField:
    _delivery_options = []

    @property
    def delivery_options(self):
        return self._delivery_options

    @delivery_options.setter
    def delivery_options(self, options):
        self._delivery_options = options if options else []


class PickupOptionsField:
    _pickup_options = []

    @property
    def pickup_options(self):
        return self._pickup_options

    @pickup_options.setter
    def pickup_options(self, options):
        self._pickup_options = options if options else []
