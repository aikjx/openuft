
import svgutils.transform as sg
import svgutils.compose as sc

svg = sg.fromfile('projection_efficiency.svg')
svg.save('projection_efficiency.pdf')
print('Conversion completed')
