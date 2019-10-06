#!/usr/bin/env python3
import sys
import os
import argparse
import yaml

sys.path.insert(0,
                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '../pwnagotchi/'))

from pwnagotchi.ui.display import Display, VideoHandler
from PIL import Image


class CustomDisplay(Display):

    def __init__(self, config, state):
        self.last_image = None
        super(CustomDisplay, self).__init__(config, state)

    def _http_serve(self):
        # do nothing
        pass

    def _on_view_rendered(self, img):
        self.last_image = img

    def get_image(self):
        """
        Return the saved image
        """
        return self.last_image


class DummyPeer:
    @staticmethod
    def name():
        return "beta"


def append_images(images, horizontal=True, xmargin=0, ymargin=0):
    w, h = zip(*(i.size for i in images))

    if horizontal:
        t_w = sum(w)
        t_h = max(h)
    else:
        t_w = max(w)
        t_h = sum(h)

    result = Image.new('RGB', (t_w, t_h))

    x_offset = 0
    y_offset = 0

    for im in images:
        result.paste(im, (x_offset, y_offset))
        if horizontal:
            x_offset += im.size[0] + xmargin
        else:
            y_offset += im.size[1] + ymargin

    return result


def main():
    parser = argparse.ArgumentParser(description="This program emulates\
                                     the pwnagotchi display")
    parser.add_argument('--displays', help="Which displays to use.", nargs="+",
                        default="waveshare_2")
    parser.add_argument('--lang', help="Language to use",
                        default="en")
    parser.add_argument('--output', help="Path to output image (PNG)", default="preview.png")
    parser.add_argument('--xmargin', type=int, default=5)
    parser.add_argument('--ymargin', type=int, default=5)
    args = parser.parse_args()

    config_template = '''
    main:
        lang: {lang}
    ui:
        fps: 0.3
        display:
            enabled: false
            rotation: 180
            color: black
            refresh: 30
            type: {display}
            video:
                enabled: true
                address: "0.0.0.0"
                port: 8080
    '''

    list_of_displays = list()
    for display_type in args.displays:
        config = yaml.safe_load(config_template.format(display=display_type,
                                                       lang=args.lang))
        display = CustomDisplay(config=config, state={'name': f"{display_type}>"})
        list_of_displays.append(display)

    columns = list()

    for display in list_of_displays:
        emotions = list()
        # Starting
        display.on_starting()
        display.update()
        emotions.append(display.get_image())
        display.on_ai_ready()
        display.update()
        emotions.append(display.get_image())
        display.on_normal()
        display.update()
        emotions.append(display.get_image())
        display.on_new_peer(DummyPeer())
        display.update()
        emotions.append(display.get_image())
        display.on_lost_peer(DummyPeer())
        display.update()
        emotions.append(display.get_image())
        display.on_free_channel('6')
        display.update()
        emotions.append(display.get_image())
        display.wait(2)
        display.update()
        emotions.append(display.get_image())
        display.on_bored()
        display.update()
        emotions.append(display.get_image())
        display.on_sad()
        display.update()
        emotions.append(display.get_image())
        display.on_motivated(1)
        display.update()
        emotions.append(display.get_image())
        display.on_demotivated(-1)
        display.update()
        emotions.append(display.get_image())
        display.on_excited()
        display.update()
        emotions.append(display.get_image())
        display.on_deauth({'mac': 'DE:AD:BE:EF:CA:FE'})
        display.update()
        emotions.append(display.get_image())
        display.on_miss('test')
        display.update()
        emotions.append(display.get_image())
        display.on_lonely()
        display.update()
        emotions.append(display.get_image())
        display.on_handshakes(1)
        display.update()
        emotions.append(display.get_image())
        display.on_rebooting()
        display.update()
        emotions.append(display.get_image())

        # append them all together (vertical)
        columns.append(append_images(emotions, horizontal=False, xmargin=args.xmargin, ymargin=args.ymargin))

    # append columns side by side
    final_image = append_images(columns, horizontal=True, xmargin=args.xmargin, ymargin=args.ymargin)
    final_image.save(args.output, 'PNG')


if __name__ == '__main__':
    SystemExit(main())
