import os
import pituophis

splash = """
 __       ___  ___         ___  ___  __  
/  `  /\   |  |__  |\ | | |__  |__  |__) 
\__, /--\  |  |___ | \| | |    |___ |  \ 
https://github.com/dotcomboom/pituophis
"""

home = 'gopher://gopher.floodgap.com/1/'
typeIcons = {
  "i": "ℹ️",
  "1": "🚪",
  "0": "📝",
  "h": "🌎",
  "7": "🔍",
  "9": "⚙️"
}
noLinkTypes = {"i", "h"}
compatibleTypes = {'0', '1', '7'}
menuTypes = {'1', '7'}
lastType = '1'

def bold(txt):
  return "\033[1m" + txt + "\033[0;0m"

requests = {}
def go(url, itype=''):
  req = pituophis.parse_url(url)
  if req.url().endswith('/'):
    req.type = '1'
  if itype == '7':
    req.type = itype
  if req.type in menuTypes:
    os.system('clear')
    print(splash)
  print(bold('URL: ' + req.url()))
  if req.type == '7':
    if req.query == '':
      req.query = input(bold('Search term: '))
  if req.type in compatibleTypes:
    resp = req.get()
    if req.type in menuTypes:
      menu = resp.menu()
      selectors = 0
      for selector in menu:
        text = typeIcons['9']
        if selector.type in typeIcons:
          text = typeIcons[selector.type]
        text = text + '  ' + selector.text
        if selector.type not in noLinkTypes:
          selectors += 1
          requests[selectors] = selector.request()
          text = text + ' (' + requests[selectors].url() + ') ' + bold('[#' + str(selectors) + ']')
        if selector.path.startswith('URL:'):
          text = text + ' (' + selector.path.split('URL:')[1] + ')'
        print(text)
    elif req.type == '0':
      print(resp.text())
  else:
    print("nyi binaries")

go(home)
while True:
  cmd = input(bold('# or URL: '))
  try:
    cmd = int(cmd)
    go(requests[cmd].url(), requests[cmd].type)
  except Exception:
    go(cmd)