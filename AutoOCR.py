import PyHook3
import pythoncom
import sys
from PIL import ImageGrab




#鼠标左键按下
def OnMouseLeftDownEvent(event):
  global position
  position.append(event.Position[0])
  position.append(event.Position[1])

  return True


#鼠标左键松开
def OnMouseLeftUpEvent(event):
  global position
  position.append(event.Position[0])
  position.append(event.Position[1])
 # print(position)
  #开始识别
  result = ocr(position)  #获取json格式的文本
  resultFinal = getContent(result)   #解析json
  addToClipboard(resultFinal) 
  position.clear()

  global hm
  hm.UnhookMouse()

  return True


#监听键盘，按下alt+q退出程序，按下alt+a开始监听鼠标
def OnKeyboardEvent(event):
  if chr(event.Ascii) == 'q' and event.Alt != 0 :
    sys.exit()
  elif chr(event.Ascii) == 'a' and event.Alt != 0 :
    global hm
    hm.HookMouse()

  return True
  


#识别指定区域的文字，返回json形式的文本内容
def ocr(squareInfo):
  tempPic = "temp.jpg"
  #先保存截图
  img = ImageGrab.grab(squareInfo)
  img.save(tempPic)
  from aip import AipOcr
  # 定义常量  
  APP_ID = '********'
  API_KEY = '**********'
  SECRET_KEY = '***********'
  # 初始化文字识别分类器
  client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
  image = get_file_content(tempPic)
  #调用通用文字识别, 图片参数为本地图片
  result = client.basicGeneral(image)
  return result


#读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()



#将由API返回的json数据解析为纯文本
def getContent(jText):
  res = ''
  for i in jText['words_result']:
    print(i['words'])
    res = res + i['words'] + '\r\n'
  return res



# 将内容添加到剪切板
def addToClipboard(aString):
  import win32clipboard as w
  import win32con
  w.OpenClipboard()
  w.EmptyClipboard()
  w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
  w.CloseClipboard()



position = []  #用于保存选定矩形区域坐标信息
# create the hook mananger
hm = PyHook3.HookManager()
# register two callbacksq
hm.MouseLeftDown = OnMouseLeftDownEvent
hm.MouseLeftUp   = OnMouseLeftUpEvent
hm.KeyDown = OnKeyboardEvent
# hook into the mouse and keyboard events
hm.HookKeyboard()
pythoncom.PumpMessages()