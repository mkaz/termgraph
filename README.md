termgraph.py
=============

A python command-line tool which draws basic graphs in the terminal.


### Author
Marcus Kazmierczak, [http://mkaz.com/](http://mkaz.com/)


### Examples

`$ python termgraph.py ex1.dat`

![](docs/img/example.png)

`$ python termgraph.py ex2.dat --color green`

![](docs/img/example2.png)


### Background

I wanted a quick way to visualize some data which is stored in a simple text file.
I initiall created some scripts in R which generated graphs but tended to be a two
step process of creating the graph and then opening the generated graph.

I did some graphing using gnuplot, but X11 would never be started so it took time to start.
So after seeing [command-line sparklines](https://github.com/holman/spark)
I figured I could do the same thing using block characters for bar charts.



### Usage

* Create data file with two columns either comma or space separated.
  The first column is your labels, the second column is a numeric data

* python termgraph.py [datafile]


### TODO
I may or may not ever get around to these TODOs but a few ideas to take it further

- [ ] Add switch for vertical bar charts
- [ ] Add options and flags for width
- [x] Add options for different colors
- [ ] Stacked Bar Charts
- [ ] Multiple series (side-by-side)


#### Release Info

* Ver 0.3 - Dic 27, 2017
  - Color option added

* Ver 0.2 - Sep 22, 2012
  - Add width parameter

* Ver 0.1 - Sep 21, 2012
  - Initial Horizontal Graphs


### License

Copyright 2012-2018 Marcus Kazmierczak

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

