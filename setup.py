from setuptools import setup

# TODO: addd a makefile to compile our own qt5-webkit lib
# see aur package qt5-webkit-print for options andd build

setup(
   name="libriis",
   version="0.1",
   author = "Bachir Soussi Chiadmi",
   author_email = "bach@figureslibres.io",
   packages=[
      'libriis',
      'libriis.classes',
   ],
   scripts = [
      'bin/libriis',
   ],
   include_package_data=True,
   package_data={
      # If any package contains *.txt or *.rst files, include them:
      '': ['*.png', '*.html', '*.zip', '*.scss', '*.js', '*.md'],
      '': ['libriis.assets','libriis.assets.images'],
      '': [
            'libriis.templates',
            'libriis.templates.newproject',
            'libriis.templates.newproject..config',
            'libriis.templates.newproject.assets',
            'libriis.templates.newproject.assets.css',
            'libriis.templates.newproject.assets.images',
            'libriis.templates.newproject.assets.js',
            'libriis.templates.newproject.assets.lib',
            'libriis.templates.newproject.contents'
         ]
   },
   install_requires=[
      'pyphen','sass',
   ],
)
