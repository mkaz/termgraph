termgraph.py
=============

A python command-line tool which draws basic graphs in the terminal


### Author 
Marcus Kazmierczak, [http://mkaz.com/](http://mkaz.com/)

### Background

I wanted a quick ay to visualize my data from running and compare my 
mileage year-over-year. The data is stored in a simple text file, so 
it is super portable and quick and easy to update. 

I created some scripts in R which generated graphs but tended to be 
a two step process of creating the graph and then opening the 
generated graph. 

I created some graphing using gnuplot, but X11 would never be started
so it took awhile to view, so after seeing [command-line sparklines](https://github.com/holman/spark)
I figured I could do the same thing using block characters for bar charts.

### Example

<img src="https://raw.github.com/mkaz/termgraph/master/example.png">




### Usage

* Create data file with two columns either comma or space separated.
  The first column is your labels, the second column is a numeric data

* python termgraph.py [datafile]


### TODO
I may or may not ever get around to these TODOs but a few ideas to take it further

* Add switch for vertical bar charts
* Add options and flags for width
* Add options for different colors
* Stacked Bar Charts
* Multiple series (side-by-side)


#### Release Info

* Ver 0.1 - Sep 21, 2012 - Initial Horizontal Graphs


