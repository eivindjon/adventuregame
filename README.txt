In this assignment you will write a text adventure meta-game.

Your program will read a .json file like this one: game.json  Download game.jsondescribing a text adventure.

Note the format of the .json file. It is a list of lists. Each inner list represents a page of the game and contains 2 elements: a text to be shown in the screen in case the page is reached and a list of options the player can chose while he/she is on that page. Each option is composed by a list of three elements containing: Letter for the option, text for the option, page number where the player will go if he/she takes that option.

For example, consider the first page (index 0):

    [
        "Where do you want to move?\nChoose wisely.",
        [
            ["L", "Left", 1],
            ["R", "Right", 2]
        ]
    ]

The text to be printed is: "Where do you want to move?\nChoose wisely."

The options are: letter L which means Left and takes the player to page 1 and Letter R which means Right and takes the player to page 2

For this task you are given the function read_page: adv_game.py  Download adv_game.py. To use this function you need to have the file "game.json" in the same directory as your Python code. Given the page number, the function prints in the screen the correspondent text and returns the list of options (a list of lists) for that page.

Your task is to code the meta-game that, starting  in page 0, show the text and present the options for the user to decide what to do next.

Check the video of a program working with the example in game.json