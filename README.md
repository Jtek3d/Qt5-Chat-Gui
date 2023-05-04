# Multi/os use gui, for openai chat bots
the plan i had with this:
   
a useful chat bot usable on most devices.
   in raw form only needs internet python and qt5 library.
   working on local models as to not need internet. this should be quick when i attack it.

on android its useful speech to text, using the android gboard text tool built in.
working on that integration as well. I have custom voice speech and speech to text in mind.

right now it uses premade models.
planing on integrating my own model when i get it's training to be more predictable. fun training a new model.

bloated for looks, but i can release a lite hud version, maybe even just do settings on this one to toggle ui visuals

features:
-run on any os that runs os, it uses python qt5. using api mode.
   if its a problem the library generation can be removed,
       then qt5 should be the only dependency
-easily runs on my linux, windows or android 
  prosibly even oculus being android based(hmm), 
  would have to clean the ui easily done tho 
   
-generated text using the openai library or api, 
-testing using alpaca, as well as one of the models i'm training.
-differnt model selection divinci, ada so on
-has presonality presets, temperture, top_k, legnth changes.
-has a topic bar as well as presets

-has temporary history easily set up for file history
   
-was designed for mouse drag/touch drag scrolling
