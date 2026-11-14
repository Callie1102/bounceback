# A cozy, nostalgic visual novel about memory, comfort, and learning how to keep someone close.


define n = Character(None, color="#f6efe7")
define s = Character("Sally", color="#f3b7c0")

image sally = "sally.png"
image bg apartment = Transform("kitchen.png", xysize=(1920, 1080), fit="cover")
image bg kitchen = Transform("Kitchennnnnn.png", xysize=(1920, 1080), fit="cover")

transform sally_standing:
    xalign 0.92
    yalign 1.0
    zoom 1.8


default selected_ingredients = []


init python:
    soup_levels = [
        {
            "name": "Baked Potato Soup",
            "description": "This soup was so creamy and savory with a few tangy notes.",
            "ingredients": ["potatoes", "carrots", "chicken broth", "lemon juice", "salt", "sugar", "water"],
            "correct": ["potatoes", "salt", "lemon juice", "chicken broth"],
            "hint": "",
            "success": "Yes, that's it. Mom let me help cut the potatoes while the broth warmed on the stove."
        },
        {
            "name": "French Onion Soup",
            "description": "This soup was savory and rich, with a very flavorful broth.",
            "ingredients": ["onions", "beef stock", "wine vinegar", "cheese", "parsley", "apple cider vinegar", "basil"],
            "correct": ["onions", "beef stock", "wine vinegar", "cheese", "parsley"],
            "hint": "Vinegar adds more flavor to broth.",
            "success": "That's right. I remember Mom stirring the onions slowly and telling me not to rush them."
        },
        {
            "name": "Pho",
            "description": "A delicate, layered balance of deep savory richness, warm aromatic spices, and bright, fresh herbal notes.",
            "ingredients": ["spices", "charred ginger", "bone broth", "basil", "cilantro", "coriander", "oregano", "thyme", "mint leaves", "carrots", "hot sauce"],
            "correct": ["spices", "charred ginger", "bone broth", "basil", "cilantro", "coriander", "mint leaves"],
            "hint": "Think medicinal soup.",
            "success": "Yes, pho. Mom used to let me pick the herbs and smell each one before we added it."
        },
        {
            "name": "Tom Yum",
            "description": "An intense, bright, and complex hot-and-sour flavor profile.",
            "ingredients": ["lemongrass", "lime leaves", "chili jam", "fish sauce", "mushrooms", "sugar", "eggs", "milk", "rosemary", "cream", "paprika"],
            "correct": ["lemongrass", "lime leaves", "chili jam", "fish sauce", "mushrooms", "sugar"],
            "hint": "Driven by fresh aromatics rather than heavy fats or thickeners.",
            "success": "That's it, Tom yum. I remember Mom showing me how much flavor could come from a few fresh ingredients."
        },
        {
            "name": "Consomme",
            "description": "It tastes like the purest, most concentrated essence of its main ingredient—clean, deeply savory, and remarkably rich despite looking as clear as tea.",
            "ingredients": ["minced meat", "egg whites", "onions", "carrots", "celery", "parsley stems", "bay leaves", "tomatoes", "black pepper", "white chili", "broccoli", "basil", "beans", "corn", "cheddar cheese", "gochugaru"],
            "correct": ["minced meat", "egg whites", "onions", "carrots", "celery", "parsley stems", "bay leaves", "tomatoes"],
            "hint": "Aromatics lend a gentle, rounded sweetness and mild acidity that balances the heavy savory notes.",
            "success": "Yes. This is the consommé Mom made. I remember how carefully she showed me each step."
        }
    ]


screen soup_selection(level):
    modal True
    zorder 20

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1500
        ysize 760
        background Solid("#f3e7d7")

        vbox:
            spacing 20
            xfill True

            text "Which ingredients belong in this soup?" color "#2d241f" size 30 xalign 0.5
            text "Tap ingredients to select them. Selected ingredients have a white outline." color "#6a4a3d" size 18

            vpgrid:
                cols 4
                xsize 940
                ysize 460
                spacing 20
                xalign 0.5
                for ingredient in level["ingredients"]:
                    frame:
                        xysize (220, 100)
                        padding (5, 5)
                        background Solid("#ffffff" if ingredient in selected_ingredients else "#b8a596")

                        textbutton ingredient:
                            xfill True
                            yfill True
                            background Solid("#f3e7d7")
                            hover_background Solid("#e8d3c1")
                            text_color "#4f3d33"
                            text_hover_color "#2d241f"
                            action ToggleSetMembership(selected_ingredients, ingredient)

            hbox:
                spacing 20
                xalign 0.5
                textbutton "Clear" action SetVariable("selected_ingredients", [])
                textbutton "Check my soup" action Return(selected_ingredients)


label start:
    scene bg apartment
    with fade
    show sally at sally_standing

    n "The apartment is quiet except for the hum of the refrigerator."
    n "Sally sets her work bag down by the door and opens the supermarket soup she picked up on her way home."
    n "She takes a spoonful. It's fine, but it doesn't taste like her mother's soup."
    n "The familiar warmth brings back a memory of standing beside her mother in the kitchen and making soup together."

    s "It doesn't taste like Mom's. But it reminds me of making soup with her."
    s "She would let me chop the potatoes into little chunks while the broth simmered."
    s "I wish I could remember exactly what she put in it. Maybe I can make it again."

    n "She goes to the kitchen and gathers ingredients, hoping she can remember the recipe."
    scene bg kitchen
    with dissolve
    show sally at sally_standing

    call level_round(0)
    call level_round(1)
    call level_round(2)
    call level_round(3)
    call level_round(4)

    jump ending


label level_round(index):
    $ level = soup_levels[index]
    $ selected_ingredients = []
    $ attempts = 0

    n "Sally looks over the ingredients. She tries to remember what her mother used to add."

    while True:
        $ attempts += 1
        call screen soup_selection(level)
        $ guess_list = _return
        python:
            guess_set = set(guess_list)
            correct_set = set(level["correct"])
            guess_is_correct = guess_set == correct_set

        if guess_is_correct:
            call level_success(index)
            return

        if attempts == 1:
            s "Not quite. Let me think."
        else:
            s "Still not right. I'll try again."

        if level["hint"]:
            n "Hint: [level['hint']]"


label level_success(index):
    $ level = soup_levels[index]

    n "[level['name']]"
    n "[level['description']]"
    s "[level['success']]"

    if index < len(soup_levels) - 1:
        n "Sally clears the counter and gets ready to try the next recipe."

    return


label ending:
    scene bg kitchen
    with fade
    show sally at sally_standing

    n "Sally ladles the consommé into a bowl. It looks just the way she remembers."
    s "This is exactly how Mom made it."
    n "Her mother died a few years ago. Sally still misses her, especially when something brings back an ordinary day they spent together."
    n "For a while, Sally worried that she would forget the details. Now she knows she can keep some of them by making the recipes they shared."
    s "I'll make this again. I don't want to lose it."
    n "She sits down with her soup and thinks of her mother. It hurts, but she is glad to have this memory—and a way to honor it."
    return
