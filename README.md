# whillpy
Unofficial python package for WHILL Model CK control

## Installation Steps
* `python setup.py install`

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
