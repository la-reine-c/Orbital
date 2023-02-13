from setuptools import setup

setup(name='orbiting',
      version='0.01',
      description='Combines Celestrak.org with a reverse-gecoder',
      url='https://github.com/la-reine-c/Orbital',
      author='Lawrence Carter',
      author_email='lawrence.tn.carter@gmail.com',
      liscence='MIT',
      long_description=open('README.md').read(),
      install_requires=[
          'lxml',
          'requests',
          'pandas',
          'orbit',
          'country_converter',
      ]
)