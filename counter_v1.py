# Import libraries the program uses
from PIL import Image
import time
import json

# To time how long the program takes to find all
start_time = time.time()

# Open the final_place image (https://placedata.reddit.com/data/final_place.png)
final_place = Image.open('final_place.png')
# Load the pixels
final_place_pix = final_place.load()

# Create an AmongUs image with white background
amongus_image = Image.new("RGB", (final_place.width, final_place.height), (255, 255, 255))
amongus_image.save("final_place_amongus.png")

# Set the counter
amongus_counter = 0

# Something to visualise coordinates
# AmongUs shape: 0 = anything, 1 = body_color, 2 = eye_color
# [0, 1, 1, 1]  [0           (x,y)           (x+1,y)         (x+2,y)]
# [1, 1, 2, 2]  [(x-1,y+1)   (x,y+1)         (x+1, y+1)      (x+2, y+1)]
# [1, 1, 1, 1]  [(x-1,y+2)   (x, y+2)        (x+1,y+2)       (x+2, y+2)]
# [0, 1, 1, 1]  [0           (x, y+3)        (x+1, y+3)      (x+2, y+3)]                            
# [0, 1, 0, 1]  [0           (x, y+4)        0               (x+2, y+4)]

def statistics(body_color, eye_color):
    # stats.json before counting
    # {
    # "total": 0,
    # "body": {

    #     },
    #     "eye": {
            
    #     }
    # }

    with open("stats.json", "r") as f:
        data = json.load(f)
    
    # Create color key if there isn't one already
    # Add 1 to the color key if there is
    try:
        data["body"][str(body_color)] += 1
    except KeyError: data["body"][str(body_color)] = 1

    try:
        data["eye"][str(eye_color)] += 1
    except KeyError: data["eye"][str(eye_color)] = 1

    # Total AmongUs
    data["total"] += 1

    # Save data
    with open("stats.json", "w") as f:
        json.dump(data, f, indent=4)

def drawAmongUs(x, y, body_color, eye_color):
    # Open the final_place_amongus image
    amongus_image = Image.open("final_place_amongus.png")
    amongus_image_pix = amongus_image.load()
    
    # Draw eyes
    amongus_image_pix[x+1, y+1] = eye_color
    amongus_image_pix[x+2, y+1] = eye_color

    # This could get cleaned up, that's a todo
    # Draw body
    amongus_image_pix[x,y] = body_color
    amongus_image_pix[x+1,y] = body_color
    amongus_image_pix[x+2,y] = body_color

    amongus_image_pix[x-1,y+1] = body_color
    amongus_image_pix[x,y+1] = body_color

    amongus_image_pix[x-1,y+2] = body_color
    amongus_image_pix[x, y+2] = body_color
    amongus_image_pix[x+1,y+2] = body_color
    amongus_image_pix[x+2, y+2] = body_color

    amongus_image_pix[x, y+3] = body_color
    amongus_image_pix[x+1, y+3] = body_color
    amongus_image_pix[x+2, y+3] = body_color

    amongus_image_pix[x, y+4] = body_color
    amongus_image_pix[x+2, y+4] = body_color

    # Save the Image (could do that at the end, but if it crashes you atleast have something)
    amongus_image.save("final_place_amongus.png")

def isAmongUs(x: int, y: int):
    # Check if AmongUs is possible:
    # x-1 < 0: "backpack" is not possible
    # x+3 > final_place.width: not enough room for AmongUs body
    # y+4 > final_place.height: not enough room for AmongUs legs
    if x-1 < 0 or x+3 > final_place.width or y+4 > final_place.height: return False
    
    # Get the colors
    body_color = final_place_pix[x,y]
    eye_color = final_place_pix[x+1, y+1]

    # Check if eye color isn't body color because otherwise any 5x4 grid with the same color is AmongUs (I decided it isn't)
    if eye_color == body_color: return False

    # Check if eyes have same color, if they haven't it's a broken AmongUs and doesn't get counted
    if not eye_color == final_place_pix[x+2, y+1]: return False

    # This could get cleaned up, that's a todo
    # Check if body has the same color
    if not body_color == final_place_pix[x+1, y]: return False
    if not body_color == final_place_pix[x+2, y]: return False

    if not body_color == final_place_pix[x-1, y+1]: return False
    if not body_color == final_place_pix[x, y+1]: return False

    if not body_color == final_place_pix[x-1, y+2]: return False
    if not body_color == final_place_pix[x, y+2]: return False
    if not body_color == final_place_pix[x+1, y+2]: return False
    if not body_color == final_place_pix[x+2, y+2]: return False

    if not body_color == final_place_pix[x, y+3]: return False
    if not body_color == final_place_pix[x+1, y+3]: return False
    if not body_color == final_place_pix[x+2, y+3]: return False

    if not body_color == final_place_pix[x, y+4]: return False
    if not body_color == final_place_pix[x+2, y+4]: return False

    # If there is an AmongUs, draw and log it
    drawAmongUs(x, y, body_color, eye_color)
    statistics(body_color, eye_color)

    # Return that there is an among us
    return True

# Loop through the final_place image
for y in range(0, final_place.height):    
    for x in range(0, final_place.width):
        # If there is an AmongUs, count it
        # This is also done in statistics(), but it counts twice to be sure
        if isAmongUs(x, y):
            amongus_counter += 1
            # Log the colum to see the progress and how many AmongUs have been found
            print(f"column: {y}/{final_place.height} AmongUs: {amongus_counter}")

# Print statistics
print("\n")
print(f"Total AmongUs counted: {amongus_counter}")
print(f'It took: {time.time()-start_time} seconds')

