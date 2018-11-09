from setuptools import setup
setup(
    name='tesla_delivery_alert',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'TeslaDeliveryAlertSetup=TeslaDeliveryAlert:main'
        ]
    }
)