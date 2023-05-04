from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
def token(userid,seconds):
    s=Serializer('harpuj@7j',seconds)
    return s.dumps({'user':userid}).decode('utf-8')
