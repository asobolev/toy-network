Discrimination learning
=======================

This project aims at building a network to learn to differentiate the four 
stimuli, such, that from the spike output of layer 2 one can tell, which 
stimulus was active.


Dependencies
============

nest-dev
--------

```bash
cd nest
./bootstrap.sh
cp fm_configure new_configure
```
then  modify new_configure to your needs (change directories for the prefixes)

```bash
./as_configure
make
make install
```

nix
---

https://github.com/G-Node/nixpy
