"""
Deuces: A pure Python poker hand evaluation library
"""

from setuptools import setup

setup(
    name='deuces',
    version='0.2.2',
    description=__doc__,
    long_description=open('README.md', encoding="utf8").read(),
    author='Nutchanon Ninyawee',
    url='https://github.com/CircleOnCircles/deuces',
    license='MIT',
    packages=['deuces'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Games/Entertainment'
    ]
)
