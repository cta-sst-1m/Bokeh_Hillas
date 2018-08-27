import pandas as pd
import numpy as np
import os

from bokeh.layouts import row, widgetbox, column
from bokeh.models import Select, DatetimeTickFormatter, TextInput
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure

from astropy.table import Table

df = pd.DataFrame({'none': []})
columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(df[x].unique()) > 20]

def load_data(filename):
    global df
    df = Table.read(filename, format='fits')
    df = df.to_pandas()
    df['local_time'] = pd.to_datetime(df['local_time'])
    df = df.dropna()
    global columns, discrete, continuous, quantileable
    columns = sorted(df.columns)
    discrete = [x for x in columns if df[x].dtype == object]
    continuous = [x for x in columns if x not in discrete]
    quantileable = [x for x in continuous if len(df[x].unique()) > 20]


SIZES = list(range(6, 22, 3))
COLORS = Spectral5

def create_figure():

    df_loc = df
    if not df.empty :
        #applying cut on data
        cut_cmd = ""
        if (str(cut_1.value) in cut_1.options) and (str(cut_1_op.value) in cut_1_op.options) and \
                        str(cut_1.value) is not 'None' and cut_1_input.value != "":
            cut_cmd += "(" + "df[\"" + str(cut_1.value) + "\"]" + str(cut_1_op.value) + \
                       "%d" % float(cut_1_input.value) + ")"

        if (str(cut_2.value) in cut_2.options) and (str(cut_2_op.value) in cut_2_op.options) and \
                        str(cut_2.value) is not 'None' and cut_2_input.value != "":
            if cut_cmd != "":
                cut_cmd += " & "
            cut_cmd += "(" + "df[\"" + str(cut_2.value) + "\"]" + str(cut_2_op.value) + \
                       "%d" % float(cut_2_input.value) + ")"

        if (str(cut_3.value) in cut_3.options) and (str(cut_3_op.value) in cut_3_op.options) and \
                        str(cut_3.value) is not 'None' and cut_3_input.value != "":
            if cut_cmd != "":
                cut_cmd += " & "
            cut_cmd += "(" + "df[\"" + str(cut_3.value) + "\"]" + str(cut_3_op.value) + \
                       "%d" % float(cut_3_input.value) + ")"

        if cut_cmd != "":
            cut_cmd += ", ["
            for i,v in enumerate(columns):
                if i==0:
                    cut_cmd += "\"" + v +"\""
                else:
                    cut_cmd += ",\"" + v + "\""
            cut_cmd += "]"
            df_loc = df.loc[eval(cut_cmd)]

        xs = df_loc[x.value].values
        ys = df_loc[y.value].values
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
    else:
        p = figure(plot_height=800, plot_width=800)
        p.text(x=[1, 2, 3], y=[1, 2, 3], text=['SST-1M', 'SST-1M', 'SST-1M'], text_color="white")
        return p

#cut possibilities:
cut_list = ["==", "<", "<=", ">", ">="]

old_filnemane = ""

def update(attr, old, new):
    layout.children[1] = create_figure()

def update_data(attr, old, new):
    new_filename = text_input.value
    if new_filename != old_filnemane and os.path.isfile(new_filename):
        load_data(new_filename)
        x.options = columns
        y.options = columns
        size.options = ['None'] + columns
        color.options = ['None'] + columns
        cut_1.options = ['None'] + columns
        cut_2.options = ['None'] + columns
        cut_3.options = ['None'] + columns
        layout.children[1] = create_figure()

text_input = TextInput(value="Bokeh_Hillas/hillas.fits", title="File path and name:")
text_input.on_change('value', update_data)

x = Select(title='X-Axis', value='x', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='y', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + quantileable)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + quantileable)
color.on_change('value', update)


#cut 1
cut_1 = Select(title='Cuts', value='', options=columns, width=100)
cut_1.on_change('value', update)
cut_1_op = Select(title='Operator', value='', options=cut_list, width=50)
cut_1_op.on_change('value', update)
cut_1_input = TextInput(value='', title="Value", width=50)
cut_1_input.on_change('value', update)

#cut 2
cut_2 = Select(title='Cuts', value='', options=columns, width=100)
cut_2.on_change('value', update)
cut_2_op = Select(title='Operator', value='', options=cut_list, width=50)
cut_2_op.on_change('value', update)
cut_2_input = TextInput(value="", title="", width=50)
cut_2_input.on_change('value', update)

#cut 3
cut_3 = Select(title='Cuts', value='', options=columns, width=100)
cut_3.on_change('value', update)
cut_3_op = Select(title='Operator', value='', options=cut_list, width=50)
cut_3_op.on_change('value', update)
cut_3_input = TextInput(value="", title="Value", width=50)
cut_3_input.on_change('value', update)


controls = widgetbox([text_input, x, y, color, size], width=350)
cut_1_row = row(cut_1, cut_1_op)
cut_2_row = row(cut_2, cut_2_op)
cut_3_row = row(cut_3, cut_3_op)
ctrl_box = column(controls, cut_1_row, cut_1_input, cut_2_row, cut_2_input, cut_3_row, cut_3_input)
layout = row(ctrl_box, create_figure())

curdoc().add_root(layout)
curdoc().title = "Hillas"
