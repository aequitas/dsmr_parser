"""Test telegram parsing."""

import pytest
from dsmr_parser import telegram_specifications
from dsmr_parser.obis_references import (CURRENT_ELECTRICITY_USAGE,
                                         GAS_METER_READING,
                                         HOURLY_GAS_METER_READING)
from dsmr_parser.parsers import TelegramParser, TelegramParserV2_2

TELEGRAM_V2_2 = [
    "/ISk5\2MT382-1004",
    "",
    "0-0:96.1.1(00000000000000)",
    "1-0:1.8.1(00001.001*kWh)",
    "1-0:1.8.2(00001.001*kWh)",
    "1-0:2.8.1(00001.001*kWh)",
    "1-0:2.8.2(00001.001*kWh)",
    "0-0:96.14.0(0001)",
    "1-0:1.7.0(0001.01*kW)",
    "1-0:2.7.0(0000.00*kW)",
    "0-0:17.0.0(0999.00*kW)",
    "0-0:96.3.10(1)",
    "0-0:96.13.1()",
    "0-0:96.13.0()",
    "0-1:24.1.0(3)",
    "0-1:96.1.0(000000000000)",
    "0-1:24.3.0(161107190000)(00)(60)(1)(0-1:24.2.1)(m3)",
    "(00001.001)",
    "0-1:24.4.0(1)",
    "!",
]

TELEGRAM_ZCF110 = [
    "/XMX5LGBBFG1012530239",
    "",
    "1-3:0.2.8(42)",
    "0-0:1.0.0(161116201035W)",
    "0-0:96.1.1(00000000000000)",
    "1-0:1.8.1(000075.067*kWh)",
    "1-0:1.8.2(000084.813*kWh)",
    "1-0:2.8.1(000000.000*kWh)",
    "1-0:2.8.2(000000.000*kWh)",
    "0-0:96.14.0(0002)",
    "1-0:1.7.0(01.010*kW)",
    "1-0:2.7.0(00.000*kW)",
    "0-0:96.7.21(00002)",
    "0-0:96.7.9(00000)",
    "1-0:99.97.0(0)(0-0:96.7.19)",
    "1-0:32.32.0(00000)",
    "1-0:32.36.0(00000)",
    "0-0:96.13.1()",
    "0-0:96.13.0()",
    "1-0:31.7.0(012*A)",
    "1-0:21.7.0(02.778*kW)",
    "1-0:22.7.0(00.000*kW)",
    "0-1:24.1.0(003)",
    "0-1:96.1.0(4730303435303031363038313037323136)",
    "0-1:24.2.1(161116200000W)(00001.001*m3)",
    "!CC1E",
]


@pytest.mark.parametrize('telegram_lines', [
    TELEGRAM_V2_2,
])
def test_parse_v2_2(telegram_lines):
    """Test if telegram parsing results in correct results."""

    parser = TelegramParserV2_2(telegram_specifications.V2_2)
    result = parser.parse(telegram_lines)

    assert float(result[CURRENT_ELECTRICITY_USAGE].value) == 1.01
    assert result[CURRENT_ELECTRICITY_USAGE].unit == 'kW'
    assert float(result[GAS_METER_READING].value) == 1.001
    assert result[GAS_METER_READING].unit == 'm3'


@pytest.mark.parametrize('telegram_lines', [
    TELEGRAM_ZCF110,
])
def test_parse_v4(telegram_lines):
    """Test parsing v4 telegrams."""

    parser = TelegramParser(telegram_specifications.V4)
    result = parser.parse(telegram_lines)

    assert float(result[CURRENT_ELECTRICITY_USAGE].value) == 1.01
    assert result[CURRENT_ELECTRICITY_USAGE].unit == 'kW'
    assert float(result[HOURLY_GAS_METER_READING].value) == 1.001
    assert result[HOURLY_GAS_METER_READING].unit == 'm3'
