from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
import base64
from PIL import Image
from PIL import ImageFilter
from PIL import ImageColor
from PIL import ImageEnhance
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')

def uploadImagePage(request):
    return render(request, 'uploadImage.html')

def setEffect(request):
    
    result = {}
    
    #Open Image to apply effects
    im = Image.open("static/img/img.png")
    image = im
    filterInput = request.POST["effect"]
    borderColor = request.POST["border"];
    print filterInput + " " + borderColor
    
    #background.save('out.png')
    #background.show
    
    #Apply a filter to the picture
    if filterInput != '0':
        if filterInput == '1':
            image = im.filter(ImageFilter.BLUR)
        elif filterInput == '2':
            image = im.filter(ImageFilter.CONTOUR)
        elif filterInput == '3':
            image = im.filter(ImageFilter.DETAIL)
        elif filterInput == '4':
            image = im.filter(ImageFilter.EDGE_ENHANCE)
        elif filterInput == '5':
            image = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
        elif filterInput == '6':
            image = im.filter(ImageFilter.EMBOSS)
        elif filterInput == '7':
            image = im.convert('L')
        elif filterInput == '8':
            converter = ImageEnhance.Color(image)
            image = converter.enhance(3.0)
        elif filterInput == '9':
            image = im.filter(ImageFilter.SMOOTH_MORE)
        elif filterInput == '10':
            image = im.filter(ImageFilter.SHARPEN)
        elif filterInput == '11':
            image = im.convert('1')
        
        elif filterInput != 0:
            print("You choose a invalid filter!")
    else:
        image = im
        
            #Apply border
    if borderColor != "noBorder":
        rgb = ImageColor.getrgb(borderColor)
        img_w, img_h = image.size
        im = Image.new('RGBA', (img_w+30, img_h+30), rgb)
        bg_w, bg_h = im.size
        offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
        im.paste(image, offset)
    else:
        im = image
        
    im.save("static/img/newImage.png", "PNG")
    
    #result = {"Success": True}

    #Get image using PILLOW
    #pic = Image.open("static/img/img.png")
    #pic = pic.filter(ImageFilter.CONTOUR)
    #pic.save("static/img/newImage.png")
    
    with open("static/img/newImage.png", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        result['image'] = str

    #pic.show()
    
    return HttpResponse(json.dumps(result),content_type='application/json')

def uploadImage(request):

    result = {"Success": True}
    
    #Get the image from front-end
    imageBase64 = request.POST["image"] 
    
    #Convert image base64 to image.png
    image = imageBase64.decode('base64')

    fh = open("static/img/img.png", "wb") 
    fh.write(image)
    fh.close()
    
    with open("static/img/img.png", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        result['image'] = str
    
    return HttpResponse(json.dumps(result),content_type='application/json')