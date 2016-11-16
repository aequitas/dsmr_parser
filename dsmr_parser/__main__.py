import argparse
import logging

from serial import EIGHTBITS, PARITY_EVEN, PARITY_NONE, PARITY_ODD, SEVENBITS

import dsmr_parser.obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.serial import (SERIAL_SETTINGS_V2_2, SERIAL_SETTINGS_V4,
                                SerialReader)

# mapping of obis to human readable names
obis_mapping = {
    obis.CURRENT_ELECTRICITY_USAGE: 'Power Consumption',
    obis.CURRENT_ELECTRICITY_DELIVERY: 'Power Production',
    obis.ELECTRICITY_ACTIVE_TARIFF: 'Power Tariff',
    obis.ELECTRICITY_USED_TARIFF_1: 'Power Consumption (low)',
    obis.ELECTRICITY_USED_TARIFF_2: 'Power Consumption (normal)',
    obis.ELECTRICITY_DELIVERED_TARIFF_1: 'Power Production (low)',
    obis.ELECTRICITY_DELIVERED_TARIFF_2: 'Power Production (normal)',
}


def console():
    """Output DSMR data to console."""

    parser = argparse.ArgumentParser(description=console.__doc__)
    parser.add_argument('--device', default='/dev/ttyUSB0',
                        help='port to read DSMR data from')
    parser.add_argument('--version', default='2.2', choices=['2.2', '4'],
                        help='DSMR version (2.2, 4)')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument('-p', '--parity', default=None, choices=[
                        PARITY_NONE, PARITY_EVEN, PARITY_ODD],
                        help='Override serial parity setting.')
    parser.add_argument('-b', '--bytesize', default=None, choices=[
                        SEVENBITS, EIGHTBITS], type=int,
                        help='Override serial bytesize setting.')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    settings = {
        '2.2': (SERIAL_SETTINGS_V2_2, telegram_specifications.V2_2),
        '4': (SERIAL_SETTINGS_V4, telegram_specifications.V4),
    }

    serial_settings = settings[args.version][0]
    if args.parity:
            serial_settings['parity'] = args.parity
    if args.bytesize:
            serial_settings['bytesize'] = args.bytesize

    serial_reader = SerialReader(
        device=args.device,
        serial_settings=serial_settings,
        telegram_specification=settings[args.version][1],
    )

    # print interesting values of each telegram as it comes in
    for telegram in serial_reader.read():
        for obiref, obj in telegram.items():
            if not obj or obiref not in obis_mapping:
                continue
            print(obis_mapping[obiref], obj.value, obj.unit)
        print()
