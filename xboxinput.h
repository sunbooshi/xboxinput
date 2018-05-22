#ifndef XBOX_INPUT_H
#define XBOX_INPUT_H

#include <stdbool.h>

struct XobxInputValue {
    int X1;
    int Y1;
    int X2;
    int Y2;
    int A;
    int B;
    int X;
    int Y;
    int du;
    int dd;
    int dl;
    int dr;
    int back;
    int guide;
    int start;
    int lt;
    int lb;
    int rt;
    int rb;
};

typedef void (*InputValueHandler)(struct XobxInputValue);

bool openXboxInput(const char* dev);

void readXboxInput(InputValueHandler inputHanlder);

void closeXboxInput();

#endif