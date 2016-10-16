Protocol Analysis
=================

In this file, I write down my finding with the protocol. This file is full of assumptions and some of those will undoubtedly wrong. Expect this file to change relatively often.

The light bulbs have a seemingly proprietary protocol. It has confusing parts, but most are quite easily recognisable.

# Configuration
## Note
I'm busy trying to figure out what protocol is used in configuring the bulbs, and while I captured most of the traffic, the light bulbs are pretty inconsistent in responding to the commands.

## General
The light bulb can be configured right from the app. All configuration commands are sent via UDP in constrast to the commands to control the light bulb which are sent via TCP.

## Commands
### IP and Hostname
To get the IP and hostname of the lightbulb we sent:
```
HF-A11ASSISTHREAD
```
The response will look along the lines of:
```
10.0.1.31,ACCF2341CF98,HF-LPB100-ZJ200
```

Looking at the traffic I've captured the app responds with:
```
+ok
```
after which no reponse is received.

### Mode
To get the mode in which the lightbulb is configured you'll send:
```
AT+WMODE\n
```
Possible responses are:
```
+ok=STA\r\n\rn
```
The meaning of STA is unknown right now.

### SSID and MAC-address
To get the SSID and the MAC-address of the lightbulb you can send:
```
AT+WSLK\n
```
Possible responses are:
```
+ok=<SSID>(<MAC>)\r\n\r\n
```
MAC: AA:BB:CC:DD:EE:FF


### SSID
To get the SSID you send:
```
AT+WSSSID\n
```
```
+ok=<SSID>\r\n\r\n
```

### WiFi Password
To get the password you send:
```
AT+WSKEY\n
```
```
+ok=<SEC>,<ENC>,<PASS>
```
SEC: might be something like WPA2PSK
ENC: Encryption, probabably AES
PASS: Password in plain text

### Not yet identified
The following commands are sent by the application, but I've yet to discover why.
```
WAP\n
WAKEY\n
Z\n
Q\n
```

# Controlling the Light Bulb
## General
All commands are sent via TCP.

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
