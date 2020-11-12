import os

KeySimple=['*','-','/','=','>','<','>=','==','<=','%','+','+=','-=','*=','/=']
KeyAmbit=['(',')',',',';','.','{','}','<','>','"']
# for making sure I included all reserved word
KeyWord=[ 'bool','char' ,'char[','class','double','false','float','include','int','main','null','open','print',
          'public','read','return','short','static','str','true',
          'void']
WithoutSpaceKeyWord=['main','print','open','read','true','false']
 
LeftNoteFlag=0
RightNoteFlag=0
class Assembly():
    def IsLetter(self,Char):
         if((Char<='z' and Char>='a') or( Char<='Z' and Char>='A')):
                return True
         else:
                return False
 
    def IsNote(self,String):
        global LeftNoteFlag
        global RightNoteFlag
        NumberInString=0
        for Char in String:
            if(NumberInString<len(String)):
                NumberInString+=1
            if(Char=='/'):
                if(String[NumberInString]=='/'):
                    return 2
                elif(String[NumberInString]=='*'):
                    if(LeftNoteFlag==0):
                        LeftNoteFlag+=1
                    return 1
            elif(Char=='*'):
                if(String[NumberInString]=='/'):
                    if(RightNoteFlag==0):
                        RightNoteFlag+=1
                    return 3
            if(len(String)==NumberInString+1):
                    return False
            
    def IsDigit(self,Char):
         if(Char<='9' and Char>='0'):
             return True
         else:
             return False
 
    def IsSpace(self,Char):
         if(Char==' '):
             return True
         else:
             return False
 
    def PassSpace(self,List):                                                                                                       #delete space
        NumberinList=0
        for String in List:
            List[NumberinList]=String.strip()
            NumberinList+=1
        return List
    
    
    def SplitSourceProgram(self,List):                                                                                  #split string
        ListSplit = List.split("\\n")
        return ListSplit
    
   
    def DeleteNote(self,List):                                                                                                  #Delete comment like ''', '', #, ##
        RemoveList=[]
        FirstLeftNoteNumber=0
        NumberinList=0
        LeftNoteNumber=0
        global LeftNoteFlag
        global RightNoteFlag
        for String in List: 
            Flag=self.IsNote(String)
            NumberInString=0
            FirstLeftNoteNumber=0
            if(Flag):
                for Char in String:
                    if(NumberInString<len(String)-1):
                        NumberInString+=1
                    if(Flag==1):
                        if(Char=='#' and String[NumberInString]=='*'):
                            if(NumberInString!=1):
                                LeftNoteNumber=NumberInString-2
                            else:
                                LeftNoteNumber=NumberInString-1
                            if(FirstLeftNoteNumber==0):
                                FirstLeftNoteNumber=LeftNoteNumber
                                LeftNoteFlag=1
                            else:
                                pass
                        if(Char=="'" and String[NumberInString]=='/'):
                            if(NumberInString!=len(String)-1):
                                String=String[0:FirstLeftNoteNumber]+String[NumberInString+1:]
                            else:
                                String=String[0:FirstLeftNoteNumber]
                            LeftNoteFlag=0
                            break
                        if(NumberInString+1==len(String) and RightNoteFlag==0 and LeftNoteFlag==1 ):                                                 
                            if(FirstLeftNoteNumber==0):
                               RemoveList.append(String)
                            else:
                                String=String[0:FirstLeftNoteNumber]                                          
                            break
                    elif(Flag==2):
                        if(Char=='/' and String[NumberInString]=='/'):
                            String=String[0:NumberInString-1]
                            break
                    elif(Flag==3):
                        if(Char=='*' and String[NumberInString]=='/'):
                            if(LeftNoteFlag!=0 and NumberInString!=len(String)-1):
                                String=String[NumberInString:]
                            elif(LeftNoteFlag==0 and NumberInString!=len(String)):
                                String=String[0:NumberInString-1]+String[NumberInString+1:]
                            elif(LeftNoteFlag!=0 and NumberInString+1==len(String)):
                                RemoveList.append(String)
                            RightNoteFlag=0
                            LeftNoteFlag=0
                            break
            else:
                if(LeftNoteFlag!=0 and RightNoteFlag==0):
                    RemoveList.append(String)
                elif(LeftNoteFlag!=0 and RightNoteFlag!=0):
                    LeftNoteFlag=0
                    RightNoteFlag=0
                else:
                    pass
            List[NumberinList]=String
            if(NumberinList<len(List)-1):
                NumberinList+=1
        for ListString in RemoveList:
            List.remove(ListString)
        return List
 
    def Reader(self,List):
        ResultList=[]
        for String in List:
            Letter=''
            Digit=''
            ElseLetter=''
            NumberInString=0
            for Char in String:
                if(NumberInString<len(String)-1):
                    NumberInString+=1
                if(self.IsLetter(Char) ):
                    if(self.IsLetter(String[NumberInString]) or self.IsDigit(String[NumberInString]) ):
                        Letter+=Char
                    elif(self.IsSpace(String[NumberInString]) or (String[NumberInString] in KeyAmbit) or (String[NumberInString] in KeySimple) or (String[NumberInString:NumberInString+2] in KeySimple)):
                        Letter+=Char
                        ResultList.append(Letter)
                        Letter=''  
                else:
                    if(self.IsDigit(Char)):
                        if(self.IsLetter(String[NumberInString]) or self.IsDigit(String[NumberInString]) ):
                            Digit+=Char
                        elif (self.IsSpace(String[NumberInString]) or (String[NumberInString] in KeyAmbit) or (String[NumberInString] in KeySimple) or (String[NumberInString:NumberInString+2] in KeySimple)):
                            Digit+=Char
                            ResultList.append(Digit)
                            Digit=''
                    else:
                        if(Char=='#'):
                            ResultList.append('#')
                        else:
                            if(Char in KeyAmbit ):
                                ResultList.append(Char)
                            else:
                                if(Char in KeySimple):
                                    ElseLetter+=Char
                                    if(String[NumberInString] in KeySimple):
                                        ElseLetter+=String[NumberInString]
                                        ResultList.append(ElseLetter)
                                        ElseLetter=''
                                    else:
                                        ResultList.append(ElseLetter)
                                        ElseLetter=''
                                else:
                                    if(self.IsSpace(Char)):
                                        pass
        return ResultList
        
    def JugeMent(self,List):
        FormatFlag=0
        NumberinList=0
        for String in List:
            if(NumberinList<len(String)-1):
                NumberinList+=1
            if(len(String)==1):
               if(String=='#'):
                   print('#  ---------->comment')
               elif(String in KeyAmbit):
                    if(String=='<' ):
                        if(List[NumberinList] in KeyWord):
                            print('<  ---------->seperator')
                    elif(String=='>'):
                        if(List[NumberinList-3] in KeyAmbit or List[NumberinList-4] in KeyWord):
                            print('>  ---------->seperator')
                    else:
                        print(String+'  ---------->seperator')
               elif(String in KeySimple):
                    if(String=='%'):
                        if(not(List[NumberinList].isdigit())):
                            print('%  ---------->operator')
                            FormatFlag=1
                            continue
                    print(String+'  ---------->operator')
               else:
                    if(String.isdigit()):
                        print(String+'  ---------->number')
                    elif(String.isalnum()):
                        if(FormatFlag==0):
                            print(String+'  ---------->variable')
                        else:
                            print(String+'  ---------->variable')
                            FormatFlag==0
            else:
                if(String in KeyWord):
                    print(String+'  ---------->reserved word')
                elif(String in KeySimple):
                    print(String+'  ---------->operator')
                else:
                    if(String.isdigit()):
                        print(String+'  ---------->number')
                    elif(String.isalnum()):
                        if(FormatFlag==0):
                            print(String+'  ---------->variable')
                        else:
                            print(String+'  ---------->variable')
                            FormatFlag==0
 
 
def main():
    AsseMbly=Assembly()
    SourceProgram=[]
    Filepath= os.getcwd() + "/target_code/myscript2.py"
    for line in open(Filepath,'r',encoding='UTF-8-sig' ):
        line=line.replace('\n','')
        SourceProgram.append(line)
    print(SourceProgram)
    SourceProgram=AsseMbly.DeleteNote(SourceProgram)
    print(SourceProgram)
    SourceProgram=AsseMbly.PassSpace(SourceProgram)
    SourceProgram=AsseMbly.Reader(SourceProgram)
    print(SourceProgram)
    AsseMbly.JugeMent(SourceProgram)
 
if __name__ == "__main__":
    main()
 
