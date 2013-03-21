import sqlalchemy

class Connection(object):
    current = None
    connections = {}
    @classmethod
    def tell_format(cls):
        return "Format: (postgresql|mysql)://username:password@hostname/dbname, or one of %s" \
               % str(cls.connections.keys())
    def __init__(self, connect_str=None):
        try:
            engine = sqlalchemy.create_engine(connect_str)
        except: # TODO: bare except; but what's an ArgumentError?
            print(self.tell_format())
            raise 
        self.metadata = sqlalchemy.MetaData(bind=engine)
        self.name = self.assign_name(engine)
        self.session = engine.connect() 
        self.connections[self.name] = self
        Connection.current = self
    @classmethod
    def get(cls, descriptor):
        #import pdb; pdb.set_trace()
        if isinstance(descriptor, Connection):
            cls.current = descriptor
        elif descriptor:
            key = cls.connections.get(descriptor.lower()) 
            if key:
                cls.current = cls.connections[key]
            else:
                cls.current = Connection(descriptor)
        if cls.current:
            return cls.current
        else:
            raise Exception('Please specify a database connector')
    @classmethod
    def assign_name(cls, engine):
        core_name = '%s@%s' % (engine.url.username, engine.url.database)
        incrementer = 1
        name = core_name
        while name in cls.connections:
            name = '%s_%d' % (core_name, incrementer)
            incrementer += 1
        return name
