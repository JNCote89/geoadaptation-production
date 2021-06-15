# This is a general purpose script to return base 64 images in various other scripts (CreateWidget, CreateMap)

# Import to manipulate data in memory instead of writing them on disk
import io

# Import to encode base64 images to display them in HTML
import base64

# Function take two parameters (the file to encode and the DPI required)
def create_b64_plt(fig, dpi):

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=dpi)
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # It's technically possible to return only the encoding and add the "data:image/png;base64" in the HTML file,
    # but beware of any characters like space or slash that could alter the result.
    # I find it easier to import the whole thing from the python script.
    return "data:image/png;base64,{image}".format(image=graphic)

