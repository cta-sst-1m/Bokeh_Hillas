import pandas as pd
import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import Select, DatetimeTickFormatter, TextInput, PreText
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure

from astropy.table import Table


df = Table.read('Bokeh_Hillas/hillas.fits', format='fits')
df = df.to_pandas()
df['local_time'] = pd.to_datetime(df['local_time'])
df = df.dropna()

SIZES = list(range(6, 22, 3))
COLORS = Spectral5

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(df[x].unique()) > 20]

def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    if x.value == 'local_time' and y.value != 'local_time':
        p = figure(plot_height=800, plot_width=800, x_axis_type="datetime", tools='pan,box_zoom,reset', **kw)
        p.xaxis.formatter = DatetimeTickFormatter(microseconds=["%m/%d/%y %I:%M:%S %p"],
        milliseconds=["%m/%d/%y %I:%M:%S %p"],
        seconds=["%m/%d/%y %I:%M:%S %p"],
        minsec=["%m/%d/%y %I:%M:%S %p"],
        minutes=["%m/%d/%y %I:%M:%S %p"],
        hourmin=["%m/%d/%y %I:%M:%S %p"],
        hours=["%m/%d/%y %I:%M:%S %p"],
        days=["%m/%d/%y %I:%M:%S %p"],
        months=["%m/%d/%y %I:%M:%S %p"],
        years=["%m/%d/%y %I:%M:%S %p"])
        p.xaxis.major_label_orientation = np.pi/4

    elif x.value != 'local_time' and y.value == 'local_time':
        p = figure(plot_height=800, plot_width=800, y_axis_type="datetime", tools='pan,box_zoom,reset', **kw)
        p.yaxis.formatter = DatetimeTickFormatter(microseconds=["%m/%d/%y %I:%M:%S %p"],
        milliseconds=["%m/%d/%y %I:%M:%S %p"],
        seconds=["%m/%d/%y %I:%M:%S %p"],
        minsec=["%m/%d/%y %I:%M:%S %p"],
        minutes=["%m/%d/%y %I:%M:%S %p"],
        hourmin=["%m/%d/%y %I:%M:%S %p"],
        hours=["%m/%d/%y %I:%M:%S %p"],
        days=["%m/%d/%y %I:%M:%S %p"],
        months=["%m/%d/%y %I:%M:%S %p"],
        years=["%m/%d/%y %I:%M:%S %p"])
        p.yaxis.major_label_orientation = np.pi/4

    elif x.value == 'local_time' and y.value == 'local_time':
        p = figure(plot_height=800, plot_width=800,x_axis_type="datetime", y_axis_type="datetime",
                   tools='pan,box_zoom,reset', **kw)
        p.xaxis.formatter = DatetimeTickFormatter(microseconds=["%m/%d/%y %I:%M:%S %p"],
        milliseconds=["%m/%d/%y %I:%M:%S %p"],
        seconds=["%m/%d/%y %I:%M:%S %p"],
        minsec=["%m/%d/%y %I:%M:%S %p"],
        minutes=["%m/%d/%y %I:%M:%S %p"],
        hourmin=["%m/%d/%y %I:%M:%S %p"],
        hours=["%m/%d/%y %I:%M:%S %p"],
        days=["%m/%d/%y %I:%M:%S %p"],
        months=["%m/%d/%y %I:%M:%S %p"],
        years=["%m/%d/%y %I:%M:%S %p"])
        p.xaxis.major_label_orientation = np.pi / 4
        p.yaxis.formatter = DatetimeTickFormatter(microseconds=["%m/%d/%y %I:%M:%S %p"],
        milliseconds=["%m/%d/%y %I:%M:%S %p"],
        seconds=["%m/%d/%y %I:%M:%S %p"],
        minsec=["%m/%d/%y %I:%M:%S %p"],
        minutes=["%m/%d/%y %I:%M:%S %p"],
        hourmin=["%m/%d/%y %I:%M:%S %p"],
        hours=["%m/%d/%y %I:%M:%S %p"],
        days=["%m/%d/%y %I:%M:%S %p"],
        months=["%m/%d/%y %I:%M:%S %p"],
        years=["%m/%d/%y %I:%M:%S %p"])
        p.yaxis.major_label_orientation = np.pi/4
    else:
        p = figure(plot_height=800, plot_width=800, tools='pan,box_zoom,reset', **kw)

    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    #if x.value in discrete:
    #    p.xaxis.major_label_orientation = pd.np.pi/4

    sz = 9
    if size.value != 'None':
        groups = pd.qcut(df[size.value].values, len(SIZES))
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        groups = pd.qcut(df[color.value].values, len(COLORS))
        c = [COLORS[xx] for xx in groups.codes]

    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p

def update(attr, old, new):
    layout.children[1] = create_figure()

#text_input = TextInput(value="filename", title="File path and name:")
#text_input.on_change('value', update)

x = Select(title='X-Axis', value='x', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='y', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + quantileable)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + quantileable)
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Hillas"
