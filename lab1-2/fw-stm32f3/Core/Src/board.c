#include "board.h"
#include "stm32f3xx_hal.h"

UART_HandleTypeDef huart1;

void Errors_Handler(void)
{

    /* User can add his own implementation to report the HAL error return state */
    __disable_irq();
    while (1)
    {
    }
}

void uart_init(void)
{
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    huart1.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
    huart1.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
    if (HAL_UART_Init(&huart1) != HAL_OK)
    {
        Errors_Handler();
    }
}

char getch(void)
{
    uint8_t d;
    while (HAL_UART_Receive(&huart1, &d, 1, 5000) != HAL_OK)
    USART1->ICR |= (1 << 3);
    //putch(d);
    return d;
}

void putch(char c)
{
    uint8_t d  = c;
    HAL_UART_Transmit(&huart1,  &d, 1, 5000);
}

void led_error(unsigned int x)
{
    if (x)
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, RESET);
    else
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, SET);
}

void led_ok(unsigned int x)
{
    if (x)
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, RESET);
    else
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, SET);
}


void trigger_high(void)
{
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_12, SET);
}

void trigger_low(void)
{
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_12, RESET);
}
