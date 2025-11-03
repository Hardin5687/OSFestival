# OSFestival
A parallel computing exercise simulating a music festival and the actions and interactions of spectators and staff

# Steps to complete

Location class
* Attributes:
  * lists of spectators/staff at location.
  * Lists of spectators with special status (wasted, high, flirting, fighting, ...).
  * List of neighbouring locations.
* Methods:
  * Change state (when a user is wasted/etc it needs the location to update its status)
  * Request a list
  * Move to neighbour (sending status along)
* Special locations (inherit previous characteristics):
  * Stage (distinction with VIP needs work)
  * Bathrooms
  * Food & Drink stalls
  * Entries/exits

Spectator class
* Most frequent thread. Inherits threading methods
* Softmax for decision function

Security Guard class

Drug dealer class

Artists class

main function sets clock and initializes threads. Is there a better way to manage the clock?
