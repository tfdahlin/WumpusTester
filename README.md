# WumpusTester
Python script for automating interaction with a user-developed Wumpus World program.

# Usage
`./tester.py <your_executable> <difficulty>`

## How to use
When you have compiled your code, you can run this tester against your code to see whether or not it passes the sample Wumpus World puzzles I have included in this script. There are three different difficulties of puzzles (easy, medium, and hard), and three puzzles at each difficulty, for a total of 9 puzzles. Additionally, if you think your solution is particularly clever, you can test it against my diabolical example by uncommenting it in the hard section. 

This script is a little finnicky about how it expects input to be formatted in order for it to work. It assumes that your robot starts in the bottom left corner, which is considered southwest, and it expects your program to print to stdout in the following format:
`Movement commands: "n", "e", "s", "w" (for north, east, south, west)`  
`Kill commands: "kill n", "kill e", "kill s", "kill w" (for killing the Wumpus)`  
`Request input: "input:"`  
If text besides what is listed above is printed to stdout, it will assume you have made a mistake, and will fail the test, so be careful about spelling. Furthermore, it assumes that there will not be excess newlines, and that there will be a newline after each input.

# Dependencies
This is written for Python 3, but should not have any external library dependencies.
