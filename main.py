import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pvlib
import yaml


def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config


def main():
    # Load configuration from YAML file
    config = load_config('config.yml')

    # Extract parameters from the configuration
    latitude = config['latitude']
    longitude = config['longitude']
    panel_angle = config['panel_angle']
    panel_azimuth = config['panel_azimuth']
    pv_tech = config['pv_tech']
    horizon_data = config['horizon_data']
    system_losses = config['system_losses']
    inverter_efficiency = config['inverter_efficiency']
    max_inverter_power = config['max_inverter_power']
    panel_price = config['panel_price']
    energy_cost_per_kwh = config['energy_cost_per_kwh']
    installation_costs = config['installation_costs']
    subsidy_amount = config['subsidy_amount']
    panel_sizes = config['panel_sizes']
    unused_energy = config['unused_energy']

    # Retrieve solar radiation data
    solar_data = get_solar_radiation_data(latitude, longitude, panel_angle, panel_azimuth, pv_tech, horizon_data, system_losses)

    # Calculate trade-off metrics
    energy_generated, payback_time, balances = calculate_trade_off(solar_data,
                                                                   max_inverter_power,
                                                                   panel_price,
                                                                   installation_costs,
                                                                   inverter_efficiency,
                                                                   energy_cost_per_kwh,
                                                                   subsidy_amount,
                                                                   panel_sizes, unused_energy)

    # Plot and display results
    plot_results(panel_sizes, energy_generated, payback_time, balances, solar_data, max_inverter_power)


def calculate_trade_off(solar_data, max_inverter_power, panel_price, installation_costs,
                        inverter_efficiency, energy_cost_per_kwh, subsidy_amount, panel_sizes, unused_energy):
    energy_generated, payback_time, balances = [], [], []
    if type(panel_price) is list and len(panel_price) != len(panel_sizes):
        raise ValueError('Panel price is not a single coefficient, but also not the same size as the panel sizes')

    num_years = (solar_data.index[-1] - solar_data.index[0]).days / 365

    for i, panel_size in enumerate(panel_sizes):
        # Calculate energy generation and financial metrics
        energy_per_hour = np.minimum(panel_size * solar_data['P'], max_inverter_power)
        if type(panel_price) is list:
            initial_cost = panel_price[i] + installation_costs
        else:
            initial_cost = panel_size * panel_price + installation_costs
        income = energy_per_hour * inverter_efficiency * energy_cost_per_kwh * (1-unused_energy) / 1000
        balances.append(min(-initial_cost + subsidy_amount, 0) + np.cumsum(income))

        total_energy_generated = sum(energy_per_hour) * inverter_efficiency * (1-unused_energy)
        energy_generated.append(total_energy_generated / (num_years * 1000))

        payback_time.append(max(initial_cost - subsidy_amount, 0) / (energy_generated[-1] * energy_cost_per_kwh))

    return energy_generated, payback_time, balances


def plot_results(panel_sizes, energy_generated, payback_time, balances, solar_data, max_inverter_power):
    fig, axs = plt.subplots(3, figsize=(12, 12), dpi=200)

    # Plot average solar radiation
    plot_average_generation(axs[0], solar_data)

    # Plot energy generation versus panel size and payback time
    plot_energy_vs_size(axs[1], panel_sizes, energy_generated, payback_time)

    # Plot balance over time for different panel sizes with labels
    plot_balance_over_time(axs[2], panel_sizes, balances, solar_data)

    # Add title and improve layout
    plt.suptitle("Solar Panel Study")
    plt.tight_layout(rect=(0.0, 0.03, 1.0, 0.95))
    plt.show()


def plot_average_generation(ax, solar_data):
    solar_data['Month'] = solar_data.index.month
    seasons = {
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    }
    season_colors = {
        'Winter': 'blue',
        'Spring': 'green',
        'Summer': 'red',
        'Fall': 'orange'
    }

    solar_data['Season'] = solar_data['Month'].map(seasons)
    avg_radiation = solar_data.groupby(['Season', solar_data.index.hour])['P'].mean()

    seasons = np.unique(solar_data['Season'])

    for i, season in enumerate(seasons):
        seasonal_data = avg_radiation[season]
        ax.plot(seasonal_data.index, seasonal_data.values, alpha=0.8, color=season_colors[season], label=season)

    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Energy generated\n[kWh/kW]')
    ax.set_title(f'Average Hourly Energy Generation per kW of installed solar panels')
    ax.set_xticks(range(24), [str(i) for i in range(24)])
    ax.legend()


def plot_energy_vs_size(ax, panel_sizes, energy_generated, payback_time):
    ax.set_title('Energy Generation and payoff time vs. panel size')
    ax.set_xlabel('Panel Size [W]')
    ax.set_ylabel('Energy Generation\n[kWh/Year]', color='b')
    ax.plot(panel_sizes, energy_generated, linestyle='-', color='b', marker='o')
    ax.tick_params(axis='y', labelcolor='b')

    ax_twin = ax.twinx()
    ax_twin.set_ylabel('Payback Time\n[Years]', color='r')
    ax_twin.plot(panel_sizes, payback_time, linestyle='-', color='r', marker='o')
    ax_twin.tick_params(axis='y', labelcolor='r')


def plot_balance_over_time(ax, panel_sizes, balances, solar_data):
    ax.set_title('Return over time vs. panel size')
    ax.set_xlabel('Time [Years]')
    ax.set_ylabel('Balance\n[euros]')
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(min(panel_sizes), max(panel_sizes))

    for i, balance in enumerate(balances):
        years_since_start = (solar_data.index - solar_data.index[0]).days / 365
        color = cmap(norm(panel_sizes[i]))
        label = f'Panel Size: {panel_sizes[i]} W'
        ax.plot(years_since_start, balance, linestyle='-', color=color, label=label)

    ax.axhline(0, color='k', linestyle='-')
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    ax.legend(loc='upper left')  # Add legend to the upper left corner of the plot


def get_solar_radiation_data(latitude, longitude, panel_angle, panel_azimuth, pv_tech, horizon_data, system_losses):
    data, inputs, meta = pvlib.iotools.get_pvgis_hourly(
        latitude=latitude,
        longitude=longitude,
        start=pd.Timestamp('2016-01-01'),
        end=pd.Timestamp('2020-12-31'),
        raddatabase='PVGIS-SARAH2',
        surface_tilt=panel_angle,
        surface_azimuth=panel_azimuth,
        pvcalculation=True,
        peakpower=0.001,
        usehorizon=True,
        pvtechchoice=pv_tech,
        userhorizon=horizon_data,
        components=False,
        mountingplace='building',
        loss=system_losses*100,
        url='https://re.jrc.ec.europa.eu/api/v5_2/',
    )
    solar_data = data[['P']].copy()
    return solar_data


if __name__ == '__main__':
    main()
