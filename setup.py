from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='uniflex_app_intents',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/uniflex',
    license='',
    author='Anatolij Zubow',
    author_email='zubow@tu-berlin.de',
    description='Application Intents Module',
    long_description='Implementation of application intents for different wireless technologies: i) IEEE 802.11 WiFi, ii) ...',
    keywords='wireless control',
    install_requires=[]
)
