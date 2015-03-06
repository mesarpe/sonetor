#####################################################################
#SONETOR, a social network traffic Generator.
#
#Developed by Cesar A. Bernardini Copyright (C) 2014.
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Library General Public
#License as published by the Free Software Foundation; either
#version 2 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Library General Public License for more details.
#
#You should have received a copy of the GNU Library General Public
#License along with this library; if not, write to the
#Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
#Boston, MA  02110-1301, USA. 
#
#####################################################################
import ConfigParser
import random
import sys

from common import Trace
    

if __name__ == '__main__':

    config = ConfigParser.RawConfigParser()
    config.readfp(open(sys.argv[1]))    

    users = config.get('General', 'number_of_users')

    f = file(sys.argv[2])
    datafile = f.read().split('\n')

    user_timestamps = {}
    mobility_model = {}

    traces = Trace()

    content_set = set()

    for d in range(len(datafile)-1):
        try:
            timestamp, action, _from, content, filesize, mobility = traces.import_retrievecontent(datafile[d])
            content_set.add(content)
            
        except:
            pass


    for content in content_set
        print Trace.export_publish(
            0.0,
            "Publish",
            random.randint(0, int(users)),
            content,
            0
        )
