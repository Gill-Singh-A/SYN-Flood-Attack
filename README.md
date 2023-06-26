# SYN Flood Attack
A Python Program that implements a TCP SYN Flood Attack.

## Requirements
Languange Used = Python3<br />
Modules/Packages used:
* os
* datetime
* optparse
* colorama
* scapy
* time
<!-- -->
Install the dependencies:
```bash
pip install -r requirements.txt
```

## Input
* '-t', "--target" : Target to perform SYN Flooding Attack on
* '-p', "--port" : Target Port to flood
* '-s', "--size" : Size of Data that we want to send(in Bytes) (Default=1024 Bytes)