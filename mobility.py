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
from common import Trace, TraceNotRetrieveException, TraceNotPublishException, TraceNotRetrieveContentException

from pymobility.models.mobility import random_waypoint, random_walk, random_direction, truncated_levy_walk

import ConfigParser
import math
import networkx
import random
import sys

class MobilityModel(object):
    def __init__(self, name_model, map_x_size, map_y_size, min_step, max_step):

        #TODO: extract from configuration file
        #name_model = 'random_waypoint'
        #map_x_size = 100
        #map_y_size = 100
        self.name_model = name_model

        if name_model == 'random_waypoint':
            self.model = random_waypoint(1, dimensions=(map_x_size, map_y_size), velocity=(min_step, max_step), wt_max=0.)
            self.pos = None
        elif name_model == 'random_walk':
            self.model = random_walk(1, dimensions=(map_x_size, map_y_size))
            self.pos = None
        elif name_model == 'random_direction':
            self.model = random_direction(1, dimensions=(map_x_size, map_y_size))
            self.pos = None
        elif name_model == 'levy_walk':
            self.model = truncated_levy_walk(1, dimensions=(map_x_size, map_y_size))
            self.pos = None
        elif name_model == 'none':
            self.model = None
            self.pos = (str(random.randint(0, map_x_size)), str(random.randint(0, map_y_size)))
        else:
            raise Exception('The model name is not correct: %s'%name_model)
        
        self.next()

    def next(self):
    # get next position of the node
        if self.name_model == 'none':
            return self.pos
        else:
            res = self.model.next()
            self.pos = res[0][0], res[0][1]
            return self.pos
    
    def current(self):
    # get current position of the node
        return self.pos

def update_user_mobility(model, previous_timestamp, new_timestamp):
    res = 0, 0
    for i in range(int(math.floor(new_timestamp)) - int(math.floor(previous_timestamp))):
        #print model, int(math.floor(new_timestamp)) - int(math.floor(previous_timestamp)), new_timestamp, previous_timestamp
        res = model.next()

    if type(res) == tuple:
        return model.current()
    else:
        return res


    


if __name__ == '__main__':

    config = ConfigParser.RawConfigParser()
    config.readfp(open(sys.argv[1]))    

    model_name = config.get('Mobility', 'model_name')
    x_size = config.getint('Mobility', 'x_size')
    y_size = config.getint('Mobility', 'y_size')
    min_step = config.getfloat('Mobility', 'min_step') or 0.1
    max_step = config.getfloat('Mobility', 'max_step') or 1.0

    f = file(sys.argv[2])
    datafile = f.read().split('\n')

    user_timestamps = {}
    mobility_model = {}

    traces = Trace()

    for d in range(len(datafile)-1):
        try:
            try:
                timestamp, action, _from, content, filesize, mobility, next = traces.import_publish(datafile[d])
                assert mobility == None, "Mobility should be null and it is value as %s in the line %s"%(mobility, datafile[d])
                
                if not user_timestamps.has_key(_from):
                    #TODO: put information in the configuration file
                    mobility_model[_from] = MobilityModel(model_name, x_size, y_size, min_step, max_step)
                    
                    print Trace.export_publish(timestamp, action, _from, content, filesize, "(%s,%s)"%update_user_mobility(mobility_model[_from], 0, timestamp ), next)
                    user_timestamps[_from] = timestamp
                else:
                    print Trace.export_publish(timestamp, action, _from, content, filesize, "(%s,%s)"%update_user_mobility(mobility_model[_from], user_timestamps[_from], timestamp), next)
                    user_timestamps[_from] = timestamp
                
            except TraceNotPublishException:
                timestamp, action, _from, _to, mobility = traces.import_retrieve(datafile[d])
                assert mobility == None, "Mobility should be null and it is value as %s in the line %s"%(mobility, datafile[d])
                
                if not user_timestamps.has_key(_from):
                    #TODO: put information in the configuration file
                    mobility_model[_from] = MobilityModel(model_name, x_size, y_size, min_step, max_step)
                    
                    try:
                        print Trace.export_retrieve(timestamp, action, _from, tuple(_to),
                            "(%s,%s)"%update_user_mobility(mobility_model[_from], 0, timestamp ))
                    except ValueError, e:
                        print timestamp, action, _from, _to
                        raise e

                    user_timestamps[_from] = timestamp
                else:
                    print Trace.export_retrieve(timestamp, action, _from, tuple(_to),
                        "(%s,%s)"%update_user_mobility(mobility_model[_from], user_timestamps[_from], timestamp ))
                    user_timestamps[_from] = timestamp

        except TraceNotRetrieveException:
            timestamp, action, _from, content, filesize, mobility = traces.import_retrievecontent(datafile[d])
            assert mobility == None, "Mobility should be null and it is value as %s in the line %s"%(mobility, datafile[d])
            
            if not user_timestamps.has_key(_from):
                #TODO: put information in the configuration file
                mobility_model[_from] = MobilityModel(model_name, x_size, y_size, min_step, max_step)
                
                print Trace.export_retrievecontent(timestamp, action, _from, content, filesize, "(%s,%s)"%update_user_mobility(mobility_model[_from], 0, timestamp ))
                user_timestamps[_from] = timestamp
            else:
                print Trace.export_retrievecontent(timestamp, action, _from, content, filesize, "(%s,%s)"%update_user_mobility(mobility_model[_from], user_timestamps[_from], timestamp))
                user_timestamps[_from] = timestamp


