# Tad Converge and Coarse Pixel Viewer
This application is a data visualization tool for analyzing Tad Converge and Coarse Pixel data. It provides interactive graphs and tables to explore and filter data from multiple tools.
# Features
## Home Page

Displays creator and special thanks information

## Coarse-Pixel Tab

Tool selection dropdown
Multiple filter options:

X Pass/Fail
Y Pass/Fail
Time
Lot Name
X Die
Y Die
Static Iteration
Orientation
Site Serial Number


Interactive scatter plot of Coarse X vs. Coarse Y
X vs. Time plot
Y vs. Time plot
Data table with highlighted cells for out-of-range values

## Tad-Converge Tab

Tool selection dropdown
Multiple filter options:

Time
Recipe
Lot
Phase
Site Serial Number
Die X
Die Y
Misreg X
Misreg Y
TIS X
TIS Y
DAD Pos X
DAD Pos Y
Slope X
Slope Y
B X
B Y
Exit Reason
Stats


TIS X vs. DAD Position X plot with custom fit line
TIS Y vs. DAD Position Y plot with custom fit line
Data table with highlighted cells for out-of-range values

# Usage
## Coarse-Pixel Tab

Select a tool number from the dropdown.
Use the filter dropdowns to refine the displayed data.
Examine the scatter plot to see the distribution of Coarse X and Y values.
Check the X vs. Time and Y vs. Time plots to observe trends over time.
Review the data table for detailed information, with out-of-range values highlighted in red.

## Tad-Converge Tab

Choose a tool number from the dropdown.
Apply filters using the various dropdown menus to focus on specific data subsets.
Analyze the TIS X vs. DAD Position X and TIS Y vs. DAD Position Y plots, including the custom fit lines.
Inspect the data table for detailed information, with out-of-range Slope X and Slope Y values highlighted in red.

# Notes

The application reads data from SQLite database files named 'Tool_[number].db' in the specified directory.
Red markers in the Coarse-Pixel plots indicate out-of-range values.
Red markers in the Tad-Converge plots highlight specific DAD Position ranges.
The custom fit lines in the Tad-Converge plots use a slope of -1000 * Slope_X or Slope_Y.
Highlighted cells in the data tables indicate values outside the specified ranges.