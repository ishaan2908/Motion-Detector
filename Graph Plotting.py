from Motion_Detector import DF
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

DF["Start_string"] = DF["Start Time"].dt.strftime("%Y-%m-%d %H:%M:%S")
DF["End_string"] = DF["End Time"].dt.strftime("%Y-%m-%d %H:%M:%S")


CDS = ColumnDataSource(DF)

p = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode = "scale_width", title = "Motion Graph")
p.yaxis.minor_tick_line_color = 'white'

hover = HoverTool(tooltips = [("Start Time", "@Start_string"), ("End Time", "@End_string")])
p.add_tools(hover)

q = p.quad(left = "Start Time", right = "End Time", bottom = 0, top = 1, color = "blue", source = CDS)

output_file("Time Graph.html")
show(p)