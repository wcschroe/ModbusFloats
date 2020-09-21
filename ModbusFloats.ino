/*
 Name:		ModbusFloats.ino
 Created:	8/19/2020 10:55 AM
 Author:	William Schroeder
 Description: A test sketch for floating point modbus registers
*/
#include "ModbusRtu.h"
#include <Streaming.h>

enum {
    float1_LSB,
    float1_MSB,
    float2_LSB,
    float2_MSB,
    TOTAL_REGS_SIZE
};

uint16_t MBR[TOTAL_REGS_SIZE];

#define SlaveModbusAdd  1
#define Port1           1
#define Port2           2
#define Port3           3

Modbus ModbusSlavePortPrimary(SlaveModbusAdd, Port3);
Modbus ModbusSlavePortSecondary(SlaveModbusAdd, Port2);

union {
    uint16_t i[2];
    float f;
} converter;

float floatFromRegs(uint16_t *registers, uint8_t regAddr) {
    converter.i[0] = registers[regAddr];
    converter.i[1] = registers[regAddr + 1];
    return converter.f;
}

void floatToRegs(uint16_t *registers, float value, uint8_t regAddr) {
    converter.f = value;
    MBR[regAddr] = converter.i[0];
    MBR[regAddr + 1] = converter.i[1];
}

void setup() {
    pinMode(A5, OUTPUT);
    ModbusSlavePortPrimary.begin(115200, SERIAL_8N1);
    ModbusSlavePortSecondary.begin(115200, SERIAL_8N1);
    Serial.begin(115200);
    floatToRegs(MBR, 25.2197314, float1_LSB);
    floatToRegs(MBR, 129834.4, float2_LSB);
}

void loop() {
    if (ModbusSlavePortPrimary.poll(MBR, TOTAL_REGS_SIZE) > 4) digitalWrite(A5, HIGH);
    else digitalWrite(A5, LOW);
    if (ModbusSlavePortSecondary.poll(MBR, TOTAL_REGS_SIZE) > 4) digitalWrite(A4, HIGH);
    else digitalWrite(A4, LOW);
    // Serial.print(floatFromRegs(MBR, float1_LSB), 6);
    // Serial.print(",");
    // Serial.println(floatFromRegs(MBR, float2_LSB), 6);
}