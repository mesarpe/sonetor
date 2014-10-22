import re
# Generate and extract information from traces
class TraceNotRetrieveException(Exception):
    pass
class TraceNotPublishException(Exception):
    pass
class TraceNotRetrieveContentException(Exception):
    pass

def extract_mobility(field):
    #return float
    res = re.match('\(([0-9\.]*), ?([0-9\.]*)\)', field)

    if res == None:
        raise Exception('there are not mobility information in the field: %s'%field)

    return float(res.group(1)), float(res.group(2))

class Trace():
    def __init__(self):
        pass
    def importTrace(self, line, **params):
        return getattr(self, "import_%s"%action_name.lower(), line, params)()
    def import_retrieve(self, line, **params):
        data = line.split('\t')
        timestamp = float(data[0])
        action = data[1].lower()

        if action != 'retrieve':
            raise TraceNotRetrieveException('Not Retrieve line')
        _from = data[2]

        # Extract mobility information
        try:
            mobility = extract_mobility(data[4])
        except:
            mobility = None

        try:
            _to = data[3][1:-1].replace(' ', '').split(',')
            return timestamp, action, _from, _to, mobility
        except:
            return timestamp, action, _from, None, mobility

    def import_publish(self, line, **params):
        
        data = line.split('\t')
        timestamp = float(data[0])
        action = data[1].lower()

        if action != 'publish':
            raise TraceNotPublishException('Not Retrieve line')

        _from = data[2]
        try:
            content, filesize = data[3][1:-1].split(', ')
        except:#TODO: implement this
            content, filesize = 0, 12

        # Extract mobility information
        try:
            mobility = extract_mobility(data[4])
        except:
            mobility = None
        try:
            next_publish = data[5]
            return timestamp, action, _from, content, filesize, mobility, next_publish
        except:
            return timestamp, action, _from, content, filesize, mobility, None

    def import_retrievecontent(self, line, **params):
        
        data = line.split('\t')
        timestamp = float(data[0])
        action = data[1].lower()

        if action != 'retrievecontent':
            raise TraceNotRetrieveContentException('Not Retrieve Content line')

        _from = data[2]
        try:
            content, filesize = data[3][1:-1].split(', ')
        except:#TODO: implement this
            content, filesize = 0, 12

        # Extract mobility information
        try:
            mobility = extract_mobility(data[4])
        except:
            mobility = None
        try:
            next_publish = data[5]
            return timestamp, action, _from, content, filesize, mobility
        except:
            return timestamp, action, _from, content, filesize, mobility

    @staticmethod
    def export_publish(timestamp, action, _from, content, filesize, mobility = None, next_publish = None):
        res  = ""
        res += "%s\t"%timestamp
        res += "%s\t"%action.capitalize()
        res += "%s\t"%_from
        res += "(%s, %s)"%(content, filesize)
        if mobility != None:
            res += "\t%s"%mobility
        if next_publish != None:
            res += "\t%s"%next_publish
        return res

    @staticmethod
    def export_retrievecontent(timestamp, action, _from, content, filesize, mobility):
        res  = ""
        res += "%s\t"%timestamp
        res += "%s\t"%action.capitalize()
        res += "%s\t"%_from
        res += "(%s, %s)\t"%(content, filesize)
        res += "%s"%mobility
        return res

    @staticmethod
    def export_publishcontent(timestamp, action, _from, content, filesize, mobility = None):
        res  = ""
        res += "%s\t"%timestamp
        res += "%s\t"%action.capitalize()
        res += "%s\t"%_from
        res += "(%s, %s)"%(content, filesize)
        if mobility != None:
            res += "\t%s"%mobility
        return res

    @staticmethod
    def export_retrieve(timestamp, action, _from, _to, mobility):
        res  = ""
        res += "%s\t"%timestamp
        res += "%s\t"%action.capitalize()
        res += "%s\t"%_from
        res += "%s\t"%str(tuple([int(e) for e in _to if e != '']))
        res += "%s"%mobility
        return res
