import ConfigParser
import sys

import importlib


import networkx

import random
import re

from scipy.stats import geom
from scipy.stats import lognorm
from scipy.stats import uniform
from scipy.stats import zipf

#What content will users publish? (We can use a MZipf function)
#When they retweet whom are taking pins from
    #Option1: repin from unknown users.

config = ConfigParser.RawConfigParser()
config.read(sys.argv[1])
NUMBER_OF_USERS = config.getint('General', 'number_of_users')
NUMBER_OF_FILES = config.getint('General', 'number_of_files')
SOCIAL_GRAPH = config.get('General', 'social_graph')
TIME_LIMIT = config.getint('General', 'time_limit')
COMMUNITIES_ENABLED = config.getboolean('General', 'communities_enabled')
if COMMUNITIES_ENABLED:
    NUMBER_OF_COMMUNITIES = config.getint('General', 'number_of_communities')

#TODO: not implemented!
MAPPING = config.get('General', 'mapping_algorithm')

class SelectContent(object):
    def __init__(self, number_of_files,alpha=1.2):
        #self.cdf = zipf.cdf(range(0,number_of_files), 1.5)
        #self.cdf /= self.cdf[number_of_files-1]
        #self.cdf[0]=-1

        self.cdf = {}
        self.cdf[0] = -1
        c = 0
        for i in range(1, number_of_files):
            c+= 1.0 / i**alpha
            self.cdf[i] = c
        
        for k,v in self.cdf.items():
            self.cdf[k] = v/c

    def next(self):
        x = random.random()
        lower = -1
        upper = len(self.cdf)-1
        atry = -1
        last_try = -1

        #binary search to find the nearest value y whose cdf is x
        while 1:
            atry = int((lower+upper+1)/2)

            if last_try == atry:
                break

            if self.cdf[atry] >= x:
                upper=atry
            else:
                lower = atry-1

            last_try = atry

        

        return upper

class SelectCommunityContent(SelectContent):
    def __init__(self, number_of_files, number_of_communities, alpha=1.2):
        q = 0

        # calculate CDF
        aux = []
        aux.append(-1)
        c = 0
        for i in range(1, number_of_files+1):
            c += 1.0 / (i+q)**alpha
            aux.append(1.0 / (i+q)**alpha)
        
        for k in range(1, number_of_files+1):
            aux[k-1] = aux[k-1]/c

        # Community
        comm_pdf = {}

        for community_index in range(0, number_of_communities):
            comm_pdf[community_index] = []

        for file_index in range(1, number_of_files+1):
            value = aux[file_index]
            
            communities = range(0, number_of_communities)
            random.shuffle(communities)
            
            for community_index in communities:
                if value >= 1.0:
                    rvalue = random.randint(0, int(value))
                else:
                    try:
                        rvalue = random.random() % value
                    except ZeroDivisionError:
                        rvalue = 0
                comm_pdf[community_index].append(rvalue)
                value -= rvalue

        # Garbage Collector
        aux = None

        # Create mapping, CDF
        #import matplotlib.pyplot as plt
        self.comm_cdf = {}
        self.mapping = {}
        for community_index in range(0, NUMBER_OF_COMMUNITIES):
            sl = comm_pdf[community_index]
            indexes_sort = sorted(range(len(sl)), key=lambda k: sl[k])[::-1]
            sl.sort()
            m = float(sum(sl))

            sl2 = []
            aux = 0
            for s in sl[::-1]:
                aux += s/m
                sl2.append(aux)
            
            self.mapping[community_index] = indexes_sort
            self.comm_cdf[community_index] = sl2
            #plt.plot(range(0, NUMBER_OF_FILES), sl2)
        #plt.show()

    def next(self, community_index=None):
        x = random.random()
        lower = -1
        upper = len(self.comm_cdf[community_index])-1
        atry = -1
        last_try = -1

        #binary search to find the nearest value y whose cdf is x
        while 1:
            atry = int((lower+upper+1)/2)

            if last_try == atry:
                break

            if self.comm_cdf[community_index][atry] >= x:
                upper=atry
            else:
                lower = atry-1

            last_try = atry

        

        return self.mapping[community_index][upper]

class ContentSize():
    def __init__(self, avgContent, number_of_files):
        self.avgContent = avgContent
        self.number_of_files = number_of_files
        
        
        self.filesize = geom.rvs(1.0/self.avgContent, size=number_of_files)
        
    def __getitem__(self, filename):
        return self.filesize[filename]

class ConstDistribution():
    def __init__(self, value):
        self.value = value
    def rvs(self, value):
        return value
    def next():
        return self.value

class GetDistribution():
    def __init__(self, name):
        distribution = config.get(name, 'distribution')
        if distribution == 'const':
            self.func = ConstDistribution(config.getfloat(name, 'param1'))
        else:
            self.func = getattr(importlib.import_module('scipy.stats'), distribution)
        i=1
        self.params = []
        try:
            while True:
                self.params.append(config.getfloat(name, 'param%d'%i))
                i+=1
        except Exception, e:
            pass
    def next(self):
        return self.func.rvs(*self.params)

#TODO: generalize this process
class SelectSequences():
    def  __init__(self, filename):
        self.g = networkx.read_gml(filename, relabel=True)

        self.position = None
        for node in self.g.nodes():
            if self.g.node[node]['start'] == True:
                self.position = node

        assert self.position != None

    def callback(self, action_name, **params):
        del params['content']
        return getattr(self, "%s_callback"%action_name.lower())(**params)

    def publish_callback(self, **params): #TODO: solve PARAMS!!!
        c = select_content.next(**params)
        return c, filesizes[c]
    def retrieve_callback(self, **params):
        return tuple(social_graph.neighbors(u))
    def publishcontent_callback(self, **params):
        return self.publish_callback(**params)
    def retrievecontent_callback(self, **params):
        return self.publish_callback(**params)

    def next(self):
        
        s, s2 = {}, []
        aux = 0
        for k in self.g[self.position].keys():
            aux += self.g[self.position][k]['weight']
            s[aux] = k
            s2.append(aux)

        v = random.random()
        assert v <= 1
        pos = ""
        #print v, s2
        for k in s2:
            if v<=k:
                pos = s[k]
                break

        self.position = pos
        return pos


if __name__ == '__main__':
    social_graph = getattr(__import__('graphs.%s'%SOCIAL_GRAPH), SOCIAL_GRAPH).G

    users = social_graph.nodes()[:NUMBER_OF_USERS]#range(0, NUMBER_OF_USERS)
    actions = {}
    inter_arrival = {}
    session_period = GetDistribution('SessionLength')
    if not COMMUNITIES_ENABLED:
        select_content = SelectContent(NUMBER_OF_FILES, alpha=config.getfloat('SelectContent', 'alpha'))
    else:
        select_content = SelectCommunityContent(NUMBER_OF_FILES, NUMBER_OF_COMMUNITIES, alpha=config.getfloat('SelectContent', 'alpha'))
    filesizes = ContentSize(10000, NUMBER_OF_FILES)

    a = GetDistribution('InterSessionTime')
    inter_arrival = GetDistribution('InterActivityTime')
    a.next()
    number_sessions = GetDistribution('SessionsPerUser')

    for u in users:
        time_elapsed = 0
        for _ in range(number_sessions.next()):
            inter_session_time = a.next()
            session = int(session_period.next())

            
            i = 0
            while i < session:
                    
                if not actions.has_key(u):
                    actions[u] = SelectSequences(config.get('MarkovChain', 'file'))
                next_activity_time = inter_arrival.next()
                action = actions[u].next()

                time_elapsed += next_activity_time
                if inter_session_time + time_elapsed > TIME_LIMIT:
                    break
                if not COMMUNITIES_ENABLED:
                    print "%.4f\t%s\t%s\t%s"%(inter_session_time+time_elapsed, action, u, actions[u].callback(action, content=select_content))
                else:
                    print "%.4f\t%s\t%s\t%s"%(inter_session_time+time_elapsed, action, u, actions[u].callback(action, content=select_content, community_index=u%NUMBER_OF_COMMUNITIES))

                i+=1
