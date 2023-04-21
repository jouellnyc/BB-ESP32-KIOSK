""" Sceen types:

Options are:

['oled',
 'lilygo_watch',
 'esp32-s3-box,
 'esp32-s3-box-lite'
 'esp32_ili9341_2_8',
 'lilygo_ili9341_2_4']

"""
screen = 'esp32-s3-box'

""" Below values are valid only for screens with ili in the name """
gui_screen_types = ['ili9341', 'lilygo_ili9341_2_4','lilygo_watch', 'esp32_ili9341_2_8', 'esp32-s3-box-lite', 'esp32-s3-box']

""" Which type of case --  'upright' or 'sideways'? """
case = "sideways"

""" Are the wires  to the 'left', 'right', 'top', 'bottom'? """
wires = "left"
