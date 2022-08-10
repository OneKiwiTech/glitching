#ifndef BOARD_H
#define BOARD_H

void uart_init(void);
char getch(void);
void putch(char c);
void led_error(unsigned int x);
void led_ok(unsigned int x);
void trigger_high(void);
void trigger_low(void);

#endif
