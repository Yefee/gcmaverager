from setuptools import setup

setup(name='gcmaverager',
      version='0.12',
      description='A lightweight parallel post process package for GCM output.',
      url='https://github.com/Yefee/gcmaverager',
      author='Chengfei He',
      author_email='che43@wisc.edu',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
      keywords='climate modeling modelling model gcm',
      license='MIT',
      packages=['gcmaverager'],
      install_requires=['xarray'],
      zip_safe=False)