from __future__ import absolute_import
class Action(object):
    def __init__(self,code,length):
        self._code = code
        self._length = length

    # create read only reference
    @property
    def code(self):
        return self._code
    
    @property
    def length(self):
        return self._length
    
    @property
    def version(self):
        return 3
    
    # create normal functions
    def parse(self, data):
        # Do nothing. Many Actions don't have a payload. 
        # For the ones that have one we override this method.
        pass

    def __repr__(self):
        # return a string representation of the object
        return "[Action] Code: 0x%x, Length: %d" % (self._code, self._length)

class ActionUnknown(Action):
    ''' Dummy class to read unknown actions '''
    def __init__(self, code, length):
        super(ActionUnknown, self).__init__(code, length)

    def parse(self, data):
        if self._length > 0:
            print("skipping {0} bytes...".format(self._length))
            data.skip_bytes(self._length)
    
    def __repr__(self):
        return "[ActionUnknown] Code: 0x%x, Length: %d" % (self._code, self._length)

'''
Usage:
# 创建Action4类的实例
action = Action4(code=0xXX, length=10)

# 访问version属性
print(action.version)  # 输出: 4
'''

class Action4(Action):
    ''' Base class for SWF 4 actions '''
    def __init__(self, code, length):
        super(Action4, self).__init__(code, length)
    
    @property
    def version(self):
        return 4
    
class Action5(Action):
    ''' Base class for SWF 5 actions '''
    def __init__(self, code, length):
        super(Action5, self).__init__(code, length)

    @property
    def version(self):
        return 5

class Action6(Action):
    ''' Base class for SWF 6 actions '''
    def __init__(self, code, length):
        super(Action6, self).__init__(code, length)

    @property
    def version(self):
        return 6

class Action7(Action):
    ''' Base class for SWF 7 actions '''
    def __init__(self, code, length):
        super(Action7, self).__init__(code, length)

    @property
    def version(self):
        return 7
    

# ========================================================= 
# SWF 3 actions
# =========================================================

class ActionGetURL(Action):
    CODE = 0x83
    def __init__(self, code, length):
        self.urlString = None
        self.targetString = None
        super(ActionGetURL, self).__init__(code, length)
    def parse(self, data):
        self.urlString = data.readString()
        self.targetString = data.readString()

class ActionGotoFrame(Action):
    CODE = 0x81
    def __init__(self, code, length):
        self.frame = 0
        super(ActionGotoFrame, self).__init__(code, length)

    def parse(self, data):
        self.frame = data.readUI16()

class ActionNextFrame(Action):
    CODE = 0x04
    def __init__(self, code, length):
        super(ActionNextFrame, self).__init__(code, length)

class ActionPlay(Action):
    CODE = 0x06
    def __init__(self, code, length):
        super(ActionPlay, self).__init__(code, length)
    
    def __repr__(self):
        return "[ActionPlay] Code: 0x{:x}, Length: {}".format(self._code, self._length)
    
class ActionPreviousFrame(Action):
    CODE = 0x05
    def __init__(self, code, length):
        super(ActionPreviousFrame, self).__init__(code, length)

class ActionSetTarget(Action):
    CODE = 0x8b
    def __init__(self, code, length):
        self.targetName = None
        super(ActionSetTarget, self).__init__(code, length)

    def parse(self, data):
        self.targetName = data.readString()  

class ActionStop(Action):
    CODE = 0x07
    def __init__(self, code, length):
        super(ActionStop, self).__init__(code, length)
    
    def __repr__(self):
        return "[ActionStop] Code: 0x{:x}, Length: {}".format(self._code, self._length)
    

class ActionStopSounds(Action):
    CODE = 0x09
    def __init__(self, code, length):
        super(ActionStopSounds, self).__init__(code, length)   
        
class ActionToggleQuality(Action):
    CODE = 0x08
    def __init__(self, code, length):
        super(ActionToggleQuality, self).__init__(code, length)

class ActionWaitForFrame(Action):
    CODE = 0x8a
    def __init__(self, code, length):
        self.frame = 0
        self.skipCount = 0
        super(ActionWaitForFrame, self).__init__(code, length)

    def parse(self, data):
        self.frame = data.readUI16()
        self.skipCount = data.readUI8()



# ========================================================= 
# SWF 4 actions
# =========================================================


class ActionAdd(Action4):
    CODE = 0x0a
    def __init__(self, code, length):
        super(ActionAdd, self).__init__(code, length)

class ActionAnd(Action4):
    CODE = 0x10
    def __init__(self, code, length):
        super(ActionAnd, self).__init__(code, length)

# some 100 to go...
'''
create a null dict to save the actions and classes.
'''
# 初始化ActionTable字典
ActionTable = {}

# 收集需要添加到ActionTable的项
actions_to_add = [(value.CODE, value) for name, value in locals().items()
                 if isinstance(value, type) and issubclass(value, Action) and hasattr(value, 'CODE')]

# 迭代收集的结果，并更新ActionTable
for code, action_class in actions_to_add:
    ActionTable[code] = action_class

class SWFActionFactory(object):
    @classmethod
    def create(cls, code, length):
        action_class = ActionTable.get(code, ActionUnknown)
        return action_class(code, length)



