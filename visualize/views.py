from django.shortcuts import render
import bokeh
import folium
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool,ColumnDataSource, FactorRange
from django.contrib.auth.models import User
from product.models import Products, Comment
from bokeh.models import HelpTool
import pandas as pd
import os

# Create your views here.

def visualize(request, product_id):
    product = Products.objects.get(pk=product_id)
    comments = Comment.objects.select_related().filter(product=product_id)
    # bar chart based on age
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
    x = [ (age, pol) for age in age_range for pol in polarity ]
    counts = sum(zip(data['pos'], data['neg']), ())  #sum(zip(data['pos'], data['neg'])) # like an hstack
    colors = ["#c9d9d3", "#718dbf"]
    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x),  title=f'{product.title}',
                toolbar_location="below", tools="pan,wheel_zoom,box_zoom,reset",plot_width=800, plot_height=300)
    p.add_tools(HelpTool())
    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.legend.label_text_font_size = '40pt'
    p.xaxis.axis_label_text_font_size = '40pt'
    p.yaxis.axis_label_text_font_size = '40pt'
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None


    script, div = components(p)

    #bar chart based on location
    product = Products.objects.get(pk=product_id)
    comments = Comment.objects.select_related().filter(product=product_id)

    kath_P = 0
    kath_N = 0
    lalit_P = 0
    lalit_N = 0
    bkt_P = 0
    bkt_N = 0
    chit_P = 0
    chit_N = 0
    gor_P = 0
    got_N = 0
    ilam_P = 0
    ilam_N = 0
    for comment in comments:
        users = User.objects.filter(pk=comment.user_id)
        for user in users:
            location = user.userprofile.location
            if location == "Kathmandu":
                if comment.polarity == 1:
                    kath_P +=1
                else:
                    kath_N +=1
            elif location == "Lalitpur":
                if comment.polarity == 1:
                    lalit_P +=1
                else:
                    lalit_N +=1
            elif location == "Bhaktapur":
                if comment.polarity == 1:
                    bkt_P += 1
                else:
                    bkt_N += 1
            elif location == "Chitwan":
                if comment.polarity == 1:
                    chit_P += 1
                else:
                    chit_N += 1
            elif location == "Gorkha":
                if comment.polarity == 1:
                    gor_P += 1
                else:
                    gor_N += 1
            elif location == "Ilam":
                if comment.polarity == 1:
                    ilam_P += 1
                else:
                    ilam_N += 1

    location = ['Kathmandu', 'Lalitpur', 'Bhaktapur','Chitwan', 'Gorkha', 'Illam']
    polarity = ['pos', 'neg']

    data = {'fruits' : location,
            'pos'   : [kath_P, lalit_P, bkt_P, chit_P, gor_P, ilam_P],
            'neg'   : [kath_N, lalit_N, bkt_N, chit_N, got_N, ilam_N],
            }

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x = [ (loc, pol) for loc in location for pol in polarity ]
    counts = sum(zip(data['pos'], data['neg']), ())  #sum(zip(data['pos'], data['neg'])) # like an hstack
    colors = ["#c9d9d3", "#718dbf"]
    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p_loc = figure(x_range=FactorRange(*x), title=f'{product.title}',
               toolbar_location="below", tools="pan,wheel_zoom,box_zoom,reset",plot_width=800, plot_height=300)
    p_loc.add_tools(HelpTool())

    p_loc.vbar(x='x', top='counts', width=0.9, source=source)

    p_loc.y_range.start = 0
    p_loc.x_range.range_padding = 0.1
    p_loc.xaxis.major_label_orientation = 1
    p_loc.xgrid.grid_line_color = None
    p_loc.legend.label_text_font_size = '40pt'


    script, div = components(p)
    script1, div1 = components(p_loc)



    return render(request, 'visualize/plot.html' , {'script': script, 'div':div,'script1':script1, 'div1':div1})

def map(request, product_id):
    product = Products.objects.get(pk=product_id)
    comments = Comment.objects.select_related().filter(product=product_id)
    kath_P = 1
    kath_N = 1
    lalit_P = 1 # to avoid zero divison error
    lalit_N = 1
    bkt_P = 1
    bkt_N = 1
    sur_P = 1
    sur_N = 1
    chit_P = 1
    chit_N =1
    gor_P = 1
    gor_N = 1
    ilam_P = 1
    ilam_N = 1
    for comment in comments:
        users = User.objects.filter(pk=comment.user_id)
        for user in users:
            location = user.userprofile.location
            if location == "Kathmandu":
                if comment.polarity == 1:
                    kath_P +=1
                else:
                    kath_N +=1

            elif location == "Lalitpur":
                if comment.polarity == 1:
                    lalit_P +=1
                else:
                    lalit_N +=1


            elif location == "Bhaktapur":
                if comment.polarity == 1:
                    bkt_P += 1
                else:
                    bkt_N += 1
            elif location == "Surkhet":
                if comment.polarity == 1:
                    sur_P += 1
                else:
                    sur_N += 1
            elif location == "Chitwan":
                if comment.polarity == 1:
                    chit_P += 1
                else:
                    chit_N += 1
            elif location == "Gorkha":
                if comment.polarity == 1:
                    gor_P += 1
                else:
                    gor_N += 1
            elif location == "Ilam":
                if comment.polarity == 1:
                    ilam_P += 1
                else:
                    ilam_N += 1

        kath_per = (kath_P)/(kath_N+kath_P)
        lalit_per = (lalit_P)/(lalit_N+lalit_P)
        bkt_per = (bkt_P)/(bkt_N+bkt_P)
        sur_per = (sur_P)/(sur_N+sur_P)
        chit_per = (chit_P)/(chit_N+chit_P)
        gor_per = (gor_P)/(gor_P+gor_N)
        ilam_per = (ilam_P)/(ilam_P+ilam_N)

    map = folium.Map(location=[27.7172, 85.3240], tiles="Mapbox Bright", zoom_start=7.5)
    state_geo = os.path.join('C:/Users/praba/Desktop', 'district.json')

    data =[[49,kath_per],[54, lalit_per],[52,bkt_per],[18,sur_per],[45, chit_per], [21,gor_per], [68,ilam_per]]
    district_data = pd.DataFrame(data, columns=['district', 'reviews'])
    map.choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=district_data,
    columns=['district', 'reviews'],
    key_on='feature.id',
    fill_color='BuGn',
    fill_opacity=0.2,
    line_opacity=0.2,
    legend_name='Positive reviews (%)'
    )
    folium.LayerControl().add_to(map)



    html_string = map.get_root().render()

    return render(request, 'visualize/map_layout.html', {'map': html_string})
