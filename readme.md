# Libriis

![icon](libriis/assets/images/icon.png)

A Markup Cascading Styles Printing software.

Inspired by [html2print](http://osp.kitchen/tools/html2print/) from [osp](osp.kitchen), you can write and organize your contents with markdown, design your layout with css and js, export to pdf and share your work with git.

## Contents

![Contents Stack](libriis/assets/images/Screenshot_stackcontents.png)

## Design

![Design Stack](libriis/assets/images/Screenshot_stackdesign.png)



## Installation

Libriis is developed with python and pyqt5, if you are confident with theese tools you should be able to build the app.

!! following install code is not yet functional !!

### Arch

#### qt-webkit
Under arch linux Libriis depends on a patched version of qtwebkit to render and print the pages:
You can install it from the qt5-webkit-print-tp5 package: https://figureslibres.io/gogs/bachir/aur--qt5-webkit-print/releases 

#### Libriis
Once special dependance installed : 
For Arch Linux and derivated distro, an aur package exists for Libriis :
``` 
yaourt -S libriis-git
```


### Ubuntu (not tested)
#### qt-webkit
you'll have to build qt-webkit from source : https://github.com/annulen/webkit/wiki/Building-QtWebKit-on-Linux
 
#### dependences
```shell
apt-get install qt5-base pandoc python3 python3-pyqt5 python3-pip 
pip3 install sass markdown beautifulsoup4 pypandoc pygments setuptools pyphen
```
#### Libriis
clone
```shell
git clone https://figureslibres.io/gogs/bachir/libriis.git
cd libriis
python3 start
```
install
```
python3 setup.py install --optimize=1 -f
```


## Roadmap

- [] add git features   
- [] handle pictures   
- [] embed custom build of qtwebkit specialized in print (eg remove video)






## Mockups

![mockups](libriis/assets/images/mockups.png)
