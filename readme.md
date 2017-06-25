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

For Arch Linux and derivated distro, an aur package exists :
``` 
yaourt -S libriis-git
```

### Ubuntu

dependences
```shell
apt-get install qt5-base pandoc python3 python3-pyqt5 python3-pip 
pip3 install sass markdown beautifulsoup4 pypandoc pygments setuptools pyphen
```
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

### qt-webkit

for now, pdf export needs a custom build of qtwebkit, see [ospkit](http://osp.kitchen/tools/ospkit/)

```shell
sudo apt-get install build-essential perl python ruby flex gperf bison \
cmake ninja-build libfontconfig1-dev libicu-dev libsqlite3-dev \
zlib1g-dev libpng12-dev libjpeg-dev libxslt1-dev libxml2-dev libhyphen-dev

git clone -b ospkit --single-branch https://github.com/aleray/webkit.git
cd webkit
WEBKIT_OUTPUTDIR=`pwd`/build/qt
Tools/Scripts/build-webkit --qt --release --no-web-audio --no-video
cd build/qt/Release
sudo ninja install
```



## Roadmap

[] add git features
[] handle pictures
[] embed custom build of qtwebkit specialized in print (eg remove video)






## Mockups

![mockups](libriis/assets/images/mockups.png)
