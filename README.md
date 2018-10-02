# whillpy
Unofficial python package for WHILL Model CK control

![WHILL](docs/whill.png)

## Dependencies
1. Python 2 or 3
1. [pyserial](https://pythonhosted.org/pyserial)
    * It can easily be installed using pip i.e., `pip install pyserial`

## Installation Steps
There are two ways to install
1. Install using pip
    * Use the following command `pip install whillpy`
1. Install from source
    * Use the following command `python setup.py install`

## Connection Diagram
In order to control WHILL Model CK, we propose to use Raspberry Pi 3 module. This module can easily be powered up by the provided USB socket in WHILL. Below are the connection diagrams -

**Power**

![power](docs/power.jpg)

**Connections**

![connections](docs/connections.jpg)

## Usage
Below is an example-

```
# import modules
from whillpy import Whill, Power

# initialize Whill by providing the name of serial port
whill = Whill(port='/dev/ttyUSB0')

# control the power
whill.set_power(Power.On)

# move straight while turning left
whill.move(straight=10, turn=-50)
```
Examples can be found in [examples](examples) directory of this package.

## Issues
Please check [here](https://github.com/ShibataLab/whillpy/issues) and create issues.

## Authors
[Ravi Prakash Joshi](https://ravijo.github.io/)
