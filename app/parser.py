#!/usr/bin/env python

from lxml import etree
import time
import sys


class FixParser:

    def __init__(self):
        pass

    def store_tags(self, tags):

        doc = etree.parse('../files/FIX50SP2.xml')

        root = doc.getroot()

        fi = root.find('fields')

        for node in fi.getchildren():
            r = node.get("number")
            tags[r] = {}
            tags[r]["name"] = node.get("name")
            for value in node:
                tags[r][value.get("enum")] = value.get("description")

        return tags


    def convert_message(self, message):
        """Removes whitespace and separators. Then converts and outputs all"""

        tags = self.store_tags({})

        message = str(message).split('\n')

        del message[-1]

        for i, m in enumerate(message):

            m = m.split(" : ")

            print "Result: " + str(i) + "\n"

            print "File: " + str(m[0].split(":", 1)[0]) + "\n"
            date = str(m[0].split(":", 1)[1].split("-")[0])
            time = str(m[0].split(":", 1)[1].split("-")[1])

            date = date[:4] + '/' + date[4:6] + "/" + date[6:]
            print "Received Time: " + date + " - " + time + "\n"

            m = m[1]

            l = m.split('\x01')  # Removes separator characters
            del l[-1]  # Removes \n

            for c in l:
                key = c.split("=")[0]
                value = c.split("=")[1]

                if str(value) in tags[str(key)]:
                    print '{:<20}  {:<10}  {:<2}'.format(tags[str(key)]["name"], " = ", tags[str(key)][str(value)])
                else:
                    print '{:<20}  {:<10}  {:<2}'.format(tags[str(key)]["name"], " = ", str(value))

            print "_____________________________________________________________________________________________" + "\n"


class main:
    data = sys.stdin.read()

    fix = FixParser()

    time1 = time.time()
    fix.convert_message(data)
    time2 = time.time()

    print "Execution time: " + str(time2 - time1)

main()