#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#include "xboxinput.h"

void valHandler(struct XobxInputValue val)
{
    printf("->X1:%6d Y1:%6d X2:%6d Y2:%6d du:%d dd:%d dl:%d dr:%d A:%d B:%d X:%d Y:%d lt:%6d rt:%6d lb:%d rb:%d back:%d guide:%d start:%d\n", 
        val.X1, val.Y1, val.X2, val.Y2,
        val.du, val.dd, val.dl, val.dr,
        val.A, val.B, val.X, val.Y,
        val.lt, val.rt, val.lb, val.rb,
        val.back, val.guide, val.start);
}

void exitHandler(){
    // Close dev
    closeXboxInput();
    exit(0);
}

int main()
{
    const char devname[] = "/dev/input/event0";
    
    signal(SIGINT, exitHandler);

    if (openXboxInput(devname)) {
        readXboxInput(valHandler);
    }

    return 0;
}