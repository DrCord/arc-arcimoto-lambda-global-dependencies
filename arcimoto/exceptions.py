__all__ = [
    'ArcimotoException',
    'ArcimotoHighAlertException',
    'ArcimotoAlertException',
    'ArcimotoFirmwareAlertException',
    'ArcimotoManufacturingAlertException',
    'ArcimotoNetworkAlertException',
    'ArcimotoOrdersAlertException',
    'ArcimotoREEFAlertException',
    'ArcimotoReplicateAlertException',
    'ArcimotoServiceAlertException',
    'ArcimotoTelemetryAlertException',
    'ArcimotoYRiskAlertException',
    'ArcimotoPermissionError',
    'ArcimotoArgumentError',
    'ArcimotoNotFoundError',
    'ArcimotoNoStepUnrollException'
]


class ArcimotoException(Exception):
    def __init__(self, message, source=None, data={}):
        self.message = message
        self.data = data
        self.source = source
        self.channel = None


class ArcimotoHighAlertException(ArcimotoException):
    pass


class ArcimotoAlertException(ArcimotoException):
    pass


class ArcimotoFirmwareAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'firmware'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoManufacturingAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'manufacturing'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoNetworkAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'network'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoOrdersAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'orders'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoREEFAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'reef'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoReplicateAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'replicate'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoServiceAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'service'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoTelemetryAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'telemetry'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoYRiskAlertException(ArcimotoException):
    def __init__(self, *args, **kwargs):
        self.channel = 'yrisk'
        super().__init__(self, *args, **kwargs)

    pass


class ArcimotoPermissionError(ArcimotoException):
    pass


class ArcimotoArgumentError(ArcimotoException):
    pass


class ArcimotoNotFoundError(ArcimotoException):
    pass


class ArcimotoNoStepUnrollException(ArcimotoException):
    pass
