# PAXG Price logger
Sam Greydanus | December 2022 | MIT License

## Reference commands
* `screen` : Enter a screen from terminal
* `python paxg.py --verbose True --interval 120` : Start logging price data (once every 120 seconds in this case)
* CTRL-A, D : Disconnect from screen
* `screen -ls` : list current screens; copy the PID of the one you need
* `screen -r PID` : Reconnect to screen (eg `screen -r 21990.ttys002.Madrid`)