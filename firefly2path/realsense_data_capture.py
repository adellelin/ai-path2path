import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
import drawSvg as draw
import strokesToSVG as stroke


isInStroke = False
hasNewStroke = False
strokePoints = []
strokeCharacter = []

def log_everything(dispatcher):
    dispatcher.map("/*", print)


def log_gesture(dispatcher):
    dispatcher.map("/cursor/*/open", print)
    dispatcher.map("/cursor/*/close", print)


def log_hand(dispatcher):
    dispatcher.map("/cursor/*/right", print)
    dispatcher.map("/cursor/*/left", print)


def process_hand(dispatcher):
    dispatcher.map("/cursor/*/right", process_hand_point)
    dispatcher.map("/cursor/*/left", process_hand_point)


def process_heartbeat(dispatcher):
    dispatcher.map("/cursor/*/heartbeat", print_stroke_points)


def process_open_gesture(dispatcher):
    dispatcher.map("/cursor/*/close", print_character_points)


def process_hand_point(address, x, y, z):
    global isInStroke
    if z < .5:
        #if isInStroke is False:
        print("ENTERING x:", x, "y:", y, "z:", z)
        append_stroke_point(x,y)
        isInStroke = True

    else:
        if isInStroke is True:
            print("EXITING x:", x, "y:", y, "z:", z)
            print_stroke_points(None, None)
            #append_stroke_point(x,y)
            isInStroke = False


def append_stroke_point(x, y):
    global hasNewStroke
    point_x = int(round(x*200))
    point_y = int(round(y*200))
    strokePoints.append([-point_x, point_y])
    hasNewStroke = True


# exit the stroke threshold, add points to character array and then clear stroke array
def print_stroke_points(address, time):
    global hasNewStroke
    global strokePoints
    print("stroke", strokePoints)
    if hasNewStroke is True:
        strokeCharacter.append(strokePoints)
        strokePoints = []
        hasNewStroke = False


def print_character_points(address, time):
    global hasNewCharacter
    global strokeCharacter
    #print("stroke", strokePoints)
    print("character", strokeCharacter)
    if (len(strokeCharacter) != 0):
        stroke.main(strokeCharacter)
        strokeCharacter = []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="239.255.0.85", help="The ip (multicast or unicast) to listen on")
    parser.add_argument("--port",
                        type=int, default=10085, help="The port to listen on")
    parser.add_argument("--ifaceip",
                        default="10.10.10.35", help="The ip of the interface to listen on, if multicast")
    args = parser.parse_args()

    address = (args.ip, args.port)
    interface_addr = args.ifaceip

    dispatch = dispatcher.Dispatcher()
    # log_everything(dispatch)
    log_gesture(dispatch)
    #log_hand(dispatch)
    process_hand(dispatch)
    process_open_gesture(dispatch)
    #process_heartbeat(dispatch)

    # server = osc_server.ThreadingOSCUDPServer(address, dispatch, interface_addr)

    server = osc_server.BlockingOSCUDPServer((args.ip, args.port), dispatch, args.ifaceip)

    server.serve_forever()
