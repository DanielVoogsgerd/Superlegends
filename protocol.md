Protocol Analysis
=================

In this file, I write down my finding with the protocol. This file is full of assumptions and some of those will undoubtedly wrong. Expect this file to change relatively often.

The light bulbs have a seemingly proprietary protocol. It has confusing parts, but most are quite easily recognisable.


## On/off
### Sending
```
Light on:
71 23 0f a3
-- -- -- --
1  2  3  4
```
```
Light off:
71 24 0f a4
-- -- -- --
1  2  3  4
```

#### Legend
1. Consistent header
2. The on or off command itself: on 0x23 and off 0x24
3. Constant part
4. [Checksum](#checksum)

### Receiving
Dataless ACK packet

## Setting colour / Warm mode

### Sending
```
Setting the colour to pure red:
31 ff 00 00 00 f0 0f 2f
-- -------- -- -- -- --
1     2     3  4  5  6
```
```
Setting the colour to pure green:
31 00 ff 00 00 f0 0f 2f
-- -------- -- -- -- --
1     2     3  4  5  6
```
```
Setting the colour to pure blue:
31 00 00 ff 00 f0 0f 2f
-- -------- -- -- -- --
1     2     3  4  5  6
```
```
Maximum brightness warm mode:
31 00 00 00 ff f0 0f 4e
-- -------- -- -- -- --
1     2     3  4  5  6
```

#### Legend
1. Header for setting colour and warm modes this is 0x31
2. RGB 8 bit colour values
3. Warm mode intensity value
4. Mode: 0xf0 for colour mode, 0x0f for warm mode.
5. Constant part
6. [Checksum](#checksum)

### Receiving
Dataless ACK packet


## Status

### Sending
Right now I just captured the status requesting sequence for one bulb, but it seems to work on all bulb I've tested.
```
Checking the status
81 8a 8b 96
-------- --
   1     2
```

#### Legend
1. Constant sequence; seems to work for all bulbs in all modes
2. [Checksum](#checksum)

### Receiving
```
Light bulb 1, warm mode:
81 44 23 61 21 1d 00 00 00 ff 04 00 0f 99
----- -- ----- -- -------- -- ----- -- --
  1   2    3   4     5     6    7   8  9
```
```
Light bulb 1, colour mode:
81 44 23 61 21 1d 49 8e ff 00 04 00 f0 51
----- -- ----- -- -------- -- ----- -- --
  1   2    3   4     5     6    7   8  9
```
```
Light bulb 2, warm mode:
81 44 23 61 21 1f 00 00 00 ff 04 00 0f 9b
----- -- ----- -- -------- -- ----- -- --
  1   2    3   4     5     6    7   8  9
```
```
Light bulb 1, warm mode:
81 44 24 61 21 1d 00 00 00 1e 04 00 0f b9
----- -- ----- -- -------- -- ----- -- --
  1   2    3   4     5     6    7   8  9
```

#### Legend:
1. Constant header
2. Randomly changing number in the low 20 range
3. Constant part in transmission
4. Device dependent number
5. The RGB values of the bulb
6. The brightness of the bulb if set in warm mode
7. Constant sequence, probably to identify the response
8. The mode of the light bulb
9. [Checksum](#checksum)

# Checksum
The checksum is quite easily calculated, just add up all the bytes and take the 256 modulus.
