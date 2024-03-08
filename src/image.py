
class Pixel:
    def __init__(self, red, green, blue) -> None:
        self.red = red
        self.green = green
        self.blue = blue

class ImagePPM:
    def __init__(self, magic, rows, cols, maxval, pixels) -> None:
        self.magic = magic
        self.rows = rows
        self.cols = cols
        self.maxval = maxval
        self.pixels = pixels

class ImagePGM:
    def __init__(self, magic, rows, cols, maxval, pixels) -> None:
        self.magic = magic
        self.rows = rows
        self.cols = cols
        self.maxval = maxval
        self.pixels = pixels

def read_ppm(filename):
    with open(filename, "rb") as file:  # Open file in binary mode
        magic = file.readline().strip().decode()

        # Skip comments
        comment_line = file.readline().decode()
        while comment_line.startswith('#'):
            comment_line = file.readline().decode()

        # The first non-comment line is dimensions
        rows, cols = map(int, comment_line.split())
        maxval = int(file.readline().strip().decode())

        if magic == "P3":
            pixels = []
            for _ in range(rows):
                row = []
                for _ in range(cols):
                    pixel_data = file.readline().split()
                    red, green, blue = map(int, pixel_data[:3])
                    row.append(Pixel(red, green, blue))
                pixels.append(row)
        elif magic == "P6":
            pixels = []
            for _ in range(rows):
                row = []
                for _ in range(cols):
                    red, green, blue = file.read(3)
                    row.append(Pixel(red, green, blue))
                pixels.append(row)
        else:
            raise ValueError(f"Unsupported PPM format: {magic}")

        return ImagePPM(magic, rows, cols, maxval, pixels)

def write_ppm(image, outputfile):
    with open(outputfile, 'w') as output:
        if output is None:
            raise ValueError("Invalid output file")

        output.write(f"{image.magic}\n")
        output.write(f"{image.rows} {image.cols}\n")
        output.write(f"{image.maxval}\n")

        for i in range(image.rows):
            for j in range(image.cols):
                pixel = image.pixels[i][j]
                output.write(f"{pixel.red:3d} {pixel.green:3d} {pixel.blue:3d}\t ")
            output.write("\n")


def read_pgm(filename):
    try:
        with open(filename, "r") as file:
            magic = file.readline().strip()
            rows, cols = map(int, file.readline().split())
            maxval = int(file.readline())
            pixels = [[0] * cols for _ in range(rows)]

            for i in range(rows):
                line = file.readline().strip()
                pixel_values = [int(value) for value in line.split()]
                pixels[i] = pixel_values

        return ImagePGM(magic, rows, cols, maxval, pixels)

    except Exception as e:
        print(f"Error reading PGM file: {e}")
        return None

def write_pgm(image, outputfile):
    with open(outputfile, 'w') as output:
        if output is None:
            raise ValueError("Invalid output file")

        output.write(f"{image.magic}\n")
        output.write(f"{image.rows} {image.cols}\n")
        output.write(f"{image.maxval}\n")

        for i in range(image.rows):
            for j in range(image.cols):
                output.write(f"{image.pixels[i][j]:3d} ")
            output.write("\n")

def convert_to_pgm(image):
    newmagic = "P2"
    newrows = image.rows
    newcols = image.cols
    newmaxval = image.maxval
    newpixels = [[0] * newcols for _ in range(newrows)]

    for i in range(newrows):
        for j in range(newcols):
            pixel_val = (image.pixels[i][j].red + image.pixels[i][j].green + image.pixels[i][j].blue) // 3
            newpixels[i][j] = pixel_val

    newimage = ImagePGM(newmagic, newrows, newcols, newmaxval, newpixels)
    return newimage

def shrink_pgm(image):
    magic = "P2"
    rows = image.rows // 2
    cols = image.cols // 2
    maxval = image.maxval

    newpixels = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            pixel_sum = 0
            for x in range(2):
                for y in range(2):
                    pixel_sum += image.pixels[2*i+x][2*j+y]
            newpixels[i][j] = pixel_sum // 4

    shrunken_pgm = ImagePGM(magic, rows, cols, maxval, newpixels)
    return shrunken_pgm
