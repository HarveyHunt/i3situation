import subprocess
import os
from i3situation.plugins._plugin import Plugin

__all__ = 'BatteryPlugin'


class BatteryPlugin(Plugin):
    """
    Displays information about the battery, such as its current charge and
    current status (Discharging, Full, Charging).
    """

    def __init__(self, config):
        self.options = {'format': '<charge>%',
                        'low_threshold': 20,
                        'low_color': '#FF0000',
                        'discharging_color': '#FF6103',
                        'charging_color': '#00F000',
                        'full_color': '#FFFFFF',
                        'percentage': True,
                        'battery_path': '/sys/class/power_supply/BAT0',
                        'interval': 30}

        super().__init__(config)

    def main(self):
        energy_now = int(self.get_battery_state('energy_now'))
        energy_full = int(self.get_battery_state('energy_full'))
        status = self.get_battery_state('status')

        charge = (energy_now / energy_full) * 100 if self.options['percentage'] else 1
        charge = int(charge)

        if charge > 100:
            charge = 100

        if charge < self.options['low_threshold']:
            self.output_options['color'] = self.options['low_color']
        elif status == 'Full':
            self.output_options['color'] = self.options['charging_color']
        elif status == 'Discharging':
            self.output_options['color'] = self.options['discharging_color']
        elif status == 'Charging':
            self.output_options['color'] = self.options['charging_color']

        output = self.options['format'].replace('<charge>', str(charge))
        output = output.replace('<status>', status)

        return self.output(output, output)

    def get_battery_state(self, prop):
        """
        Return the first line from the file located at battery_path/prop as a
        string.
        """
        with open(os.path.join(self.options['battery_path'], prop), 'r') as f:
                return f.readline().strip()
