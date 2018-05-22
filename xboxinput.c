#include <stdio.h>
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

#include "xboxinput.h"

struct XobxInputValue
xboxInputValue = {0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0};
                    
int xboxDev = 0;

InputValueHandler valueHanlder = NULL;

void syncInput()
{
    if (valueHanlder == NULL) {
        printf("-->X1:%6d Y1:%6d X2:%6d Y2:%6d du:%d dd:%d dl:%d dr:%d A:%d B:%d X:%d Y:%d lt:%6d rt:%6d lb:%d rb:%d back:%d guide:%d start:%d\n", 
            xboxInputValue.X1, xboxInputValue.Y1, xboxInputValue.X2, xboxInputValue.Y2,
            xboxInputValue.du, xboxInputValue.dd, xboxInputValue.dl, xboxInputValue.dr,
            xboxInputValue.A, xboxInputValue.B, xboxInputValue.X, xboxInputValue.Y,
            xboxInputValue.lt, xboxInputValue.rt, xboxInputValue.lb, xboxInputValue.rb,
            xboxInputValue.back, xboxInputValue.guide, xboxInputValue.start);
    }
    else {
        valueHanlder(xboxInputValue);
    }
}

void parseSyn(struct input_event ev)
{
    switch(ev.code) {
        case SYN_REPORT:
            syncInput();
            break;
        case SYN_CONFIG:
            printf("SYN_CONFIG\n");
            break;
        case SYN_MT_REPORT:
            printf("SYN_MT_REPORT\n");
            break;
        case SYN_DROPPED:
            printf("SYN_DROPPED\n");
            break;
        case SYN_MAX:
            printf("SYN_MAX\n");
            break;
        case SYN_CNT:
            printf("SYN_CNT\n");
            break;
        default:
            printf("syn default\n");
    }
}


void parseKey(struct input_event ev)
{
    switch (ev.code) {
        case BTN_A:
            xboxInputValue.A = ev.value;
            break;
        case BTN_B:
            xboxInputValue.B = ev.value;
            break;
        case BTN_X:
            xboxInputValue.X = ev.value;
            break;
        case BTN_Y:
            xboxInputValue.Y = ev.value;
            break;
        case BTN_TL:
            xboxInputValue.lb = ev.value;
            break;
        case BTN_TR:
            xboxInputValue.rb = ev.value;
            break;
        case BTN_MODE:
            xboxInputValue.guide = ev.value;
            break;
        case BTN_SELECT:
            xboxInputValue.back = ev.value;
            break;
        case BTN_START:
            xboxInputValue.start = ev.value;
            break;
        default:
            printf("type: %x value:%d\n", ev.code, ev.value);
            break;
    }
}

void parseAbs(struct input_event ev)
{
    switch (ev.code) {
        case ABS_X:
            xboxInputValue.X1 = ev.value;
            break;
        case ABS_Y:
            xboxInputValue.Y1 = ev.value;
            break;
        case ABS_Z:
            xboxInputValue.lt = ev.value;
            break;
        case ABS_RX:
            xboxInputValue.X2 = ev.value;
            break;
        case ABS_RY:
            xboxInputValue.Y2 = ev.value;
            break;
        case ABS_RZ:
            xboxInputValue.rt = ev.value;
            break;
        case ABS_HAT0X:
            if (ev.value == -1) {
                xboxInputValue.dl = 1;
            }
            else if(ev.value == 1) {
                xboxInputValue.dr = 1;
            }
            else {
                xboxInputValue.dl = 0;
                xboxInputValue.dr = 0;
            }
            break;
        case ABS_HAT0Y:
            if (ev.value == -1) {
                xboxInputValue.du = 1;
            }
            else if(ev.value == 1) {
                xboxInputValue.dd = 1;
            }
            else {
                xboxInputValue.du = 0;
                xboxInputValue.dd = 0;
            }
            break;
        default:
            printf("type: %x value:%d\n", ev.code, ev.value);
            break;
    }
}

bool openXboxInput(const char* dev)
{
    xboxDev = open(dev, O_RDONLY);
    if (xboxDev < 0) {
        return false;
    }
    return true;
}

void readXboxInput(InputValueHandler inputHanlder)
{
    struct input_event ev;
    if (inputHanlder != NULL)
        valueHanlder = inputHanlder;

    while(1)
    {
        int bytes = read(xboxDev, &ev, sizeof(ev));
        if (bytes != sizeof(ev)) {
            continue;
        }
        switch (ev.type) {
            case EV_KEY:
                parseKey(ev);
                break;
            case EV_ABS:
                parseAbs(ev);
                break;
            case EV_SYN:
                parseSyn(ev);
                break;
            default:
                break;
        }
    }
}

void closeXboxInput()
{
    if (xboxDev < 0) {
        return;
    }
    close(xboxDev);
}