# holdemSimulator
you provide the cards that are visible to you and the number of opponents. It then plays out many possible solutions to estimate the probability of you winning the round at showdown.


example command to run a simulation
```
> python main.py -h "ah 7d" -b "6s 8h jc" -o 3
```

## commands:

- **-h (hand):** set the cards that are visible in your hand
- **-b (board):** set the common cards on the board that are visible
- **-o (opponents):** set the number of opponents in the pot
- **-r (rounds):** the number of rounds to simulate. More rounds will lead to more accurate estimates but take longer.

