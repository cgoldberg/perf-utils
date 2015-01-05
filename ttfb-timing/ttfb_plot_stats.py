#!/usr/bin/env python

import csv
import urlparse

from bokeh.plotting import figure, output_file, show, VBox
import numpy as np


class Stats:

    def __init__(self, csv_file):
        self.loaded_stats = []
        with open(csv_file) as f:
            for i, row in enumerate(csv.reader(f)):
                if i == 0:
                    epoch_time = float(row[1])
                elapsed_time = float(row[1]) - float(epoch_time)
                original_url = row[2]
                timer = float(row[3])
                self._load_stat(original_url, elapsed_time, timer)
        self.unique_urls = list(set(urlparse.urlparse(stat[0]).path.strip() for
                                    stat in self.loaded_stats))
        self.unique_url_netlocs = [urlparse.urlparse(url).netloc
                                   for url in self.unique_urls]

    def _load_stat(self, url, elapsed_time, timer):
        self.loaded_stats.append((url, elapsed_time, timer))

    def _get_axis(self, netloc):
        x = [line[1] for line in self.loaded_stats if netloc in line[0]]
        y = [line[2] for line in self.loaded_stats if netloc in line[0]]
        return x, y

    def print_stats_report(self):
        print 'ttfb (times in milliseconds):\n'
        for netloc in self.unique_url_netlocs:
            _, y = self._get_axis(netloc)
            print '{}:'.format(netloc)
            print '    99th pct: {:.0f}'.format(np.percentile(y, 99))
            print '    95th pct: {:.0f}'.format(np.percentile(y, 95))
            print '    90th pct: {:.0f}'.format(np.percentile(y, 90))
            print '    80th pct: {:.0f}'.format(np.percentile(y, 80))
            print '    70th pct: {:.0f}'.format(np.percentile(y, 70))
            print '    60th pct: {:.0f}'.format(np.percentile(y, 60))
            print '    median: {:.0f}'.format(np.median(y))
            print '    mean: {:.0f}'.format(np.mean(y))
            print '    stdev: {:.0f}'.format(np.std(y))
            print ''

    def plot_to_html(self):
        output_file('scatter_plots.html', title='scatter plots')
        tools = 'pan,wheel_zoom,box_zoom,reset,save,box_select'
        width = 800
        height = 400
        vbox = VBox()
        for netloc in self.unique_url_netlocs:
            x, y = self._get_axis(netloc)
            p = figure(tools=tools,
                       title=netloc,
                       plot_width=width,
                       plot_height=height,
                       y_range=[0.0, 4000.0],
                       x_axis_label='elapsed time in test (seconds)',
                       y_axis_label='ttfb latency (milliseconds)',
                       )
            p.scatter(x, y, color='blue')
            vbox.children.append(p)
        show(vbox)


if __name__ == '__main__':
    csv_file = 'results-china3.log'
    stats = Stats(csv_file)
    stats.print_stats_report()
    stats.plot_to_html()
