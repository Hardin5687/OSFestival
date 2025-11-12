# OSFestival
A parallel computing exercise simulating a music festival and the actions and interactions of spectators and staff

# To-Do List

Location class
* Movement is very primitive.
  * We should need to move between neighbours
  * We should be able to find the path to a non-neighbouring target
  * Movement between locations should take time. Similar to a queue, like cashier threads
* Special locations
  * Stage (distinction with VIP needs work)
    * Have the attribute music
  * Bathrooms
  * Food carts
    * Have a menu attribute and a method to buy food (with a queue)
  * Drink stalls
    * Could be combined with food carts. Serve alcohol
    * Maybe all food carts are drink stalls, but not all drink stalls are food carts
  * Water (?)
    * Needs thought. Many locations (like bathrooms) should offer water
  * Entries/exits

Spectator class
* dictionary of personalities currently only contains the most basic one. More should be written
  * This is an easy task, just follow the existing template for 'averageJoe'
* method forcedDecisions() hasn't been started
* run() method isn't finished
  * We need an action function for each possible decision
    * Both as a nested if statement and as a unique method
    * Writing these should help to see what's needed in the special locations
  * We need to update preferences after each loop

# Special characters

None have been started but they are not a priority
* Security Guard class
* Drug dealer class
* Artists class

main function sets clock and initializes threads. Is there a better way to manage the clock?
