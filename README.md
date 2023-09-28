# Solar Panel Sizing Tool

The Solar Panel Sizing Tool is designed to help you analyze the ideal size of solar panels, in the context of the Berlin subsidy program for mini balcony solar powerplants, which limits the inverter power to 600 watts. This tool 
calculates 
various metrics, including energy generation and payback time, based on user-defined parameters and solar radiation data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output](#output)
- [License](#license)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/riparise/solar-panel-sizing-tool.git
   ```

2. Change to the project directory:

   ```bash
   cd solar-panel-sizing-tool
   ```

3. Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the Solar Panel Sizing Tool, follow these steps:

1. Modify the YAML configuration file (`config.yml`) with your specific parameters. Here is the parameters list:

- `latitude` and `longitude`: The geographical coordinates of your location.
- `panel_azimuth` and `panel_angle`: The azimuth angle and tilt angle of your solar panels.
- `max_inverter_power`: The maximum inverter power (limited to 600 watts for the Berlin subsidy program).
- `latitude` and `longitude`: The geographical coordinates of your location.
- `panel_azimuth` and `panel_angle`: The azimuth angle and tilt angle of your solar panels.
- `max_inverter_power` and `inverter_efficiency`: The maximum inverter power and average efficiency (limited to 600 watts for the Berlin subsidy program).
- `panel_price_per_watt` and `energy_cost_per_kwh`: Costs related to solar panel installation and energy rates.
- `system_losses`: other losses that are not associated with inverter efficiency (panels degradation, glass transmittance, dirty, etc.)
- `installation_costs` and `subsidy_amount`: Additional costs and subsidies.
- `horizon_data`: list of elevation of horizon in degrees, at arbitrary number of equally spaced azimuths clockwise from north. (e.g. for a south faced façade with buildings nearby [90, 90, 90, 20, 20, 20, 90, 90])
- `pv_tech`: Cell technologies. Options are 'crystSi', 'CIS', 'CdTe' or 'Unknown'}, defaults to 'crystSi'
- `panel_sizes`: List of the panel sizes to be analysed in Watts

Feel free to modify these parameters to match your specific setup and requirements.

   Adjust the values to match your specific setup and preferences.

2. Run the main script using Python:

   ```bash
   python solar_panel_sizing.py
   ```

   The script will load the configuration from the `config.yml` file, retrieve solar radiation data, calculate trade-off metrics, and plot the results.

3. Review the generated plots and metrics to make an informed decision about the ideal size of solar panels for your mini balcony solar powerplant.

## Output

The tool generates three plots to help you analyze your solar panel sizing:

![Output Example](/output_example.png)

1. **Average Solar Radiation:** This plot shows the average historical solar generation (per kW of solar panel) throughout the day, categorized by seasons (Winter, Spring, Summer, Fall). use this graph mostly for sanity check if the 
   input is correct (like if there is shadow in the early morning, you should see it in the graph)

2. **Energy Generation vs. Panel Size and Payback Time:** This plot illustrates the relationship between panel size and energy generation per year, along with the payback time.

3. **Balance Over Time for Different Panel Sizes:** This plot displays the balance over time in euros for different panel sizes, allowing you to compare the financial aspects of your solar powerplant.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
Radiation data from 2006 and 2020 from [European Photoboltaic Geographical Information System](https://re.jrc.ec.europa.eu/api/v5_2/) using the amazing [pvlib](https://pvlib-python.readthedocs.io/en/stable/) library for the power 
calculations.