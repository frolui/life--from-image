# life--from-image
life game with ability to set your image as a start pattern

This life game code is based on [source solution](https://www.geeksforgeeks.org/conways-game-life-python-implementation/)
Image source [cat.jpeg](https://www.pexels.com/photo/close-up-photography-of-white-and-black-cat-69932/)

How to run:
```
python3 life.py --image 'cat.jpg' --from_image

python3 life.py --grid-size 32 --interval 500 --glide
```

You can set parameters:

--treeshold - threshold value for image binarization process (0 - 255, default - 130);
--image - path to image
--mov_file - path to save output file
--interval - update interval (ms, default - 50);
--grid-size - N value of N*N game grid (min - 8, default - 100);

Modes:

--glider - start game with a glider with top left cell at (3;3);
--ghosper - start game with a Gosper Glider Gun (min --grid-zise >= 48);
--from_image - use binary resized square version of your image as a start pattern;

Example:
```
python3 life.py --image 'cat.jpeg'  --from_image  --treeshold 150
```
![Start image](/images/cat.jpeg|width=400px)
![Start pattern image](/images/cat_pattern.png|width=400px)
![Life game gif](/images/cat_life.gif|width=400px)