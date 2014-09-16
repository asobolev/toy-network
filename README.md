discrimination learning
=======================

Build a network to learn to differentiate the four stimuli, such,
that from the spike output of layer 2 one can tell, which stimulus was active.


dependencies
============

nest-dev
--------

> cd nest
> ./bootstrap.sh
> cp fm_configure new_configure

then  modify new_configure to your needs (change directories for the prefixes)

> ./as_configure
> make
> make install


nix
---

https://github.com/G-Node/nixpy
