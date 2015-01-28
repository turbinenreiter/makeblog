#!/usr/bin/env python3.3

import os
import shutil
import time
import markdown as md

from bs4 import BeautifulSoup as parse_html
import cssutils as css

# strings
content_path = './content/'
template_path = './template/'
template_name = 'boring'
target_path = '../blog/'
author = 'Turbinenreiter'

template_html = template_path+template_name+'/'+template_name+'.html'
template_css = template_path+template_name+'/'+template_name+'.css'
template_js = template_path+template_name+'/'+template_name+'.js'
target_html = target_path+'index.html'
target_css = target_path+'style.css'
target_js = target_path+'script.js'

# container for articles
html_articles = parse_html('', 'html5lib')
timestamps = []

# loop through files
for filename in os.listdir(content_path):

    if filename[-3:] == '.md':

        # read file
        with open(content_path+filename, 'r') as input_file:
            lines = input_file.readlines()

        # loop throug lines

        # handle metadata
        meta = {}

        # get metadata
        if lines[0] == 'meta:\n':
            i = 1
            while lines[i][0:4] == '    ':
                name, content = lines[i].strip().split(': ')
                meta[name] = content
                i = i + 1
            i = i + 1

            # replace author with default
            if meta['author'] == 'me':
                meta['author'] = author

            # create current timestamp
            newstamp = time.strptime(meta['date'], '%d.%m.%Y %H:%M:%S')
            idtfmt = 'd%d%m%y%H%M'
            newstamp_str = time.strftime(idtfmt, newstamp)

            # create meta p
            html_meta = '<p class="meta">' + \
                            meta['date'] + '<br>' +\
                            meta['author'] + '<br>' + \
                            meta['tags'] + \
                        '</p>'
        else:
            print(filename, 'doesn\'t have correct metadata.')
            break

        # create new article tag
        html_article = html_articles.new_tag('article', **{'id':newstamp_str})
        # add html from .md
        html_article.append(parse_html(md.markdown(''.join(lines[i:])), 'html5lib'))
        # add metadata
        html_article.append(parse_html(html_meta, 'html5lib'))

        # add article to articles
        try:
            if newstamp < min(timestamps):
                html_articles.append(html_article)
                print('append bc earliest', newstamp_str)
            else:
                for timestamp in timestamps:
                    if newstamp > timestamp:
                        tsid = time.strftime(idtfmt, timestamp)
                        try:
                            tag_tsid = html_articles.find('article', {'id':tsid})
                            tag_tsid.insert_before(html_article)
                            print('insert', newstamp_str, 'before', tsid)
                            break
                        except:
                            html_articles.append(html_article)
                            print('append', newstamp_str, 'bc not found', tsid)
                            break
        except ValueError:
            html_articles.append(html_article)
            print('append bc first', newstamp_str)

        timestamps.append(newstamp)
        timestamps.sort(reverse=True)

def apply_color_theme(css_template, color_theme):

    color_themes = {'BlueGrey': {'body': '#ECEFF1',
                                 'header': '#607D8B',
                                 'article': '#CFD8DC',
                                 'nav a:hover': '#FF9E80'},
                    'Red':      {'body': '#FFEBEE',
                                 'header': '#F44336',
                                 'article': '#FFCDD2',
                                 'nav a:hover': '#2196F3'},
                   }

    color_theme = color_themes[color_theme]

    for rule in css_template:
        if rule.type == rule.STYLE_RULE:
            if rule.selectorText in color_theme.keys():
                rule.style['background-color'] = color_theme[rule.selectorText]

# build index.html from template and articles and write to target
with open(template_html) as input_file:
    html_template = parse_html(input_file.read(), 'html5lib')
    html_template.section.append(html_articles)
    with open(target_html, 'w') as output_file:
        output_file.write(html_template.prettify(formatter='html5'))

with open(template_css) as input_file:
    css_template = css.parseFile(template_css)
    apply_color_theme(css_template, 'BlueGrey')
    with open(target_css, 'wb') as output_file:
        output_file.write(css_template.cssText)

# copy css template to target
#shutil.copyfile(template_css, target_css)
shutil.copyfile(template_js, target_js)
