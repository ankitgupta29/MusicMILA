'''
Created on Apr 24, 2013

@author: Sandala
'''
import re
def main():
    #doc = ":| /:) I-) ;) =) test test) R&R I.O.U. 24/7 D: D= >:) [-( X( (._.) (,_,) X( D: D= >:) [-( X( (._.) (,_,) X("
    doc = " atish's D: D= >:) [-( X( (._.) (,_,) X( :| /:) I-) :) :] :-) :o) :D :)) :P :p :b =)) lol roflmao ha haha rofl (^_^) (^-^) (^.^) B-) ^_^ -_- (^o^) x   :-* O :\"> >:D< :x (^3^) :( :c =(( :'(   :(( :-S  (;_;) (T_T) (ToT) (>_<) (>.<) (;_;) (T_T) (ToT) (-_-) (^_^') ^_^"
    #doc = ":| /:) I-)"
    #termList = [p for p in doc.lower().split() for p in re.findall(r"[0-9A-Za-z'\&\-\.\/()=:;,_^ ->\]\[]+",p)]
    sTweet = " @istaysteezy  [-( X( (._.) (,_,) X( :| /:) I-) :) :] :-) tryna kill. a an he comin through our room scavenging for scraps this morning!!"
    tList = sTweet.lower().split()
    for term in tList:
        print term,len(term)
        if "@" in term or len(term) <2:
            #if "@" in term:
            tList.remove(term)
    print tList
    termList = [p for p in tList  for p in re.findall(r"[0-9A-Za-z'\&\-\.\/()=:;,_^ ->\]\[]+",p)]
    print termList
    return

if __name__ == '__main__':
    main()