Superlegends
============
This is a reverse engineer project for Superlegends wifi light bulbs. This project is a Work in Progress. Expect the API to change regularly right now.

Status
------
Right now I'm still busy reverse engineering the protocol used in communication with the light bulbs.
To see my efforts so far, check out the [Protocol Analysis](protocol.md).

### What is working? ###
Right now you can:
- Turn on/off the lightbulbs.
- Set the colour of the light bulb using 3 8bit RGB values (0-255).
- Set the brightness of the bulb in warm mode.
- Check the current status of the light bulb. Which mode it is in and what the intensity values are.

### What isn't working ###
I've no idea what is actually possible with the bulbs. There are still some parts of the protocol that I don't understand at all.
Besides that:
- Setup the lightbulbs, connecting them to the right network and such. You'll need the app for that right now (I'm sorry).
- Functions mode (in which you can program the bulbs to do some weird patterns).
- Music mode (In which the bulb responds to an uploaded music file) -- Seems like a lot of work with no real purpose.
- Custom mode (In which you can program custom colour fadings) -- Not gonna implement this probably. This seems like something that is easier to do in python.
