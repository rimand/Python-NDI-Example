# Python NDI Example

![image](https://user-images.githubusercontent.com/17475338/154857589-a6ff6e15-ae28-4a9f-9b8f-cba8ceee9193.png)

## Read NDI
```
 sys.path.insert(0, './pyNDI/ndi')
 #pyNDI Import
 import finder
 import receiver
 import lib

 find = finder.create_ndi_finder()
 NDIsources = find.get_sources()
 recieveSource = NDIsources[0]
 reciever = receiver.create_receiver(recieveSource)
 
 #...
 
 img = reciever.read()
```

## Create Trackbar
```
 def empty(a):
    pass
    
 cv.namedWindow("Parameters")
 cv.resizeWindow("Parameters",640,240)
 cv.createTrackbar("Threshold1","Parameters",120,255,empty)
 cv.createTrackbar("Threshold2","Parameters",50,255,empty)
 cv.createTrackbar("SizeArea","Parameters",5000,30000,empty)
```

Lib : https://github.com/CarlosFdez/pyNDI
