from setuptools import setup

setup(
   name="cascade",
   version="0.1",

   packages=[
      'cascade',
      'cascade.classes',
   ],

   include_package_data=True,
   package_data={
      # If any package contains *.txt or *.rst files, include them:
      '': ['*.png', '*.html', '*.zip', '*.scss', '*.js', '*.md'],
      '': ['cascade.assets','cascade.assets.images'],
      '': [
            'cascade.templates',
            'cascade.templates.newproject',
            'cascade.templates.newproject..config',
            'cascade.templates.newproject.assets',
            'cascade.templates.newproject.assets.css',
            'cascade.templates.newproject.assets.images',
            'cascade.templates.newproject.assets.js',
            'cascade.templates.newproject.assets.lib',
            'cascade.templates.newproject.contents'
         ]
   },
   entry_points={
      'gui_scripts': [ 'cascade = cascade.main:__main__', ]
   },
   install_requires=[
      'pyphen','sass',
   ],
)
