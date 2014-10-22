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

    for d in range(len(datafile)-1):
        try:
            timestamp, action, _from, content, filesize, mobility = traces.import_retrievecontent(datafile[d])
            
            print Trace.export_publish(
                0.0,
                "Publish",
                random.randint(0, int(users)),
                content,
                0
            )
        except:
            pass

