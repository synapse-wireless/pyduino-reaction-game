[![](https://cloud.githubusercontent.com/assets/1317406/12406044/32cd9916-be0f-11e5-9b18-1547f284f878.png)](http://www.synapse-wireless.com/)

# Pyduino Reaction Game Project

`pyduino-reaction-game` is a SNAPpy project that uses a Pyduino with an LCD shield to test your visual and auditory reaction times.

The [SparkFun LCD Button Shield](https://www.sparkfun.com/products/13293) is highly recommended
because it works very well with the Pyduino and this library.

## Installation

### For use in Portal

Download and extract the latest release zip file to Portal's `snappyImages` directory. 
By default, this is located at `..\Documents\Portal\snappyImages` on Windows.

### For use with SNAPbuild

The easiest way to install `pyduino-reaction-game` for use with SNAPbuild is using 
[pip](https://pip.pypa.io/en/latest/installing.html):

    pip install git+https://github.com/synapse-wireless/pyduino-reaction-game.git@master --process-dependency-links

Alternatively you can clone or download and extract the source, and install it:

    pip install ./pyduino-reaction-game --process-dependency-links
