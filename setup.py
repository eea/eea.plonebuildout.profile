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
          'requests>=2.4.0',
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.kupu',
          'five.intid',
          'collective.warmup',
          'edw.userhistory',
          'eea.alchemy',
          'eea.annotator',
          'eea.cache',
          'eea.daviz [full]',
          'eea.depiction',
          'eea.facetednavigation < 10.0',
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
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
