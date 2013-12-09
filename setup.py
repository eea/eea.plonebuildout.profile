from setuptools import setup, find_packages
import os

NAME = 'eea.plonebuildout.profile'
PATH = NAME.split('.') + ['version.txt']
version = open(os.path.join(*PATH)).read().strip()

setup(name='eea.plonebuildout.profile',
      version=version,
      description="A Plone profile to easily install all core EEA packages",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='eea buildout profile',
      author='European Environment Agency',
      author_email='webadmin@eea.europa.eu',
      url='https://github.com/eea/eea.plonebuildout.profile',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea', 'eea.plonebuildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests',
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
