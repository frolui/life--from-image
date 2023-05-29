# Python code to implement Conway's Game Of Life
import argparse
import numpy as np
from PIL import Image
from math import floor
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# setting up the values for the grid
ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    # returns a grid of NxN random values
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    # adds a glider with top left cell at (i, j)
    glider = np.array([[0, 0, 255],
                    [255, 0, 255],
                    [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def addGosperGliderGun(i, j, grid):
    # adds a Gosper Glider Gun with top left cell at (i, j)
    gun = np.zeros(11*38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i:i+11, j:j+38] = gun

def update(frameNum, img, grid, N):
    
    # copy grid since we require 8 neighbors
    # for calculation and we go line by line
    newGrid = grid.copy()

    for i in range(N):
        for j in range(N):

            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                        grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                        grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                        grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# function to add empty columns and rows to image to make his shape - square
def make_square(np_array):
    # if square - do nothing
    w, h = np_array.shape   
    if w == h: return np_array
    
    # function to insert empty row below
    def append_array(a):
        arr = np.append(np_array, np.array([x*0 for x in range(h)]).reshape(1,h), axis = 0)
        return arr        
    
    diff = abs(w-h)
    # add empty rows if height > width
    if w < h:
        if diff == 1:
            np_array = append_array(np_array)
        if diff % 2 == 0:
            np_array = np.append(np.zeros((floor(diff/2),h), dtype=int), np_array, axis = 0)
            for i in range(floor(diff/2)):
                np_array = append_array(np_array)
        else:
            np_array = np.append(np.zeros((floor(diff/2),h), dtype=int), np_array, axis = 0)
            for i in range(floor(diff/2)+1):
                np_array = append_array(np_array)
        return np_array
            
    # add empty columns if height < width
    else:
        arrays_list = np_array.tolist()
        if diff %2 == 1:
            for i, k in enumerate(arrays_list):
                arrays_list[i] += [0]
        else:
            left = floor(diff/2)
            right = diff - left
            for i, k in enumerate(arrays_list):
                arrays_list[i] = [x*0 for x in range(left)] + k + [x*0 for x in range(right)]
        return np.array(arrays_list)

# implementation of run from image mode
def run_from_image(image, n, treeshold, maxval = 255):
    image_gray = np.array(Image.open(image).convert('L'))
    image_binary = (image_gray > int(treeshold)) * maxval
    
    resized = size_image(image_binary, n)
    square_image = (make_square(np.array(resized)) > 0 ) * maxval
    
    # display source pattern in separate window
    plt.imshow(image_from_np(square_image))
    return square_image

# function to transform numpy int8 array to Pillow image object    
def image_from_np(np_array):
    image = Image.fromarray(np.uint8(np_array))
    return image

# function to resize image to match grid size
def size_image(np_array, n):
    image_max_size = round(n * 1.0)
    
    image = image_from_np(np_array)
    width, height = image.size
    ratio = 0
    
    if width >= height:
        ratio = image_max_size / width
    else:
        ratio = image_max_size / height
    
    resized_image = image.resize((round(width*ratio), round(height*ratio)))
    return resized_image

# main() function
def main():

    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--image', dest='image', required=False)
    parser.add_argument('--treeshold', dest='treeshold', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    parser.add_argument('--from_image', action='store_true', required=False)
    args = parser.parse_args()
    
    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set treeshold
    treeshold = 130
    if not args.treeshold.isdigit():
            raise Exception("Treeshold should be number!")
    if args.treeshold and int(args.treeshold) >= 0 and int(args.treeshold) < 256:        
        treeshold = int(args.treeshold)
        
    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])
    

    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        if N < 48:
            raise Exception("Grid size for ghosper mode should be more or equal than 48.")
        grid = np.zeros(N*N).reshape(N, N)
        addGosperGliderGun(10, 10, grid)
    elif args.from_image:
        grid = run_from_image(args.image, N, treeshold)


    else: # populate grid with random on/off -
            # more off than on
        grid = randomGrid(N)

    # set up animation
   

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                frames = 10,
                                interval=updateInterval,
                                save_count=50)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()
