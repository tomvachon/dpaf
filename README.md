# dpaf
The Dangerous Password AutoFiller! - A 1Password OP Derivative

## WARNING

This is still a work in progress and very much alpha in its look and feel.  The functionality is however, complete and usable.

## Call for Collaboration

As you can clearly see, I am not a UX expert in any way.  I welcome any help with look and feel or UX improvements.  The system is built using Kivy so any expertise there is also welcome.

## Requirements

1. 1Password Comamnd line installed to /usr/local/bin/op
2. Iterm2 Co-Process Setup with the following:
  1. /Applications/dpaf.app/Contents/MacOS/dpaf

3. Enjoy!

## Usage

1. Trigger the co-process from Iterm2
2. Enter your Master Password and hit enter
    - **Note: This app does not work offline**
3. Enter a search parameter for your item's title and hit enter
    - *Note: This works best when you enter the first part and match case*
4. Click one of the titles which matches the item you want
5. *MAGIC* The password is returned to the prompt and submitted

## Reporting Issues

Issue reporting fucntional, security, or otherwise, is to be done via Github Issues.  Pull requests are required for collaboration.