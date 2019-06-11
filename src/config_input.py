{
  "ESS": {
    "SoC_Value": 100,
    "meta": {
      "ESS_Capacity": 70,
      "ESS_Max_Charge_Power": 33,
      "ESS_Max_Discharge_Power": 33,
      "ESS_Max_SoC": 1,
      "ESS_Min_SoC": 0.2
    }
  },
  "EV": {
    "ev1": {
      "Battery_Capacity_kWh": 18.7
    },
    "ev2": {
      "Battery_Capacity_kWh": 18.7
    },
    "ev3": {
      "Battery_Capacity_kWh": 18.7
    },
    "ev4": {
      "Battery_Capacity_kWh": 18.7
    },
    "ev5": {
      "Battery_Capacity_kWh": 18.7
    },
    "meta": {
      "Unit_Consumption_Assumption": 2.5,
      "Unit_Drop_Penalty": 1
    }
  },
  "chargers": {
    "charger1": {
      "Max_Charging_Power_kW": 7,
      "Hosted_EV": "ev1",
      "SoC": 0.2
    },
    "charger2": {
      "Max_Charging_Power_kW": 7,
      "Hosted_EV": "ev2",
      "SoC": 0.2
    },
    "charger3": {
      "Max_Charging_Power_kW": 7,
      "Hosted_EV": "ev3",
      "SoC": 0.2
    },
    "charger4": {
      "Max_Charging_Power_kW": 22,
      "Hosted_EV": "ev4",
      "SoC": 0.2
    },
    "charger5": {
      "Max_Charging_Power_kW": 22,
      "Hosted_EV": "ev5",
      "SoC": 0.2
    }
  },
  "uncertainty": {
    "Plugged_Time": {
      "mean": 18.76,
      "std": 1.3
    },
    "Unplugged_Time": {
      "mean": 7.32,
      "std": 0.78
    },
    "ESS_States": {
      "Min": 0,
      "Max": 100,
      "Steps": 10
    },
    "VAC_States": {
      "Min": 0,
      "Max": 100,
      "Steps": 2.5
    },
    "meta": {
      "monte_carlo_repetition": 10000
    }
  },
  "grid": {
    "meta": {
      "Max_Voltage_Drop": 1.1,
      "Min_Voltage_Drop": 0.9,
      "P_Grid_Max_Export_Power": 1000,
      "Q_Grid_Max_Export_Power": 1000
    }
  },
  "load": {
    "P_Load": [
      -0.57,
      -0.906,
      -0.906,
      -0.70066667,
      -0.77533333,
      -0.906,
      -0.906,
      -1.0935,
      -3.8135,
      -14.73716667,
      -9.88183333,
      -24.413,
      -4.216,
      -2.1725,
      -4.536,
      -4.899,
      -0.92466667,
      -0.88733333,
      -0.906,
      -4.7475,
      -4.8255,
      -10.51866667,
      -12.96316667,
      -2.00733333
    ],
    "meta": {
      "pf_Load": 1
    }
  },
  "photovoltaic": {
    "P_PV": [
      0,
      0,
      0,
      0,
      0,
      0.39367,
      4.75361,
      15.1473,
      15.867,
      31.79674,
      38.73189,
      33.29914,
      14.63464,
      24.09385,
      10.87046,
      20.06198,
      10.99505,
      2.28806,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "meta": {
      "PV_Inv_Max_Power": 3.5
    }
  }
}