from setuptools import setup, find_packages

setup(
    name='tm1602_exporter',
    version='0.0.3',
    description='Arris Touchstone tm1602 Collector for Prometheus',
    author='Aleks Bunin',
    author_email='github@compuix.com',
    license='Apache 2.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    data_files=[('', ['src/tm1602_exporter/tests/page.html'])],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'prometheus_client',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': ['tm1602_exporter=tm1602_exporter.__main__:main'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
