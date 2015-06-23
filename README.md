# DroidSec [![Build Status](https://travis-ci.org/DarioI/DroidSec.svg?branch=master)](https://travis-ci.org/DarioI/DroidSec)
DroidSec is a security suite for analyzing Android .apk files. Core analysis technology is based on the awesome Androguard codebase.

The sole purpose of this tool is for educational and security research purposes only. Use it on your own responsibility. 
## How to run
- Make sure Python 2.7 is installed and on your path
- Make sure Android Debug Bridge (ADB) is installed and on your path
- Install [pip](https://pip.pypa.io/en/latest/installing.html)
- Download DroidSec and install requirements, run in a terminal: 
```
git clone https://github.com/DarioI/DroidSec.git
cd DroidSec
pip install -r requirements.txt
```
- Run DroidSec:
```
python droidsec.py
```
Any bugs or problems, please mail to <dario.incalza@gmail.com>

##Features
- Load .APK from system or dump from connected device
- Android Permissions overview
- Application information
- Show usage of reflection code
- Show usage of dynamic code update
- Show usage of crypto code
- Show usage of permissions
- Decompilation and browsing through .java sources (integration of the Androguard Gui app)

##Roadmap
- Instrument APKs
- Sign instrumented APKs

##Dependencies
- docutils
- dumpey
- Flask
- IPy
- ipython
- numpy
- PySide


##License
###DroidSec
Copyright (C) 2015, Dario Incalza <dario.incalza@gmail.com>
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS-IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

###Androguard
Copyright (C) 2012/2013/2014, Anthony Desnos <desnos at t0t0.fr>
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS-IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

###DAD

Copyright (C) 2012/2013/2014, Geoffroy Gueguen <geoffroy.gueguen@gmail.com>
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS-IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

##Development Phase
It is still heavily under development. Pull requests are appreciated. 
