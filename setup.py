from setuptools import setup, find_packages
import os

NAME = 'eea.plonebuildout.profile'
PATH = NAME.split('.') + ['version.txt']
version = open(os.path.join(*PATH)).read().strip()

setup(name='eea.plonebuildout.profile',
      version=version,
      description="A Plone profile to easily install all core EEA packages",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA buildout profile',
      author='European Environment Agency: IDM2 A-Team',
      author_email='eea-edw-a-team-alerts@googlegroups.com',
      url='https://github.com/eea/eea.plonebuildout.profile',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea', 'eea.plonebuildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests>=2.4.0',
          'setuptools',
          # -*- Extra requirements: -*-
          'five.intid',
          'ftw.globalstatusmessage',
          'collective.warmup',
          'edw.userhistory',
          'eea.alchemy',
          'eea.annotator',
          'eea.cache',
          'eea.daviz',
          'eea.depiction',
          'eea.facetednavigation',
          'eea.faceted.inheritance',
          'eea.geotags',
          'eea.icons',
          'eea.pdf',
          'eea.progressbar',
          'eea.rdfmarshaller',
          'eea.relations',
          'eea.socialmedia',
          'eea.tags',
          'eea.tinymce',
          'eea.translations',
          'eea.uberlisting',
          'eea.async.manager',
          'eea.similarity',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
