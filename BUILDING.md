# Pre-requisites

1. Install Python3 in a virutal environment
2. Install Cython
3. Install libraries from requirements.txt


# Building the source

```pyinstaller -y --clean --windowed --name dpaf  --exclude-module _tkinter   --exclude-module Tkinter    --exclude-module twisted  /Users/myuser/git/dpaf/dpaf/main.py```

Open ```dpaf.spec``` and change the following line:

```coll = COLLECT(exe,```

to 

```coll = COLLECT(exe, Tree('/Users/myuser/git/dpaf/dpaf/'),```

then run

```pyinstaller -y --clean --windowed dpaf.spec```

This will output a .dmg in ```dist/``` which you can then move over to /Applications


# Troubleshooing

You should ensure that you cleanly pass any Kivy tests or this will likely fail
