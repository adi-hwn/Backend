def aThingToDo(incoming):
  fileToRead = open(incoming,"r")
  return fileToRead.readline()

def anotherThingToDo(incoming,outgoing):
  fileToRead = open(incoming,"r")
  fileToWrite = open(outgoing,"w")
  for line in fileToRead:
     s = line
     fileToWrite.write(s)
     fileToWrite.write(s + "fuahwf")
     fileToWrite.write(s + "asfawdaina\n ufjeactaivo")
  return fileToWrite
#print 255,intToColor(255)