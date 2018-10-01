# whillpy
Unofficial python package for WHILL Model CK control

![WHILL](whillpy/docs/whill.png)

## Installation Steps
There are two ways to install
1. Install using pip
    * Use the following command `pip install whillpy`
1. Install from source
    * Use the following command `python setup.py install`

## Usage
Below is an example-

```
# import modules
from whillpy import Whill, Power

# initialize Whill by providing the name of serial port
whill = Whill(port='/dev/ttyUSB0')

# control the power
whill.set_power(Power.On)
```
