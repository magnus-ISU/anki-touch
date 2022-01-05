# anki-touch

Anki 2.1.x add-on that lets you swipe to answer cards.

## Description

Anki's interface is not well-suited for use with a touchscreen. There is a need for doing the most common actions easily with a touch gesture, rather than only having buttons available at the bottom of the screen.

When presented with a question, this is to show the back of the card.

When presented with the back of a card, this is to answer the card.

Possible future work:
 - Diagonal swipes to do further actions, such as undoing, answering as "hard" as well, etc
 - Don't act if the user is interacting with an element on a card, such as a button
 - Improve the quality of the code - this is my first Anki addon

If you have an idea for a feature, please open an issue.

Forked from [tobynet's 2.0 addon](https://github.com/tobynet/anki-touch). Thank you for the template to work off of!

## Requirements

* [Anki](apps.ankiweb.net) 2.1.? or lator (tested on 2.1.50)
* Should work on all platforms as it is using QtWebEngine javascript to get the actions (tested on Linux Wayland)

## Install

Not uploaded to ankiweb.net for easy to install yet, because this is my first addon and I'm not sure if it will play with other addons correctly, and whether it works on all types of cards correctly (it adds an eventListener to the root document, and picks up many events. Even some it maybe shouldn't).

### Linux

```
cd ~/.local/share/Anki2/addons21/
git clone https://github.com/magnus-ISU/anki-touch
```

### Windows

??? (Please open an issue if you know)

tobynet said the addons' folder is `%USERPROFILE%/Documents/Anki/addons/` but this likely changed since then

## Author

[Magnus Anderson](https://github.com/magnus-ISU/)

## License

[AGPL3](https://github.com/tobynet/anki-touch/blob/master/LICENSE)

## Contribution

Pull Requests welcome!

