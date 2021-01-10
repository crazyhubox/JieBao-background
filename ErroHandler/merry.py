from functools import wraps
import inspect
import logging

getargspec = None
if getattr(inspect, 'getfullargspec', None):
    getargspec = inspect.getfullargspec
else:
    # this one is deprecated in Python 3, but available in Python 2
    getargspec = inspect.getargspec


class _Namespace:
    pass


class Merry(object):
    def __init__(self, logger_name='merry', debug=False):
        self.logger = logging.getLogger(logger_name)
        self.g = _Namespace()
        self.debug = debug
        self.except_ = {}
        self.force_debug = []
        self.force_handle = []
        self.else_ = None
        self.finally_ = None

    def _try(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ret = None
            try:
                ret = f(*args, **kwargs)

                # note that if the function returned something, the else clause
                # will be skipped. This is a similar behavior to a normal
                # try/except/else block.
                if ret is not None:
                    return ret
            except Exception as e:
                # find the best handler for this exception
                handler = None
                for c in self.except_.keys():
                    if isinstance(e, c):
                        if handler is None or issubclass(c, handler):
                            handler = c

                # if we don't have any handler, we let the exception bubble up
                if handler is None:
                    raise e

                # log exception
                self.logger.exception('[merry] Exception caught')

                # if in debug mode, then bubble up to let a debugger handle
                debug = self.debug
                if handler in self.force_debug:
                    debug = True
                elif handler in self.force_handle:
                    debug = False
                if debug:
                    raise e

                # invoke handler
                if len(getargspec(self.except_[handler])[0]) == 0:
                    return self.except_[handler]()
                else:
                    return self.except_[handler](e)
            else:
                # if we have an else handler, call it now
                if self.else_ is not None:
                    return self.else_()
            finally:
                # if we have a finally handler, call it now
                if self.finally_ is not None:
                    alt_ret = self.finally_()
                    if alt_ret is not None:
                        ret = alt_ret
                    return ret
        return wrapper

    def _except(self, *args, **kwargs):
        def decorator(f):
            for e in args:
                self.except_[e] = f
            d = kwargs.get('debug', None)
            if d:
                self.force_debug.append(e)
            elif d is not None:
                self.force_handle.append(e)
            return f
        return decorator

    def _else(self, f):
        self.else_ = f
        return f

    def _finally(self, f):
        self.finally_ = f
        return f




class MyMerry(Merry):
    
    def __init__(self, logger_name='merry', debug=False):
        super().__init__(logger_name=logger_name, debug=debug)
        self.obj_ = None
        
    def setObject(self,object=None):
        self.obj_ = object


    def getObject(self):
        return self.obj_
        
    def _try(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ret = None
            try:
                ret = f(*args, **kwargs)

                # note that if the function returned something, the else clause
                # will be skipped. This is a similar behavior to a normal
                # try/except/else block.
                if ret is not None:
                    return ret
            except BaseException as e:
                # find the best handler for this exception
                handler = None
                for c in self.except_.keys():
                    if isinstance(e, c):
                        if handler is None or issubclass(c, handler):
                            handler = c

                # if we don't have any handler, we let the exception bubble up
                if handler is None:
                    raise e

                # log exception
                self.logger.exception('[merry] Exception caught')

                # if in debug mode, then bubble up to let a debugger handle
                debug = self.debug
                if handler in self.force_debug:
                    debug = True
                elif handler in self.force_handle:
                    debug = False
                if debug:
                    raise e

                # invoke handler
                FunCargs = getargspec(self.except_[handler])[0]
                if len(FunCargs) == 0:
                    return self.except_[handler]()
                elif FunCargs[0] == 'self' and len(FunCargs) == 2:
                    return self.except_[handler](self.obj_, e)
                else:
                    return self.except_[handler](e)
            else:
                # if we have an else handler, call it now
                if self.else_ is not None and not self.obj_:
                    return self.else_()
                else:
                    return self.else_(self.obj_)
            finally:
                # if we have a finally handler, call it now
                if self.finally_ is not None:
                    if not self.obj_:
                        alt_ret = self.finally_()
                    else:
                        alt_ret = self.finally_(self.obj_)
                    if alt_ret is not None:
                        ret = alt_ret
                return ret
        return wrapper
