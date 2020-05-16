import queue
import threading
import pituophis
import PySimpleGUI as sg
import pyperclip
import os

# This is a graphical Gopher client in 200 lines of code, implemented with Pituophis and PySimpleGUI for an interface. Pyperclip is used for the "Copy URL" feature.
# A tree is used for loading in menus, similar to the likes of WSGopher32 and Cyberdog. Backlinks are cut out, and menus are trimmed of blank selectors. Threaded binary downloads are supported as well.
# Based on the Chat interface example here: https://pysimplegui.trinket.io/demo-programs#/demo-programs/chat-instant-message-front-end

icons = {'1': b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII=', '0': b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACRklEQVQ4jX3TvU8iQRgGcGorG5PNJlzOHImFxXXmSgu1pLYkFhbGFmta6Cn8U6ysbAzgfgwwM6y7sx8z67IgMuoq1XPNSSTovclTvr95JpMplf5No9HYbLfbRrvdNlqtltFqtYxGo2HU63WjXq8bZ2dnRq1WM2q1mnF6erpR+jyXl5cbhJDb0WgkP4dzLhljklIqh8OhJIRI27blzc3N7f7+/uYSaDabJudcBUGAKIoQRRHiOEaSJJBSrsVxnLRarZqlT/VNzrkKwxBxHMN1XXQ6HXS73bWkaQpCyNdAFEWQUsLzPDDGwDnHaDRaSZZl68DFxYXJOVdCCKRpin6/j16vB8uy1pLnOQgh6eHh4SrAGFNCCDw8PEAIAc/zcH9/D9/34fs+giBAEASYTqfrwPn5uUkpVUopZFkGSiksy4Jt23AcB67rghACQghms9n3QJqmGI/HCMMQvu9DCIE8zzGfz6G1htYa8/kcg8FgFTg5OTGHw6EKggB5nq8AYRiuPOvz8zP6/f4qcHx8bBJCVJIkmEwmiOMYQojlopQSSikopfD6+vo9kGUZJpMJOOfLOw8GA1BKwRgDYwxFUawD1WrVdF1XZVmG6XSKJEmW1T9OXywWWCwWXwMHBwc/er3e+KPB4+Mjnp6eoLXGy8sLiqLA+/s73t7eUBQFbNvO9/b2tpeAYRg/r66uPMuyZp1OR3e7XX13d6cty9KO42jXdZehlI6vr6+9ra2tysqP3NnZ2d7d3f1dqVT+/C9HR0flcrn862PvLwGSkDy9SoL4AAAAAElFTkSuQmCC', '7': b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACqUlEQVQ4jY2SXUhTYRjHn4pQtEJDGUU3dSV4U0hEV43uRlcl1oVd2Ae7KD+mJZUEnhzuhB+JLXaQdTbzuCMu54VG0XHfx2Q723Eed+bcmdOsdCOn6NRFmjvdSIjm6g/Pzfvw+/Hw5wXYlcbGRoler5d2d3dfRVH0zO592lAURbJj/vVP3kDK7vanRseDG3a7/XNbW1vOP2Gapm20J7CFGlyBN0PC5OuPQf6pbsTTRzFrHMetdXR05O0LDw4O1g97+C1VD8vNLawvRBeT8fB84isjxIVHuJvuG2JXaZqO7StwOOilZ7gtyghxYSa2+mX2e2I6HF3h2ak4qzTybxVqi9Pnn/yFouj5PTCCIHnOESZZrbFy3qlF/8TsMhuaTwxPfFs2U6NzpELHNt9usbx3jYVEg8FQt0eAomiuy+1NVr2yBCkuavEKC++4mSXSNh5TPiZ8d6txtu5Oi8Pk4UKiTqcr3yMQRfGAw+GIvyCd8XKt96UCZxUKLXvtPu6+WImz16twtvaJxuL0jQd+VlRUnPtrB11dXWVCOJKq1ph99zB3faWWvVWlZW9Uall5WbO5x8cLmwRBTO1bIgAARVF6IRxJYSZXrFZjZh5iFstzwhka9QspnudTnZ2dolKptKWVkCT5gGGYlYnJ0AYfDG1yHLdOEMQHkiSTJpNJVKvVokqlmk4rQRAkE0GQgoaGhgtyufwEABwsKSnJxzDsR29vr4hhmNjU1JQoKio6vJM7BACZAHAUAHIpiroUiURqwuFwTX9//2UAkGRlZZ1sb29fIklSHBgYEI1G45+PdXAHfBwAJMXFxQU4jss0Gs0VqVR6FgBOA8ApAJC0traGgsGgaLVaVwoLC4/sviIDALIB4BgA5ABA7vbkbL9lA0BGaWnpTZlMlp+2i//Nb4XAbVOmOUFgAAAAAElFTkSuQmCC',
         'h': b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC60lEQVQ4jYWTa0jTARTFb2grQijsW0kULfqW9sIia1ZkWVSmWRFhWUJqrexhoLMaFOTUMgktH/goclqW23y0NfO5Tc1tOififC7XKKnUzE3d+v9PX2JYjTyfz/lxufdcojkVvGBuz1+KFxbsyyySS4pK6npyimu7EkRSKf/Gs4srVwYu/G+Qy+UvKBLXNNU2GxiVthszMzOofqeCrNWCPJkeoqzX1qDTGRvdhgMDAz1lco21obULGm0njOYvqGvrhqrLCoV+GMrG9+jtG4SyrunnzmMJ2/4B5D1XvmIYBlNTU9C1G9BtHcOHcRYGix1KTTsmbTYwDAOr1Yr0zMIfXO6s3fj78326TQNOlmVRp2qF6fM0zOOAeRzosNjRqjeiuLIJFUo1+voHoNXqcDRSmOQCCO6Kjw8OWSBRNKGxdwL9o8DgGNAz4oTKaMGMwwGbzYbhj5+gbTfgtawaUXxhpwsgTHuR0qLvwlN5B6oMo2joncR7sx2a/gk064xgWRYsy8Jut+NVhQLil+U4fO6eiiicQ0REMQnFcQ9KtciXatDTb0bp2zaINZ9Q1GBBgUyDD8Mf8X3iB0ZGRqDV6XBB8BAhEaJ61wRHIlK3CvMbmTxpC1iWhcPhQJlCg5SyTgjFBlzNbUZW8RuYTCZUVb/BgeiHCD52+7EL4Od3ZsmlZJk+KVuJ0bExOJ1OfPk6irisesRmqhGRVovr919ArVYj80kuDkamTvP2Xtr5xxm3H0k8ESuqdCRnl2FoaAjZT8twUlSDsDtyBAsqcCoxFxKJBGf4Quw+GCdx16XVG4LO5ySlP2eq5Qrsu/YMu+LLwbtSiu2xheBFPUK84A627DlrIs+FPCLy/huwjIh2rPENyg6NFHwLu5rLHrqch/0xjxESnYHgEzcn/fxDaz08PMKJyJeI3D6ZNxGt53C8w3xWbL61btPhEr+AsPJVawMyvLyWRxMRj4jWENF8d+HZmkdEi34DlxLRYiLiuDP+AiIvzWJ84dNQAAAAAElFTkSuQmCC', 'i': b'R0lGODlhAQABAAAAACwAAAAAAQABAAA=', '3': b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACuklEQVQ4jX3T20pUcRQG8A8cpPZpcnSHmmZmhGVjBzTNiMxy//fM1OigXfUARVc9QvQMkQTdRFAg1E0lIlu0k5SlNZmZZzPMpnL27BkPeZi+LppMwVrw3a3fWjdrARtUl8tVNZSdfWVk5847IwUFtwezsi4/crmqNupdVy+A3eNeb6fj960sNTYwWV/HZKiei40NtE1jebSkpL0L2LUhHpVl75ejVZGfoRB/+nxMmiaTpsll0+SSaXJJCC7UBfmpony6Nz197zrcAuhTZQcnk2dOc+UPEoKLQvCHEFwQgvNCcE4Izgb8HCvdN2YBmasDhgsLbvwI+FfRHzAvBGeFYMIwGDcMOobBWG0to8JgOD+nCQBwE8icKjs0tWCaf7cIwYQQjAvxGwlBWwhGDYMzQvC7z8chb8nHZsCDTqD8W/VxzgYCTDQ1MW5ZjFsWnTWJtbUxZlmMWRaj164xEghw4shh3gf2o2vz5rMzp2roBIOMt7czkUisSywWo23btG2bjuMw2trKz8EgxyvL2ZGWVo9nLlfNtHGSM6EQnY6OVRiPx1fh2kzfusXR4mIOFBfRAo6hGdg2VFqSiBgGI34/pyoqOJGTwzG3myOaxmFN45Cm8YOqckBV+V5V+U5V2FuYG70L5KAZSO/Zkdc6rmdxVNM4kgKDqsoPKdCvKHynKOxTFIZlmWHPFj7epj+oBlwAAAs40leUPze4Zkt/CrxNodeyzF5ZZo8k8fn27MRDoGzdMT3V5Evh7bnLfZrGsCzzTQr1SBJfSRJfShJfyjK78rcudyrSxQ3P+bFbudBdkPv1te5hr2cLuxWF3bLM7gw3n+sePsnTI21u6fy/fmkTgKITQMP1DO3Bva2eiZY83b6fpzvNesbkVY/cWgmcA1AKQP/fU0oAcgHsOQBUlwI1ALwAdgDIAJC2tvkXFRyzrLKhFPAAAAAASUVORK5CYII=', '9': b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC+0lEQVQ4jXVSX0gbBxz+tm7UIt2cL33pU0tf7MPc9jAGUgajb3kb+NI+CC10o+QhQ7YnEXTii4IpZEnUwD0UhRj1vJx3OfLv4sXsDAQ1eGpcjH849e6yIxcNadfBfn1ZS632e/6+D74/wAfg8XjaBUFQ4/H4kc/n6/wQ7xxCodADt9v9GQB4vd5v8vn8i62tLYpEIh4A6OnpaYlEIj9dEIbD4Svz8/OPFEX5JxqN/smy7G/pdHr14OCATNOkzc3NciaT8aqqmrJtm1Kp1HO32331nAnDMD9ns9lXGxsbpGka6bpOlmXR6ekpNZtNsm2bHMch0zRJFMVnl0YQBCGxt7dHx8fHZNs2NRoNchyH6vU62bZN1WqV8vn8Xm9vb+sF8cDAwN1CoVA3DIMcxyHDMHRZlseTyeTvOzs7a4Zh0NHREZVKJWIY5qnH42kHAIyPj3dyHMepqlqwLIvOzs6oWq3+t7Cw8Osb80AgcH91dXV/d3eXNE2jXC5XEwRhPRAI/IKpqaknlUqFarUaNZtNajQaVKlUzgYHB2+/M+k1SZJSxWKRVlZWaGlpiRKJBPn9/ikEg8HbsVjsD1VVs/V6nWq1GpmmSSzLDgWDwU8BwO/3/yjL8kkul6NMJkPhcHglFAr1jY6OfvW2A6/Xe2d7e/vUsiw6OTmhcrn8tyzLYVEUJwuFwl+KolA8HqdoNEoTExMPL11BUZS4rut0eHhIpVKJ1tfXSVVVkmWZYrEYsSxLHMe9GBsbu3dBPDc397RcLr/a39+nYrFIa2trtLy8TMlkkgRBIJ7naXFxkRKJBHEcVxgaGrpx7onpdPqJpmkveZ5PTU5ODs7MzGxIkvQvz/M0Ozur+3y+0MjIyANJknanp6fnLkvQ2tfX97itra0TwHcdHR0PGYbRRVGk/v7+GQD3AHS6XK7vAXwB4KP3Da4CuAHgDoCvW1pafhgeHs4yDGN1d3f3AvgWQAeAmwCuX1ri//gYwDUAn3d1dd1yuVxfAmgH0Argk/fJrwEaXuWjl/RWWwAAAABJRU5ErkJggg=='}

texttypes = ['0', '1', '7', 'h']

gophertree = sg.TreeData()

sg.theme('DarkTeal1')  # Add a touch of color

plaintext_layout = sg.Output(key="-OUTPUT-", size=(80, 35), font=('Consolas 10'))

context_menu = ['', '&Copy URL']

gophermenu_layout = sg.Tree(data=gophertree, headings=[], change_submits=True,
                              auto_size_columns=True, num_rows=26, col0_width=80, max_col_width=200, key='_TREE_', show_expanded=True, enable_events=True, right_click_menu=context_menu, font='Consolas 10', background_color='#fff', text_color='#000')

layout = [[gophermenu_layout, plaintext_layout],
          [sg.Button('<'), sg.Input(size=(84, 5), key='-QUERY-', do_not_clear=True, default_text="gopher://gopherproject.org/1/", enable_events=True), sg.Button('Go'),
           # sg.Button('Exit'),
           ],
           [sg.Checkbox('Use hierarchy', key='-USETREE-', default=True), sg.Text('...', key='-LOADING-', visible=False), sg.Text('', key='-DOWNLOADS-', visible=True, size=(60, 1))]]

window = sg.Window('TreeGopher', layout, font=(
    'Helvetica', ' 13'), default_button_element_size=(8, 2))

openNodes = []


def trim_menu(menu):
    try:
        while menu[-1].text == '':
            del menu[-1]
    except:
        pass
    try:
        while menu[0].text == '':
            del menu[0]
    except:
        pass
    return menu


def populate(parentNode, request):
    global gophertree, openNodes

    window.FindElement('-QUERY-').update(request.url())
    window.FindElement('-LOADING-').update(visible=True)

    if not parentNode in openNodes:
        good = False
        try:
            resp = request.get()
            window.FindElement('-OUTPUT-').update('')
            menu = trim_menu(resp.menu())
            good = True
        except:
            sg.popup("We're sorry!", request.url(
            ) + ' could not be loaded for one reason or another. Try again later.')
        if good:
            for item in menu:
                if not item.request().url() in openNodes:
                    sub_url = item.request().url()
                    if item.path.startswith("URL:"):
                        sub_url = item.path[4:]
                    if item.type in icons:
                        icon = icons[item.type]
                    else:
                        icon = icons['9']
                    if item.type == 'i':
                        gophertree.insert(parentNode, sub_url,
                                          text=item.text, values=[], icon=icon)
                    else:
                        gophertree.insert(parentNode, sub_url, text=item.text, values=[
                            sub_url], icon=icon)

            openNodes.append(parentNode)

            window.FindElement('_TREE_').Update(gophertree)

    window.FindElement('-LOADING-').update(visible=False)

gui_queue = queue.Queue()

def download_thread(req, dlpath, gui_queue):     # This uses Pituophis' Request().stream() function to download a file chunks at a time (instead of all in one shot like with .get())
    with open(dlpath, "wb") as dl:
        remote_file = req.stream().makefile('rb')
        while True:
            piece = remote_file.read(1024)  
            if not piece:
                break
            dl.write(piece)
    gui_queue.put(dlpath)  # put a message into queue for GUI

history = []

def go(url):
    global gophertree, openNodes

    window.FindElement('-LOADING-').update(visible=True)

    req = pituophis.parse_url(url)
    window.FindElement('-QUERY-').update(req.url())
    if req.type in texttypes:
        if req.type in ['1', '7']:
            gophertree = sg.TreeData()
            gophertree.insert('', key=req.url(), text=req.url(),
                              values=[req.url()], icon=icons[req.type])
            parentNode = req.url()
            history.append(req.url())
            openNodes = []
            populate(parentNode, req)
        else:
            try:
                resp = req.get()
            except:
                next
            window.FindElement('-OUTPUT-').update('')
            print(resp.text())
    else:
        dlpath = sg.popup_get_file('Where to save this file?', 'Download {}'.format(
            req.url()), default_path=req.url().split('/')[-1], save_as=True)
        if not dlpath is None:
            window.FindElement('-DOWNLOADS-').update(value='Downloading {}'.format(dlpath))
            threading.Thread(target=download_thread, args=(req, dlpath, gui_queue), daemon=True).start()

    window.FindElement('-LOADING-').update(visible=False)


previousvalue = None

while True:     # The Event Loop
    event, value = window.read()
    if event in (None, 'Exit'):            # quit if exit button or X
        break
    elif event == '_TREE_':
        if value == previousvalue:
            previousevent = None
            # DOUBLE CLICK
            # TODO: cooldown
            window.FindElement('-LOADING-').update(visible=True)

            url = value['_TREE_'][0]

            if url.startswith('gopher'):
                req = pituophis.parse_url(url)
                if req.type == '1':
                    parentNode = url
                    if value['-USETREE-']:
                        populate(parentNode, req)
                    else:
                        go(parentNode)
                elif req.type == '7':
                    q = sg.popup_get_text('Search on ' + req.host, '')
                    if not q is None:
                        req.query = q
                        go(req.url())
                elif req.type in texttypes:
                    try:
                        resp = req.get()
                        window.FindElement('-OUTPUT-').update('')
                        print(resp.text())
                    except:
                        next
                elif req.type != 'i':
                    go(req.url())

                window.FindElement('-LOADING-').update(visible=False)
            else:
                os.startfile(url)
        previousvalue = value
    elif event == 'Go':
        go(value['-QUERY-'].rstrip())
    elif event == '<':
        if len(history) > 1:
            h = history[-2]
            history.remove(h)
            history.remove(history[-1])
            go(h)
    elif event == 'Copy URL':
        pyperclip.copy(value['_TREE_'][0])
    try:
        message = gui_queue.get_nowait()
    except queue.Empty:             # get_nowait() will get exception when Queue is empty
        message = None              # break from the loop if no more messages are queued up
    # if message received from queue, display the message in the Window
    if message:
        window.FindElement('-DOWNLOADS-').update(value='')
        sg.popup('Finished downloading {}'.format(message))
window.close()