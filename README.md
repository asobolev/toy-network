reduced invariance model
========================

builds a network with two layers:
1. input layer, using "image_sequence_generator" and "pixel_iaf_psc_exp"
2. use 5x5gklearn0.idlmov as stimulus file
3. a second layer with e.g. 25 neurons (or more)
4. modifiable connections from input layer to layer 2 (e.g. any synapse model
with "stdp" in its name)

tries to make the network learn to differentiyte the four stimuli, such,
that from the spike output of layer 2 you can tell, which stimulus was active.

You will need to add more components to the network, to make it work. E.g.
some inhibition, maybe some form of weight normalization ...
Try it - it will teach you a lot.
If you got it, you can try if your network also works with 5x5gklearn1.idlmov,
5x5gklearn2.idlmov etc. 5x5gklearn0.idlmov has zero overlap between the four
stimuli (stimuli are orthogonal). the Other stimuli have more overlap, and
thus are a bit more difficult to separate for the network.