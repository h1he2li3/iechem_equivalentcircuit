"""
This is a Python + Panel-based interactive visualisation of the frequency
dependent impedance of a simple electrical circuit (otherwise known as
equivalent circuit or equivalent circuit model in electrochemistry), 'R0-p(R1,C1)''.
The data is displayed in a Complex plane plot (or) Nyquist plot (Plot 1) and a Bode plot (Plot 2).
"""

import numpy as np
import panel as pn
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

pn.extension(sizing_mode="stretch_width")

# Creation of sliders, radio and toggle buttons, etc.
# ------------
r0 = pn.widgets.EditableFloatSlider(start=1, end=20, value=10, step=0.5,
                                    format=PrintfTickFormatter(
                                        format='%.1f Ohm'),
                                    bar_color='#ff0000')
r1 = pn.widgets.EditableFloatSlider(start=1, end=40, value=20, step=0.5,
                                    format=PrintfTickFormatter(
                                        format='%.1f Ohm'),
                                    bar_color='#ff0000')
c1 = pn.widgets.EditableFloatSlider(start=1e-6, end=1e-4, value=1e-5, step=1e-6,
                                    format=PrintfTickFormatter(format='%.6f F'),
                                    bar_color='#ff00ff')

fstart = pn.widgets.EditableFloatSlider(start=1000 / 2, end=10000000,
                                        value=9685000, step=500,
                                        format=PrintfTickFormatter(
                                            format='%.0f Hz'),
                                        bar_color='#3339ff')
fstop = pn.widgets.EditableFloatSlider(start=1000000 / 10000000, end=1000 / 2,
                                       value=0.09685000, step=0.001 / 2,
                                       format=PrintfTickFormatter(
                                           format='%.3f Hz'),
                                       bar_color='#3339ff')

pts_per_decade = pn.widgets.EditableFloatSlider(start=1, end=15, value=12,
                                                step=1,
                                                format=PrintfTickFormatter(
                                                    format='%.0f'),
                                                bar_color='#000000')

plot1width = pn.widgets.EditableIntSlider(start=200, end=800, value=525,
                                          step=25,
                                          format=PrintfTickFormatter(
                                              format='%.0f #unit'),
                                          bar_color='#808080', max_width=400)
plot2width = pn.widgets.EditableIntSlider(start=200, end=800, value=525,
                                          step=25,
                                          format=PrintfTickFormatter(
                                              format='%.0f #unit'),
                                          bar_color='#808080', max_width=400)
plot1height = pn.widgets.EditableIntSlider(start=200, end=800, value=400,
                                           step=25,
                                           format=PrintfTickFormatter(
                                               format='%.0f #unit'),
                                           bar_color='#808080', max_width=400)
plot2height = pn.widgets.EditableIntSlider(start=200, end=800, value=400,
                                           step=25,
                                           format=PrintfTickFormatter(
                                               format='%.0f #unit'),
                                           bar_color='#808080', max_width=400)

range_setting = np.logspace(np.log10(fstart.value), np.log10(fstop.value), (
        int((np.log10(fstart.value) - np.log10(fstop.value))) * 12))

plot1_range_axis = pn.widgets.EditableRangeSlider(start=0, end=80, step=1,
                                          value=(0, 60),
                                          format=PrintfTickFormatter(
                                              format='%.1f Ohm'),
                                          bar_color='#ff0000')
plot2_range_xaxis = pn.widgets.EditableRangeSlider(start=min(range_setting),
                                           end=max(range_setting),
                                           step=0.0001,
                                           value=(min(range_setting),
                                                  max(range_setting)),
                                           format=PrintfTickFormatter(
                                               format='%.1f Hz'),
                                           bar_color='#ff0000')
plot2_range_yaxis = pn.widgets.EditableRangeSlider(start=0, end=80,
                                                   step=1,
                                                   value=(0, 60),
                                                   format=PrintfTickFormatter(
                                                       format='%.5f Ohm'),
                                                   bar_color='#ff0000')

reset_button = pn.widgets.Toggle(name='Press me twice to Reset',
                                 button_type='danger')
plot_properties_radio = pn.widgets.RadioButtonGroup(name='Radio Button Group',
                                                    options=['Default',
                                                             'Manual'],
                                                    button_type='success',
                                                    max_width=600)

# Creation of Markdowns for sliders, radio and toggle buttons, etc.
# ------------
r0_Markdown = pn.pane.Markdown("""Ohmic (or) Solution resistance: $$R_0$$""")
r1_Markdown = pn.pane.Markdown(
    r"""Reaction resistance: $$R_1$$""")
c1_Markdown = pn.pane.Markdown("""Double layer capacitance: $$C_1$$""")
fstart_Markdown = pn.pane.Markdown("Start frequency: $$f_{start}$$""")
fstop_Markdown = pn.pane.Markdown(
    """Stop frequency: $$f_{stop}$$""")
pts_per_decade_Markdown = pn.pane.Markdown("""Points per decade:""")
Slider_Markdown_heading = pn.pane.Markdown('### Editable Sliders for Variables')

# Creation of Markdowns for other parts
# ------------
Info_Markdown = pn.pane.Markdown("""
##Equivalent Circuit 'R0-p(R1,C1)'

Elements in series are separated by a dash '**-**', and those in parallel are written in '**p( , )**', where elements are separated by a comma '**,**'.

Here, an interactive visualization for the equivalent circuit '**R0-p(R1,C1)**' is presented.

All the elements are grouped under '*System / Observation Parameters*' dropdown and can be varied. Start, stop frequencies, and resolution of measurement can be adjusted using sliders present under a second '*Measurement Parameters*' dropdown.

---
$$ Z_{R_{0}} = R_{0}$$

$$Z_{C_{1}} = -\\frac{j}{\\omega * C_{1}}$$ (or) $$ \\frac{1}{j* \\omega * C_{1}}$$

$$Z_{R_{1}C_{1}} = \\biggl(\\frac{1}{ \\frac{1}{Z_{R_{1}}} + \\frac{1}{Z_{C_{1}}}} \\biggl)$$

---

## $$Z = Z_{R_{0}} + Z_{R_{1}C_{1}}$$
in words, **R0 in series with parallel of (R1, C1)**

---
""")
plot_properties_Markdown = pn.pane.Markdown("""
#### Use the below radio button group to choose between 'Default' and 'Manual' setting for plot properties - size and range
""")


# Non-Interactive (I-0) and Interactive (I-1) Function(s)

# Function 1 (I-0) to Generate angular frequency range
# ------------
def ang_freq_range(fstart, fstop, pts_per_decade):
    """returns an angular frequency range as a numpy array,
       between fstart [Hz] and fstop [Hz], with a set number
       of points per decade"""
    decades = np.log10(fstart) - np.log10(fstop)
    pts_total = np.around(decades * pts_per_decade)
    frange = np.logspace(np.log10(fstop), np.log10(fstart), num=int(pts_total),
                         endpoint=True)
    return 2 * np.pi * frange
    # ------------#


# Function 2 (I-0) to Reset all sliders to their default state
# ------------
def reset_variable_values():
    """
    Returns pre-fixed default non-plot property slider values,
    which replaces the existing variable values in the calling function

    Input
    =====
    none

    Output
    =====
    default non-plot property slider values to overwrite existing ones in the
    calling function
    """
    r0.value = 10
    r1.value = 20
    c1.value = 1e-5
    fstart.value = 9685000
    fstop.value = 0.09685
    pts_per_decade.value = 12
    return r0.value, r1.value, c1.value, fstart.value, fstop.value, pts_per_decade.value
    # ------------#


# Function 3 (I-0) to Reset the plot property sliders i.e., size
# ------------
def reset_plot_size_values():
    """
    Returns pre-fixed default plot size slider values,
    which replaces the existing plot size values in the calling function.

    Input
    =====
    none

    Output
    =====
    default plot size slider values to overwrite existing ones in the calling
    function
    """
    plot1width.value = 525
    plot1height.value = 400
    plot2width.value = 525
    plot2height.value = 400
    return plot1width.value, plot1height.value, plot2width.value, plot2height.value
    # ------------#


# Function 4 (I-0) to Reset the plot property sliders i.e., plot range
# ------------
def reset_plot_range_values():
    """
    Returns pre-fixed default plot range slider values,
    which replaces the existing plot range values in the calling function

    Input
    =====
    none

    Output
    =====
    default plot range slider values to overwrite existing ones in the calling
    function
    """

    plot1_range_axis.value = (0, 60)
    plot2_range_xaxis.value = (min(range_setting), max(range_setting))
    plot2_range_yaxis.value = (0, 60)
    return plot1_range_axis.value, plot2_range_xaxis.value, plot2_range_yaxis.value
    # ------------#


# Function 5 (I-0) to Return the calculated complex impedance of the circuit
# ------------
def z_r0_r1c1(r0, r1, c1, w):
    """
    Returns the impedance of a 'R0-p(R1,C1)' circuit.

    Input
    =====
    R0 = series resistance (Ohmic resistance) of circuit
    R1 = resistance of parallel connected circuit element
    C1 = capacitance of parallel connected circuit element
    w = angular frequency

    Output
    ======
    The frequency dependent impedance as a complex number.
    """
    z_r0 = r0
    z_r1 = r1
    z_c1 = -1j / (w * c1)  # capacitive reactance
    z_r1c1 = 1 / (1 / z_r1 + 1 / z_c1)  # parallel connection
    return z_r0 + z_r1c1  # Z_R0 and Z_R1,C1 connected in series
    # ------------#


# Function 6 (I-1) to Calculate, and update Nyquist and Bode plots while also,
# updating when any parameter is changed
# ------------
@pn.depends(r0.param.value, r1.param.value, c1.param.value,
            fstart.param.value, fstop.param.value, pts_per_decade.param.value,
            plot1width.param.value, plot1height.param.value,
            plot2width.param.value, plot2height.param.value,
            plot_properties_radio.param.value, reset_button.param.value,
            plot1_range_axis.param.value, plot2_range_xaxis.param.value,
            plot2_range_yaxis.param.value)
def z(r0, r1, c1, fstart, fstop, pts_per_decade,
      plot1width, plot1height, plot2width, plot2height,
      setting, reset, plot1_range_axis,
      plot2_range_xaxis, plot2_range_yaxis):
    """
    Returns the complex plane/nyquist plot and bode plot, reset the
    plot properties mode, reset all sliders to their default state.

    Input
    =====
    R0 = ohmic/solution/series resistance of circuit
    R1 = resistance of parallel connected circuit element
    C1 = capacitance of parallel connected circuit element
    fstart = start frequency
    fstop = stop frequency
    pts_per_decade = resolution i.e., sampling points per decade
    plot sizes
    plot ranges
    state of toggle to reset all sliders
    plot properties mode between Default and Manual

    Output
    ======
    Nyquist and Bode plots with computed Impedance
    """

    plot1_x_left = plot1_range_axis[0]
    plot1_x_right = plot1_range_axis[1]
    plot1_y_bottom = plot1_range_axis[0]
    plot1_y_top = plot1_range_axis[1]

    plot2_x_left = plot2_range_xaxis[0]
    plot2_x_right = plot2_range_xaxis[1]
    plot2_y_bottom = plot2_range_yaxis[0]
    plot2_y_top = plot2_range_yaxis[1]

    if reset is True:
        reset_variable_values()
        reset_plot_size_values()

    if setting == 'Default':
        reset_plot_size_values()

    w = ang_freq_range(fstart, fstop, pts_per_decade)

    z = z_r0_r1c1(r0, r1, c1, (w / 2 * np.pi))

    if setting == 'Default':
        plot2_y_top = 20

    plot1_nyquist = ColumnDataSource(data=dict(x=z.real, y=-1 * z.imag))
    plot2_bode = ColumnDataSource(data=dict(x=w / (2 * np.pi), y=-1 * z.imag))

    plot1 = figure(name='Plot 1', title="Nyquist Plot",
                   tools="pan, wheel_zoom, box_zoom, reset, save, box_select",
                   x_axis_label="Z Real [Ohm]",
                   y_axis_label="-Z Imaginary [Ohm]",
                   plot_height=plot1height,
                   x_range=(plot1_x_left, plot1_x_right),
                   y_range=(plot1_y_bottom, plot1_y_top))
    plot1.line('x', 'y', source=plot1_nyquist, line_width=2, color="blue")
    plot2 = figure(name='Plot 2', title="Bode Plot",
                   tools="pan,wheel_zoom, box_zoom, reset, save, box_select",
                   x_axis_type="log", y_axis_type="linear",
                   x_axis_label="frequency [Hz]",
                   y_axis_label="-Z Imaginary [Ohm]",
                   plot_height=plot2height,
                   x_range=(plot2_x_left, plot2_x_right),
                   y_range=(plot2_y_bottom, plot2_y_top))
    plot2.line('x', 'y', source=plot2_bode, line_width=2, color="blue")

    if setting == 'Default':
        plot1 = figure(name='Plot 1', title="Nyquist Plot",
                       tools="pan, wheel_zoom, box_zoom, reset, save, box_select",
                       x_axis_label="Z Real [Ohm]",
                       y_axis_label="-Z Imaginary [Ohm]",
                       plot_height=plot1height,
                       x_range=(plot1_x_left, plot1_x_right),
                       y_range=(plot1_y_bottom, plot1_y_top))
        plot1.line('x', 'y', source=plot1_nyquist, line_width=2, color="blue")
        plot2 = figure(name='Plot 2', title="Bode Plot",
                       tools="pan,wheel_zoom,box_zoom,reset,save,box_select",
                       x_axis_type="log", y_axis_type="linear",
                       x_axis_label="frequency [Hz]",
                       y_axis_label='-Z Imaginary [Ohm]',
                       y_range=(plot2_y_bottom, plot2_y_top),
                       plot_height=plot2height)
        plot2.line('x', 'y', source=plot2_bode, line_width=2, color="blue")

    return pn.Column(pn.Tabs(plot1, width=plot1width,
                             height=plot1height + 30, closable=True),
                     pn.Tabs(plot2, width=plot2width,
                             height=plot2height, closable=True))
    # ------------#


# Function 7 (I-1) to Select between Default and Manual mode for plot size, and
# range parameters.
# ------------
@pn.depends(plot_properties_radio.param.value, reset_button.param.value)
def set_and_reset_plot_size_and_limits(setting, reset):
    """
    Returns Default message or shows Manual mode with plot size and range sliders.
    Further, also take in the state of Radio and Toggle panes to set the modes,
    and reset the size and range values.

    Input
    =====
    State of Reset panel-'Toggle' button

    Output
    =====
    Display plot properties panel-Sliders grouped under 'Default' and 'Manual'
    panel-Radio button
    """
    text = """
    ### Default mode enabled!
    <hr>
    """
    plot1_limits = pn.Column(plot1_range_axis)
    plot2_xlimits = pn.Column(plot2_range_xaxis)
    plot2_ylimits = pn.Column(plot2_range_yaxis)

    if reset is True:
        reset_plot_size_values()
        reset_plot_range_values()

    if setting == 'Default':
        return pn.pane.Alert(text, alert_type="success", max_width=600)
    return pn.Column('### Plot size',
                     pn.Accordion(('Nyquist plot width', plot1width),
                                  ('Nyquist plot height', plot1height),
                                  ('Bode plot width', plot2width),
                                  ('Bode plot height', plot2height),
                                  max_width=600, header_color='#FFFFFF',
                                  header_background='#008835',
                                  active_header_background='#008835'),
                     '### Plot range', pn.Accordion(
            ('Nyquist plot limits', plot1_limits),
            ('Bode plot x-axis limits', plot2_xlimits),
            ('Bode plot y-axis limits', plot2_ylimits), max_width=600,
            header_color='#FFFFFF', header_background='#008835',
            active_header_background='#008835'))


# Function 8 (I-1) to Display and Update all butler-volmer current slider variables
# ------------
@pn.depends(reset_button.param.value)
def changing_variables(reset):
    """
    Returns a Markdown/Heading of the section with a current density display,
    and Accordion(s) with variable sliders grouped under. Additionally,
    the slider variable values will also be reset to Default if reset button
    is pressed twice.

    Input
    =====
    State of Reset panel-'Toggle' button

    Output
    =====
    Reset the all sliders and output the grouped panel-sliders
    under respective heading and accordion(s)
    """
    if reset is True:
        reset_variable_values()

    tab1 = pn.Column(r0_Markdown, r0, r1_Markdown, r1, c1_Markdown, c1)
    tab2 = pn.Column(fstart_Markdown, fstart, fstop_Markdown, fstop,
                     pts_per_decade_Markdown, pts_per_decade)
    return pn.Column(Slider_Markdown_heading,
                     pn.Accordion(
                         ('System / Observation parameters', tab1),
                         ('Measurement parameters', tab2),
                         header_color='#FFFFFF',
                         header_background='#008835',
                         active_header_background='#008835'))


# ------------
Info = z
plot_properties = pn.Column(plot_properties_Markdown, plot_properties_radio,
                            set_and_reset_plot_size_and_limits)

pn.template.GoldenTemplate(accent_base_color='#008835',
                           header_background='#008835',
                           site="Interactive Electrochemistry",
                           title=" Equivalent Circuit 'R0-(R1,C1)'",
                           sidebar=[Info_Markdown, changing_variables,
                                    reset_button, plot_properties],
                           main=[Info]).servable(target='simple_app')
