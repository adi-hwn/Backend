def aThingToDo(incoming):
  fileToRead = open(incoming,"r")
  return fileToRead.readline()

def anotherThingToDo(incoming,outgoing,fill):
  fileToRead = open(incoming,"r")
  fileToWrite = open(outgoing,"w")
  for f in fill:
      fileToWrite.write(f[0])
      fileToWrite.write(",")
  return fileToWrite
#print 255,intToColor(255)