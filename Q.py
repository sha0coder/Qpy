# -*- coding: utf-8 -*-

'''
     QuickPY, sha0coder's  automation.

	TODO:
    * EXAMPLES

    Q('http://site.com').download().before('<h1>','</h1>').save('titles.txt').disp()
         
    Q('http://site.com').download().split().must('a./').cut('/',0,-2).dontContains('http').save('test.txt')

    

    Q('hello').reverse().disp()
    olleh


    * METHODS

    Introspection:
        trace

    HTTP:
        httpCode(timeout=5)
        download(timeout=5)

    Data display
        disp
        dispType
        dir

    Random:
        randInt(n1, n2)
        randStr(len,min=0,max=255)

    Data manipulation:
        sort
        uniq
        strip
        join
        merge
        split
        contains
        notContain
        must
        sz
        clear
        append
        prepend
        walk

    IO:
        read
        write
        

    Control flow:
        isNum(callback)
        isStr(callback)
        isList(callback)
        


    File operations:
        save
        load
        appendFile



'''

import requests
import urllib
import time
import sys
import re
import os


class Q:
    def __init__(self,input=''):
        self.param = input
        self.err = None
        self._trace = False

    def trace(self):
        if self._trace:
            self._trace = False
        else:
            self._trace = True
        return self

    def tr(self):
        if self._trace:
            caller = sys._getframe(1).f_code.co_name
            print('[Qtrace] %s -> %s (%s)' % (caller,self.param,type(self.param)))
        return self

    def between(self,before,after):
        l = len(before)
        if self._str():
            off_init = self.param.find(before)
            off_init += l
            off_end = self.param.rfind(after, off_init)
            self.param = self.param[off_init:off_end]
        elif self._list():
            for i in xrange(len(self.param)):
                off_init = self.param[i].find(before)
                off_init += l
                off_end = self.param[i].rfind(after, off_init)
                self.param[i] = self.param[i][off_init:off_end]
        elif self._int():
            pass
                    
        return self.tr()

    def randInt(self, a, b):
        self.param = random.randint(a,b)
        return self.tr()

    def randStr(self, l, min=0, max=255):
        self.param = ''
        for i in xrange(l):
            self.param += chr(self.randint(min,max))

    def sz(self):
        self.param = len(self.param)
        return self.tr()

    def httpCode(self, timeout=5):
        r = requests.get(self.param, timeout=timeout)
        self.param = r.status_code
        return self.tr()

    def downloadFile(self, name):
        f = urllib.URLopener()
        f.retrieve(self.param,name)
        return self.tr()

    def download(self, timeout=5):
        try:
            r = requests.get(self.param, timeout=timeout)
            if r.status_code != 200:
                self.param = ''
                return self
            self.param = r.text #json?
        except:
            self.param = ''
        return self.tr()

    def cmd(self,stdin=''):
        if stdin:
            fd = os.popen(self.param,'w')
            fd.write(stdin)
        else:
            fd = os.popen(self.param,'r')
            self.param = fd.read()
        fd.close()
        return self.tr()

    def disp(self,extra='',NL=True):
        if self._str() or self._int():
            if not NL:
                sys.sdtout.write(self.param)
                sys.sdtout.write(' '+extra)
            else:
                print(self.param+' '+extra)
        elif self._list():
            for p in self.param:
                if not NL:
                    sys.sdtout.write(self.param)
                    sys.sdtout.write(' '+extra)
                else:
                    print(p+' '+extra)
        else:
            print(dir(self.param))
        return self.tr()

    def strip(self):
        if self._str():
            self.param.strip()
        elif self._list():
            new = []
            for p in self.param:
                if p:
                    new.append(p.strip())
            self.param = new
        return self.tr()

    def join(self, txt):
        self.param = txt.join(self.param)
        return self.tr()

    def merge(self,q):
        self.param += q.param
        return self.tr()

    def split(self,param=None):
        if self._str():
            if not param:
                self.param = re.split('[\n ><",\']',self.param)
            else:
                self.param = re.split(param, self.param)
        elif self._list():
            for i in xrange(self.param):
                if not param:
                    self.param[i] = re.split('[\n ><",\']',self.param[i])
                else:
                    self.param[i] =  re.split(param, self.param[i])
            pass #TODO
        return self.tr()

    def contains(self, word):
        if not self._list():
            if self._str():
                if word not in self.param:
                    self.param = ''
            else:
                print('[err] mustNot is only for lists and str')
            return self.tr()
        
        new = []
        for p in self.param:
            if word in p:
                new.append(p)
        self.param = new
        return self.tr() 

    def notContain(self, patt):
        if not self._list():
            if self._str():
                if patt in self.param:
                    self.param = ''
            else:
                print('[err] mustNot is only for lists and str')
            return self.tr()

        new = []
        for p in self.param:
            if patt not in p:
                new.append(p)

        self.param = new

        return self.tr()

    def must(self,patt):
        #TODO es obligatorio que esten TODOS
        if not self._list():
            print('[err] must is only for lists')
            return self.tr()

        new = []
        for w in self.param:
            occ = 0
            for c in patt:
                # esto esta mal pasa demasiadas veces por los mismos:
                if c == 'a' and re.findall('[a-z]',w):
                    occ += 1
                elif c == 'A' and re.findall('[A-Z]',w):
                    occ += 1
                elif c == '9' and re.findall('[0-9]',w):
                    occ += 1
                elif c == '(':
                    for s in ['?','¿','!','¡','<','>','(',')','"',"'"]:
                        if s in w:
                            occ += 1
                            break
      
                elif c == '?':
                    for s in ['?','¿','=',',','*','@','!','¡','º','ª','-','_','<','>','(',')','%','#','|','\\','/',"'",'"']:
                        if s in w:
                            occ += 1
                            break
                else:
                    if c in w:
                        occ += 1
            if occ == len(patt):
                new.append(w)
        self.param = new
        return self.tr()

    def save(self, filename):
        fd = open(filename,'wb')
        fd.write(self.param.encode('utf8'))
        fd.close()
        return self.tr()

    def saveAppend(self, filename):
        print('writting %s on %s' % (self.param, filename))
        fd = open(filename,'a+')
        fd.write(self.param)
        fd.close()
        return self.tr()

    def load(self,filename=None):
        if filename:
            fd = open(filename,'rb')
            self.param += fd.read()
            fd.close()
        else:
            fd = open(self.param,'rb')
            self.param = fd.read()
            fd.close()

        return self.tr()
    
    def read(self):
        return self.param
        
    def write(self,param):
        self.param = param
        return self.tr()

    def clear(self):
        self.param = None
        return self.tr()

    def append(self,suffix):
        if self._str():
            self.param += suffix
        elif self._list():
            for i in xrange(len(self.param)):
                self.param[i] += suffix
        return self.tr()

    def prepend(self,preffix):
        if self._str():
            self.param = preffix+self.param
        elif self._list():
            for i in xrange(len(self.param)):
                self.param[i] =  preffix+self.param[i]
        return self.tr()

    def walk(self):
        if not self._list():
            return [self.param]
        return self.param

    def _str(self):
        if type(self.param) == str or type(self.param) == unicode:
            return True
        return False

    def _list(self):
        return type(self.param) == list

    def _int(self):
        return type(self.param) == int

    def isNum(self, cb):
        if self._int():
            cb(self.tr())
        return self.tr()

    def isStr(self, cb):
        if self._str():
            cb(self.tr())
        return self.tr()

    def isList(self, cb):
        if self._list():
            cb(self.tr())
        return self.tr()

    def cut(self,byte,begin,end):
        if self._str():
            self.param = byte.join(self.param.split(byte)[begin:end])
        elif self._list():
            for i in xrange(len(self.param)):
                self.param[i] = byte.join(self.param[i].split(byte)[begin:end])
        return self.tr()

    def each(self,callback):
        if self._str():
            callback(-1,self.param)
        elif self._list():
            for i in xrange(len(self.param)):
                callback(i, self.param[i])
        return self.tr()

    def dir(self):
        print(dir(self.param))
        return self.tr()

    def dispType(self):
        print(type(self.param))
        if self._list():
            for n in self.param:
                print(type(n))
        return self.tr()

    def sort(self):
        self.param.sort()
        return self.tr()

    def uniq(self):
        self.param.sort()
        self.param = list(set(self.param))
        return self.tr()

    def equal(self, q, callback=None):
        if self.param == q.param:
            if callback:
                callback()
                return self.tr()
            else:
                return True
        else:
            if callback:
                return self.tr()
            
        return False

    def reverse(self):
        if self._str():
            s = ''
            for p in self.param:
                s = p + s 
            self.param = s
        elif self._list():
            self.param = list(reversed(self.param))
        return self.tr()

    def range(self,i,e,s=1):
        self.param = xrange(i,e,s)
        return self.tr()


            
