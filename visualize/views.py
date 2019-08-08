from django.shortcuts import render
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool,ColumnDataSource, FactorRange
from django.contrib.auth.models import User
from product.models import Products, Comment

# Create your views here.

def visualize(request, product_id):
    product = Products.objects.get(pk=product_id)
    comments = Comment.objects.select_related().filter(product=product_id)
    fif_twenP = 0
    fif_twenN = 0
    twen_twen5P = 0
    twen_twen5N = 0
    twen5_thirP = 0
    twen5_thirN = 0
    for comment in comments:
        users = User.objects.filter(pk=comment.user_id)
        for user in users:
            age = user.userprofile.age
            if age>15 and age<20:
                if comment.polarity == 1:
                    fif_twenP += 1
                else:
                    fif_twenN +=1
            elif age>20 and age<25:
                if comment.polarity == 1:
                    twen_twen5P += 1
                else:
                    twen_twen5N +=1
            elif age>25 and age<30:
                if comment.polarity == 1:
                    twen5_thirP += 1
                else:
                    twen5_thirN += 1


    age_range = ['15-20', '20-25', '25-30']
    polarity = ['pos', 'neg']

    data = {'fruits' : age_range,
            'pos'   : [fif_twenP, twen_twen5P, twen5_thirP],
            'neg'   : [fif_twenN, twen_twen5N, twen5_thirN ],
            }

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x = [ (fruit, year) for fruit in age_range for year in polarity ]
    counts = sum(zip(data['pos'], data['neg']), ())  #sum(zip(data['pos'], data['neg'])) # like an hstack
    colors = ["#c9d9d3", "#718dbf"]
    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), plot_height=250, title=f'{product.title}',
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None


    script, div = components(p)

    return render(request, 'visualize/plot.html' , {'script': script, 'div':div})

def map(request):
    pass
